# helper functions for APIs - they converstion database objects to
# JSON objects for return
from hydromosaic.database import Timeseries, Variable, Scenario, Model
from hms import get_app_session


def timeseries_json(ts, subid, include_outlet=False):
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
