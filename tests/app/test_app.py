"""
Note: in order to test our database with a gh action,
we will have to get fancy.
"""
from app.routes import adherence_model


def test_adherence_model():
    data = "x,y,z\n1,2,3\n4,5,6"
    model_output = adherence_model(data)
    assert model_output.get("pred_string") is not None
    assert model_output.get("pred") is not None
    assert model_output["pred_string"] == "You just took your medication!"
    assert model_output["pred"] == 3.5
