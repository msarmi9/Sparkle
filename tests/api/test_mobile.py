"""
Tests api for communicating with mobile clients.
"""
import json

import pytest


@pytest.fixture(scope="module")
def sensor_json():
    """Return a sample json file of watch sensor data sent by the mobile app."""
    test_file = "tests/data/2020-04-27_21_00_19_2.csv"
    with open(test_file, "r") as f:
        sensor_data = f.read()

    keys = ["id", "s3_url", "recording_data", "on_time", "timestamp"]
    values = ["-1", "s3", sensor_data, "0", "2999-12-31_11:59:59"]
    return dict(zip(keys, values))


def test_send_data(client, sensor_json):
    """API receives mobile json data and returns json response."""
    response = client.post("/send-data", json=sensor_json)
    pred_dict = json.loads(response.data)
    assert response.status_code == 200
    assert all(key in pred_dict.keys() for key in {"pred_string", "pred_type", "pred"})
