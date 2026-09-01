import os
from datetime import datetime, timedelta
from functools import lru_cache

from flask import Response, current_app, stream_with_context
from hydromosaic.database import Outlet, Timeseries, Variable, Scenario, Model, Datafile
from netCDF4 import Dataset
from hms import get_app_session

ROW_CHUNK_SIZE = int(os.getenv("HMS_NETCDF_ROW_CHUNK_SIZE", "4096"))


def time_string(reference, units, increment):
    if units == "hours":
        return (reference + timedelta(hours=increment)).strftime("%Y-%m-%d %H:%M:%S")
    elif units == "days":
        return (reference + timedelta(days=increment)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        raise ValueError(f"Unknown time units: {units}")


def basin_name_string(value):
    if isinstance(value, bytes):
        return value.decode("utf-8").strip()
    return str(value).strip()


def basin_name_index_map_from_values(basin_names):
    return {
        basin_name_string(value): index
        for index, value in enumerate(basin_names[:].tolist())
    }


@lru_cache(maxsize=32)  # 32 directory paths
def basin_name_index_map(parent_dir):
    for entry in sorted(os.scandir(parent_dir), key=lambda item: item.name):
        if not entry.is_file() or not entry.name.endswith((".nc")):
            continue

        with Dataset(entry.path) as nc:
            basin_names = nc.variables.get("basin_name")
            if basin_names is None:
                continue

            return basin_name_index_map_from_values(basin_names)

    raise ValueError(f"No basin_name variable found in NetCDF files under {parent_dir}")


def time_reference_and_units(time_units_string):
    if "hours since" in time_units_string:
        return (
            datetime.strptime(time_units_string, "hours since %Y-%m-%d %H:%M:%S"),
            "hours",
        )
    elif "days since" in time_units_string:
        return (
            datetime.strptime(time_units_string, "days since %Y-%m-%d %H:%M:%S"),
            "days",
        )
    else:
        raise ValueError(f"Unknown time units: {time_units_string}")


def timeseries_data(subid, ts_id):
    """Return a timeseries in CSV format, one metadata table and one timeseries table"""

    # Get the metadata from the database, build metadata table
    _timeseries, variable_name, scenario_name, model_name, filename = (
        get_app_session()
        .query(
            Timeseries,
            Variable.standard_name,
            Scenario.short_name,
            Model.short_name,
            Datafile.filename,
        )
        .join(Variable, Variable.id == Timeseries.variable_id)
        .join(Scenario, Scenario.id == Timeseries.scenario_id)
        .join(Model, Model.id == Timeseries.model_id)
        .join(Datafile, Datafile.id == Timeseries.datafile_id)
        .join(Outlet, Outlet.id == Timeseries.outlet_id)
        .filter(Outlet.code == subid, Timeseries.id == ts_id)
        .one()
    )

    metadata = (
        f"Attribute, Value\n"
        f"Variable, {variable_name}\n"
        f"Outlet, {subid}\n"
        f"Scenario, {scenario_name}\n"
        f"Model, {model_name}\n"
        f"\n"
    )

    @stream_with_context
    def generate_rows():
        yield metadata

        with Dataset(filename) as nc:
            yield f"Time, {variable_name} ({nc.variables[variable_name].units})\n"

            basin_names = nc.variables["basin_name"]
            outlet_index = basin_name_index_map(os.path.dirname(filename))[subid]
            basin_name = basin_name_string(basin_names[outlet_index])
            if basin_name != subid:
                current_app.logger.warning(
                    "Cached basin index mismatch for subid %s in %s; rebuilding from file",
                    subid,
                    filename,
                )
                outlet_index = basin_name_index_map_from_values(basin_names)[subid]

            time_variable = nc.variables["time"]
            reference_time, time_units = time_reference_and_units(time_variable.units)
            num_rows = len(time_variable)

            for start in range(0, num_rows, ROW_CHUNK_SIZE):
                stop = min(start + ROW_CHUNK_SIZE, num_rows)
                time_values = time_variable[start:stop]
                data_values = nc.variables[variable_name][start:stop, outlet_index]

                for time_value, data_value in zip(time_values, data_values):
                    yield f"{time_string(reference_time, time_units, time_value)}, {data_value}\n"

    return Response(generate_rows(), mimetype="text/csv")
