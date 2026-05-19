import os
from datetime import datetime, timedelta
from functools import lru_cache

from flask import current_app
from hydromosaic.database import Outlet, Timeseries, Variable, Scenario, Model, Datafile
from netCDF4 import Dataset
from hms import get_app_session


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


@lru_cache(maxsize=32) #32 directory paths
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

    # Fetch data from netCDF file, build data table
    with Dataset(filename) as nc:
        header = f"Time, {variable_name} ({nc.variables[variable_name].units})\n"

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
        # timestamps may be given in either hours or days
        if "hours since" in nc.variables["time"].units:
            reference_time = datetime.strptime(
                nc.variables["time"].units, "hours since %Y-%m-%d %H:%M:%S"
            )
            time_units = "hours"
        elif "days since" in nc.variables["time"].units:
            reference_time = datetime.strptime(
                nc.variables["time"].units, "days since %Y-%m-%d %H:%M:%S"
            )
            time_units = "days"
        else:
            raise ValueError(f"Unknown time units: {nc.variables['time'].units}")

        timestamps = [
            time_string(reference_time, time_units, t) for t in nc.variables["time"][:]
        ]
        data = nc.variables[variable_name][0 : len(timestamps), outlet_index]

    data_rows = [f"{timestamps[i]}, {data[i]}" for i in range(len(timestamps))]

    return metadata + header + "\n".join(data_rows)
