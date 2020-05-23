"""
Tests for gauging the predictive ability of trained adherence models.
"""
from pathlib import Path

import numpy as np
import pytest

from modeling.predict import adherence_model


# Paths to training records of pill-taking data
train_path_01 = Path("tests/data/train/2020-04-21_07_51_17_1.csv")
train_path_02 = Path("tests/data/train/2020-04-27_21_00_19_2.csv")
train_paths = [train_path_01, train_path_02]

# Paths to holdout records of pill-taking data
test_path_01 = Path("")

# Paths to non-pill taking activities
path_at_rest = Path("tests/data/non-pill/2020-04-21_09_11_37_at_rest.csv")


# Adherence model requires string data, since that's how data is streamed from the watch
def get_csv_string(path_to_csv):
    """Return a csv file as a string."""
    with open(path_to_csv, "r") as f:
        return f.read()


def get_label_from_path(csv_path):
    """Return the substring after the last underscore in a path as an int."""
    return int(csv_path.name.rstrip(".csv").split("_")[-1])


class TestAdherenceModel:
    """Tests model can both learn from training data and predict well on unseen data."""

    @pytest.mark.parametrize("train_path", train_paths)
    def test_classifier_on_training_data(self, train_path):
        """Model classifies activity as pill-taking for recorded pill intake data."""
        data = get_csv_string(train_path)
        pred_dict = adherence_model(data)
        assert pred_dict["pred_type"] == "regression"

    @pytest.mark.parametrize("train_path", train_paths)
    def test_regressor_on_training_data(self, train_path, mae_tol=1):
        """Model predicts number of pills remaining within a given MAE tol."""
        data = get_csv_string(train_path)
        label = get_label_from_path(train_path)
        pred_dict = adherence_model(data)
        assert np.abs(pred_dict["pred"] - label) <= mae_tol

    def test_classifier_on_data_at_rest(self):
        """Classifier classifies data of a hand at rest as non-pill-taking activity."""
        data = get_csv_string(path_at_rest)
        pred_dict = adherence_model(data)
        assert pred_dict["pred"] == 0
        assert pred_dict["pred_type"] == "classification"
