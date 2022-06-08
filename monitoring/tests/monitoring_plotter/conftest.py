from pytest import fixture


@fixture
def mock_ps_monitoring_data():
    return {
        "id": [0, 2, 5, 6, 8],
        "pid": [1, 1, 1, 1, 1],
        "user": ["cassand+", "cassand+", "cassand+", "cassand+", "cassand+"],
        "pr": [20, 20, 20, 20, 20],
        "ni": [0, 0, 0, 0, 0],
        "virt": [2915196, 2915196, 2915196, 2915196, 2915196],
        "res": ["1.2g", "1.2g", "1.2g", "1.2g", "1.2g"],
        "shr": [24708, 24708, 24708, 24708, 24708],
        "s": ["S", "S", "S", "S", "S"],
        "cpu": [20.0, 21.0, 37.0, 41.0, 17.0],
        "mem": [3.9, 5.9, 13.1, 30.5, 45.0],
        "time": ["1:45.58", "1:45.61", "1:45.64", "1:45.66", "1:45.68"],
        "command": ["java", "java", "java", "java", "java"],
        "timestamp": [
            "07-06-2022 09:10:05_534943",
            "07-06-2022 09:12:06_786421",
            "07-06-2022 09:50:08_045620",
            "07-06-2022 10:10:09_302488",
            "07-06-2022 10:23:10_553379",
        ],
        "container_id": ["mycassandra1", "mycassandra1", "mycassandra1", "mycassandra1", "mycassandra1"],
    }
