from hydromosaic.database import Outlet, Timeseries, Variable, Scenario, Model
from hms import get_app_session


def timeseries_dict(ts, subid, include_outlet=False):
    """helper function that builds a timeseries dict from a Timeseries database object"""
    timeseries, variable_name, scenario_name, model_name = ts

    ts = {
        "id": timeseries.id,
        "uri": f"/outlets/{subid}/timeseries/{timeseries.id}",
        "data_uri": f"/outlets/{subid}/timeseries/{timeseries.id}/data",
        "variable": variable_name,
        "variable_uri": f"/variables/{variable_name}",
        "scenario": scenario_name,
        "model": model_name,
        "start_time": timeseries.start_time,
        "end_time": timeseries.end_time,
        "num_times": timeseries.num_times,
    }
    if include_outlet:
        ts["outlet"] = subid
        ts["outlet_uri"] = f"/outlets/{subid}"
    return ts


def timeseries_query():
    return (
        get_app_session()
        .query(Timeseries, Variable.standard_name, Scenario.short_name, Model.short_name)
        .join(Variable, Variable.id == Timeseries.variable_id)
        .join(Scenario, Scenario.id == Timeseries.scenario_id)
        .join(Model, Model.id == Timeseries.model_id)
    )


def list_outlets():
    """return a list with an object for each outlet in the database"""
    outlets = get_app_session().query(Outlet).all()

    return [{"id": o.code, "uri": f"/outlets/{o.code}"} for o in outlets]


def outlet(subid):
    """Return detailed data on one outlet"""
    try:
        outlet = get_app_session().query(Outlet).filter_by(code=subid).one()
        timeseries = timeseries_query().filter(Timeseries.outlet_id == outlet.id).all()
        return {
            "id": outlet.code,
            "uri": f"/outlets/{outlet.code}",
            "timeseries": [timeseries_dict(t, subid, False) for t in timeseries],
        }
    except:
        return {}


def list_timeseries(subid):
    """Return all timeseries associated with one outlet"""
    try:
        outlet = get_app_session().query(Outlet).filter_by(code=subid).one()
        timeseries = timeseries_query().filter(Timeseries.outlet_id == outlet.id).all()
        return [timeseries_dict(t, subid, True) for t in timeseries]
    except:
        return []


def timeseries(subid, ts_id):
    """Return detailed information describing one timeseries"""
    try:
        timeseries = (
            timeseries_query()
            .join(Outlet, Outlet.id == Timeseries.outlet_id)
            .filter(Outlet.code == subid, Timeseries.id == ts_id)
            .one()
        )
        return timeseries_dict(timeseries, subid, True)

    except:
        return {}
