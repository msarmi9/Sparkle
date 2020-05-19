"""
Tests api for communicating with mobile clients.
"""

test_file = "tests/modeling/2020-04-27_21_00_19_2.csv"
with open(test_file, "r") as f:
    sensor_data = f.read()

json_input = {
    "id": "-1",
    "s3_url": "foo33",
    "recording_data": sensor_data,
    "on_time": "0",
    "timestamp": "2999-12-31_11:59:59",
}


def test_send_data(client):
    """API receives mobile json data and returns json response."""
    rv = client.post("/send-data", json=json_input)
