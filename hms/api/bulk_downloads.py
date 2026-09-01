import os
import tempfile
from pathlib import Path

import numpy as np
from flask import send_file
from hydromosaic.database import Datafile, Model, Outlet, Scenario, Timeseries, Variable
from netCDF4 import Dataset

from hms import get_app_session
from hms.api.data import basin_name_index_map_from_values

CHUNK_SIZE = int(os.getenv("HMS_NETCDF_ROW_CHUNK_SIZE", "4096"))


def copy_attributes(source, target):
    target.setncatts(
        {
            name: source.getncattr(name)
            for name in source.ncattrs()
            if name != "_FillValue"
        }
    )


def creation_options(variable, chunksizes):
    filters = variable.filters()
    options = {
        "zlib": bool(filters.get("zlib")),
        "shuffle": bool(filters.get("shuffle")),
    }
    if filters.get("zlib"):
        options.update(complevel=filters["complevel"], chunksizes=chunksizes)
    if "_FillValue" in variable.ncattrs():
        options["fill_value"] = variable.getncattr("_FillValue")
    return options


def bulk_downloads(body):
    subids = body["subids"]

    rows = (
        get_app_session()
        .query(Outlet.code, Datafile.filename)
        .select_from(Timeseries)
        .join(Outlet, Outlet.id == Timeseries.outlet_id)
        .join(Datafile, Datafile.id == Timeseries.datafile_id)
        .join(Variable, Variable.id == Timeseries.variable_id)
        .join(Scenario, Scenario.id == Timeseries.scenario_id)
        .join(Model, Model.id == Timeseries.model_id)
        .filter(
            Outlet.code.in_(subids),
            Model.short_name == body["model"],
            Scenario.short_name == body["scenario"],
            Variable.standard_name == body["variable"],
        )
        .all()
    )
    outlets_by_file = {}
    for subid, filename in rows:
        outlets_by_file.setdefault(filename, set()).add(subid)
    requested = set(subids)
    filename = next(
        (
            filename
            for filename, available in sorted(outlets_by_file.items())
            if requested <= available
        ),
        None,
    )
    if filename is None:
        return {"detail": "No Datafile contains all requested subids."}, 422
    source_path = Path(filename).resolve()
    output_path = None
    try:
        with Dataset(source_path) as source:
            time = source.variables["time"]
            basin_name = source.variables["basin_name"]
            data = source.variables[body["variable"]]
            basin_indexes = basin_name_index_map_from_values(basin_name)
            selected = [basin_indexes[subid] for subid in subids]

            handle, output_path = tempfile.mkstemp(prefix="hms-bulk-", suffix=".nc")
            os.close(handle)
            with Dataset(output_path, "w", format="NETCDF4") as output:
                copy_attributes(source, output)
                output.createDimension("time", len(time))
                output.createDimension("outlet", len(subids))

                output_time = output.createVariable(
                    "time",
                    time.dtype,
                    ("time",),
                    **creation_options(time, (min(CHUNK_SIZE, len(time)),)),
                )
                copy_attributes(time, output_time)

                output_basin = output.createVariable("basin_name", str, ("outlet",))
                copy_attributes(basin_name, output_basin)
                output_basin[:] = np.asarray(subids, dtype=object)

                output_data = output.createVariable(
                    body["variable"],
                    data.dtype,
                    ("time", "outlet"),
                    **creation_options(
                        data,
                        (min(CHUNK_SIZE, len(time)), min(64, len(subids))),
                    ),
                )
                copy_attributes(data, output_data)

                time_first = data.dimensions[0] == "time"
                for start in range(0, len(time), CHUNK_SIZE):
                    stop = min(start + CHUNK_SIZE, len(time))
                    output_time[start:stop] = time[start:stop]
                    values = (
                        data[start:stop, selected]
                        if time_first
                        else data[selected, start:stop].T
                    )
                    output_data[start:stop, :] = values
    except Exception:
        if output_path and os.path.exists(output_path):
            os.unlink(output_path)
        raise

    download_name = f"{source_path.stem}_subset.nc"
    response = send_file(
        output_path,
        mimetype="application/x-netcdf",
        as_attachment=True,
        download_name=download_name,
        conditional=False,
    )
    response.call_on_close(lambda: os.unlink(output_path))
    return response
