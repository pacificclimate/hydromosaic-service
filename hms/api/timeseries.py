from hydromosaic.database import Outlet, Timeseries
from hms import get_app_session
from hms.api.json import timeseries_json


def list_timeseries(subid):
    """Return all timeseries associated with one outlet"""
    try:
        outlet = get_app_session().query(Outlet).filter_by(code=subid).one()
        timeseries = get_app_session().query(Timeseries).filter_by(outlet_id=outlet.id)
        return [timeseries_json(t, subid, True) for t in timeseries]
    except:
        return []


def timeseries(subid, ts_id):
    """Return detailed information describing one timeseries"""
    try:
        outlet = get_app_session().query(Outlet).filter_by(code=subid).one()
        timeseries = get_app_session().query(Timeseries).filter_by(id=ts_id).one()
        return timeseries_json(timeseries, subid, True)

    except:
        return {}


def timeseries_data(subid, ts_id):
    """Return dummy data for now"""
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
