from hydromosaic.database import Outlet, Timeseries, Variable, Scenario, Model, Datafile
from netCDF4 import Dataset
from hms import get_app_session
from datetime import datetime, timedelta


def time_string(reference, hours):
	return (reference + timedelta(hours = hours)).strftime("%Y-%m-%d %H:%M:%S")
	

def timeseries_data(subid, ts_id):
    """Return a timeseries in CSV format, one metadata table and one timeseries table"""

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

    header = f"Time, {var.standard_name} ({nc.variables[var.standard_name].units})\n"

    outlet_index = nc.variables["basin_name"][:].tolist().index(subid)
    reference_time = datetime.strptime(nc.variables['time'].units, "hours since %Y-%m-%d %H:%M:%S")
    timestamps = [time_string(reference_time, t) for t in nc.variables["time"][:]]
    data = nc.variables[var.standard_name][0 : len(timestamps), outlet_index]

    data_rows = [f"{timestamps[i]}, {data[i]}" for i in range(len(timestamps))]

    return metadata + header + "\n".join(data_rows)
