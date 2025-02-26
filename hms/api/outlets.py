from hydromosaic.database import Outlet, Timeseries
from hms import get_app_session
from hms.api.json import timeseries_json


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
            "timeseries": [timeseries_json(t, subid) for t in timeseries],
        }
    except:
        return {}
