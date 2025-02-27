from hydromosaic.database import Outlet, Timeseries, Variable, Scenario, Model
from hms import get_app_session


def timeseries_dict(ts, subid, include_outlet=False):
    """helper function that builds a timeseries dict from a Timeseries database object"""
    var = get_app_session().query(Variable).filter_by(id=ts.variable_id).one()
    scen = get_app_session().query(Scenario).filter_by(id=ts.scenario_id).one()
    mod = get_app_session().query(Model).filter_by(id=ts.model_id).one()

    ts = {
        "id": ts.id,
        "uri": f"/outlets/{subid}/timeseries/{ts.id}",
        "data_uri": f"/outlets/{subid}/timeseries/{ts.id}/data",
        "variable": var.standard_name,
        "variable_uri": f"/variables/{var.standard_name}",
        "scenario": scen.short_name,
        "model": mod.short_name,
        "start_time": ts.start_time,
        "end_time": ts.end_time,
        "num_times": ts.num_times,
    }
    if include_outlet:
        ts["outlet"] = subid
        ts["outlet_uri"] = f"/outlets/{subid}"
    return ts


def list_outlets():
    """return a list with an object for each outlet in the database"""
    outlets = get_app_session().query(Outlet).all()

    return [{"id": o.code, "uri": f"/outlets/{o.code}"} for o in outlets]


def outlet(subid):
    """Return detailed data on one outlet"""
    try:
        outlet = get_app_session().query(Outlet).filter_by(code=subid).one()
        timeseries = get_app_session().query(Timeseries).filter_by(outlet_id=outlet.id)
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
        timeseries = get_app_session().query(Timeseries).filter_by(outlet_id=outlet.id)
        return [timeseries_dict(t, subid, True) for t in timeseries]
    except:
        return []


def timeseries(subid, ts_id):
    """Return detailed information describing one timeseries"""
    try:
        outlet = get_app_session().query(Outlet).filter_by(code=subid).one()
        timeseries = get_app_session().query(Timeseries).filter_by(id=ts_id).one()
        return timeseries_dict(timeseries, subid, True)

    except:
        return {}
