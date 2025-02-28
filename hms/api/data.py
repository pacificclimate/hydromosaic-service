from hydromosaic.database import Outlet, Timeseries, Variable, Scenario, Model, Datafile
from netCDF4 import Dataset
from hms import get_app_session


def timeseries_data(subid, ts_id):
    """Return dummy data for now"""

    # Get the metadata from the database, build metadata table
    ts = get_app_session().query(Timeseries).filter_by(id=ts_id).one()
    var = get_app_session().query(Variable).filter_by(id=ts.variable_id).one()
    scen = get_app_session().query(Scenario).filter_by(id=ts.scenario_id).one()
    mod = get_app_session().query(Model).filter_by(id=ts.model_id).one()

    metadata = (
        f"Attribute, Value\n"
        f"Variable, {var.standard_name}\n"
        f"Outlet, {subid}\n"
        f"Scenario, {scen.short_name}\n"
        f"Model, {mod.short_name}\n"
        f"\n"
    )

    # Fetch data from netCDF file, build data table
    df = get_app_session().query(Datafile).filter_by(id=ts.datafile_id).one()
    nc = Dataset(df.filename)

    header = f"Time ({nc.variables['time'].units}), {var.standard_name} ({nc.variables[var.standard_name].units})\n"

    outlet_index = nc.variables["basin_name"][:].tolist().index(subid)
    timestamps = nc.variables["time"][:]
    data = nc.variables[var.standard_name][0 : len(timestamps), outlet_index]

    data_rows = [f"{timestamps[i]}, {data[i]}" for i in range(len(timestamps))]

    return metadata + header + "\n".join(data_rows)

    return """
Attribute, Value
Variable, q_in
Outlet, sub4008275
Scenario, rcp26
Model, CanESM2

time (hours since 1991-01-01 00:00:00), q_in (m**3 s**-1)
0, 0.000146036960985626
24, 0.0750794376526951
48, 9.148511994179339
72, 0.145543980219365
96, 0.142641812389788
120, 0.139802770939621
144, 0.137024598885108
"""
