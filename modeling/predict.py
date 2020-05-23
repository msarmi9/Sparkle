"""
Models for predicting medication adherence from smartwatch sensor data.

Models take as input strings of sensor data recorded by a smartwatch and output:
    1. A prediction for whether the activity is pill-taking (1) or not (0).
    2. If an activity is classified as pill-taking, a prediction for the number of pills
    present in the prescription bottle at the time the recording was made.
"""
import io
import pickle

from modeling.preprocessing import preprocess


def adherence_model(data):
    """Predict the number of pills remaining given a string of sensor data."""
    classifier_path = "modeling/models/classifier.pkl"
    regressor_path = "modeling/models/regressor.pkl"

    # run the pill classifier process
    X = preprocess(io.StringIO(data), regression=False)
    classifier = pickle.load(open(classifier_path, "rb"))
    classifier_pred = classifier.predict(X).item()

    if classifier_pred == 0:
        pred_string = "It does not appear you took any medication."
        return {
            "pred_string": pred_string,
            "pred_type": "classification",
            "pred": classifier_pred,
        }
    else:
        # run the regression process
        X = preprocess(io.StringIO(data), regression=True)

        regressor = pickle.load(open(regressor_path, "rb"))
        predicted_pills = regressor.predict(X).round().item()
        predicted_pills = max(min(predicted_pills, 30), 1)

        pred_string = f"It looks like you have {predicted_pills - 1} pills remaining."
        return {
            "pred_string": pred_string,
            "pred_type": "regression",
            "pred": predicted_pills,
        }
