"""
Note: This is an updated test to reflect a direct test of preprocess. 
"""
from modeling.preprocessing import *

def test_preprocess():
	path = 'tests/modeling/2020-04-27_21_00_19_2.csv'
	X = preprocess(path, regression=True)
	assert type(X) == np.ndarray
	assert X[0][0] == -4.185989856719972
	assert X[0][19] == 0.16386624716216439
