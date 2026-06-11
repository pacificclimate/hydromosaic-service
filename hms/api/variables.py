from hydromosaic.database import Variable
from hms import get_app_session


def list_variables():
    """return a list with an object for each variable in the database"""
    vars = (
        get_app_session()
        .query(Variable.standard_name, Variable.units, Variable.long_name)
        .all()
    )

    return [
        {
            "id": standard_name,
            "uri": f"/variables/{standard_name}",
            "units": units,
            "long_name": long_name,
        }
        for standard_name, units, long_name in vars
    ]


def variable(v_id):
    """Return an object representing the requested variable"""

    try:
        standard_name, units, long_name = (
            get_app_session()
            .query(Variable.standard_name, Variable.units, Variable.long_name)
            .filter_by(standard_name=v_id)
            .one()
        )

        return {
            "id": standard_name,
            "uri": f"/variables/{standard_name}",
            "units": units,
            "long_name": long_name,
        }
    except:
        return {}
