from hydromosaic.database import Outlet, Timeseries
from hms import get_app_session


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
