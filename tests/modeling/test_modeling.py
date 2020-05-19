import numpy as np

from modeling.preprocessing import preprocess


def test_preprocess():
    path = "tests/data/2020-04-27_21_00_19_2.csv"
    X = preprocess(path, regression=True)
    assert type(X) == np.ndarray
    assert X[0][0] == -4.185989856719972
    assert X[0][19] == 0.16386624716216439
