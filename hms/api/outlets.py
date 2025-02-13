def list_outlets():
    """For now, return dummy data"""
    return [
        {"id": "sub4008275", "uri": "/outlets/sub4008275"},
        {"id": "sub4000665", "uri": "/outlets/sub4000665"},
        {"id": "sub4000732", "uri": "/outlets/sub4000732"},
        {"id": "sub4012087", "uri": "/outlets/sub4012087"},
        {"id": "sub4000652", "uri": "/outlets/sub4000652"},
        {"id": "sub4012058", "uri": "/outlets/sub4012058"},
        {"id": "sub4012102", "uri": "/outlets/sub4012102"},
        {"id": "sub4008291", "uri": "/outlets/sub4008291"},
        {"id": "sub4008124", "uri": "/outlets/sub4008124"},
        {"id": "sub4000740", "uri": "/outlets/sub4000740"},
        {"id": "sub4012067", "uri": "/outlets/sub4012067"},
        {"id": "sub4012070", "uri": "/outlets/sub4012070"},
    ]


def outlet(subid):
    """For now, return dummy data"""
    return {
        "id": "sub4008275",
        "uri": "/outlets/sub4008275",
        "timeseries": [
            {
                "id": "1",
                "uri": "/outlets/sub4008275/timeseries/1",
                "data_uri": "/outlets/sub4008275/timeseries/1/data",
                "variable": "q_in",
                "variable_uri": "/variables/q_in",
                "scenario": "rcp26",
                "model": "CanESM2",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "2",
                "uri": "/outlets/sub4008275/timeseries/2",
                "data_uri": "/outlets/sub4008275/timeseries/2/data",
                "variable": "q_sim",
                "variable_uri": "/variables/q_sim",
                "scenario": "rcp26",
                "model": "CanESM2",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "3",
                "uri": "/outlets/sub4008275/timeseries/3",
                "data_uri": "/outlets/sub4008275/timeseries/3/data",
                "variable": "q_obs",
                "variable_uri": "/variables/q_obs",
                "scenario": "rcp26",
                "model": "CanESM2",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "4",
                "uri": "/outlets/sub4008275/timeseries/4",
                "data_uri": "/outlets/sub4008275/timeseries/4/data",
                "variable": "q_in",
                "variable_uri": "/variables/q_in",
                "scenario": "rcp85",
                "model": "CanESM2",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "5",
                "uri": "/outlets/sub4008275/timeseries/5",
                "data_uri": "/outlets/sub4008275/timeseries/5/data",
                "variable": "q_sim",
                "variable_uri": "/variables/q_sim",
                "scenario": "rcp85",
                "model": "CanESM2",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "6",
                "uri": "/outlets/sub4008275/timeseries/6",
                "data_uri": "/outlets/sub4008275/timeseries/6/data",
                "variable": "q_obs",
                "variable_uri": "/variables/q_obs",
                "scenario": "rcp85",
                "model": "CanESM2",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "7",
                "uri": "/outlets/sub4008275/timeseries/7",
                "data_uri": "/outlets/sub4008275/timeseries/7/data",
                "variable": "q_in",
                "variable_uri": "/variables/q_in",
                "scenario": "rcp26",
                "model": "PCIC6",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "8",
                "uri": "/outlets/sub4008275/timeseries/8",
                "data_uri": "/outlets/sub4008275/timeseries/8/data",
                "variable": "q_sim",
                "variable_uri": "/variables/q_sim",
                "scenario": "rcp26",
                "model": "PCIC6",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "9",
                "uri": "/outlets/sub4008275/timeseries/9",
                "data_uri": "/outlets/sub4008275/timeseries/9/data",
                "variable": "q_obs",
                "variable_uri": "/variables/q_obs",
                "scenario": "rcp26",
                "model": "PCIC6",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "10",
                "uri": "/outlets/sub4008275/timeseries/10",
                "data_uri": "/outlets/sub4008275/timeseries/10/data",
                "variable": "q_in",
                "variable_uri": "/variables/q_in",
                "scenario": "rcp85",
                "model": "PCIC6",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "11",
                "uri": "/outlets/sub4008275/timeseries/11",
                "data_uri": "/outlets/sub4008275/timeseries/11/data",
                "variable": "q_sim",
                "variable_uri": "/variables/q_sim",
                "scenario": "rcp85",
                "model": "PCIC6",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
            {
                "id": "12",
                "uri": "/outlets/sub4008275/timeseries/12",
                "data_uri": "/outlets/sub4008275/timeseries/12/data",
                "variable": "q_obs",
                "variable_uri": "/variables/q_obs",
                "scenario": "rcp85",
                "model": "PCIC6",
                "start_time": "1991-01-01 00:00:00",
                "end_time": "2001-01-01 00:00:00",
                "num_times": 3653,
            },
        ],
    }
