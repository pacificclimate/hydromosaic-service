def list_variables():
    """For now, return dummy values"""
    return [
        {
            "id": "q_in",
            "uri": "/variables/q_in",
            "units": "m**3 s**-1",
            "long_name": "Simulated reservoir inflows",
        },
        {
            "id": "q_sim",
            "uri": "/variables/q_sim",
            "units": "m**3 s**-1",
            "long_name": "Simulated outflows",
        },
        {
            "id": "q_in",
            "uri": "/variables/q_obs",
            "units": "m**3 s**-1",
            "long_name": "Observed outflows",
        },
    ]


def variable(v_id):
    """For now, return dummy values"""
    return {
        "id": "q_in",
        "uri": "/variables/q_in",
        "units": "m**3 s**-1",
        "long_name": "Simulated reservoir inflows",
    }
