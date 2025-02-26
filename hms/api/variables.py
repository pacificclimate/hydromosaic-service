from hydromosaic.database import Variable
from hms import get_app_session


def list_variables():
    """return a list with an object for each variable in the database"""
    vars = get_app_session().query(Variable).all()

    return [
        {
            "id": v.standard_name,
            "uri": f"/variables/{v.standard_name}",
            "units": v.units,
            "long_name": v.long_name,
        }
        for v in vars
    ]


def variable(v_id):
    """Return an object representing the requested variable"""

    try:
        var = get_app_session().query(Variable).filter_by(standard_name=v_id).one()

        return {
            "id": var.standard_name,
            "uri": f"/variables/{var.standard_name}",
            "units": var.units,
            "long_name": var.long_name,
        }
    except:
        return {}
