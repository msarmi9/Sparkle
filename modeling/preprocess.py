import math

import numpy as np
import pandas as pd

import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel

import xgboost as xgb


def initializeDf(raw_sensor_data):
    """
    Loads the raw sensor data into a Pandas dataframe.
    """
    df = pd.read_csv(raw_sensor_data).reset_index()

    return df


def renameColumns(df):
    """
    Rename columns through override to a standardized set needed for following transformation.
    """
    df.columns = [
        "loggingSample",
        "accel_x",
        "accel_y",
        "accel_z",
        "gyro_x",
        "gyro_y",
        "gyro_z",
    ]
    return df


def trimData(df, trim_start_pct, trim_end_pct):
    """
    Trim the first 'trim_start_pct' and last 'trim_end_pct' off of the data, as this is noise.
    Ex) trim_data(df, 0.05, 0.05)
    """
    count = df.shape[0]
    new_start = math.floor(count * trim_start_pct)
    new_end = math.ceil(count * (1 - trim_end_pct))

    return df[new_start:new_end]


def windowData(df, n_windows):
    """
    Partition data into equal sized windows and assign 'window' id.
    'window' id ranges from 1 to n_windows.
    """
    df["window"] = pd.qcut(df["loggingSample"], n_windows, range(1, n_windows + 1))

    return df


def pivotData(df):
    """
    Get 'median', 'min', 'max', 'std' per window per column and pivot the entire data into a single row.
    Ex) Input df columns: ['loggingSample', 'gyro_x', 'gyro_y',.., 'window']
    Output df columns: ['gyro_x_median_1', 'gyro_x_median_2',...]
    """
    df = df.groupby("window")[
        ["gyro_x", "gyro_y", "gyro_z", "accel_x", "accel_y", "accel_z"]
    ].agg(["median", "min", "max", "std"])

    df.columns = ["_".join(col).strip() for col in df.columns.values]
    df["temp"] = None
    df = df.reset_index()

    df = df.pivot("temp", "window").reset_index(drop=True)
    df.columns = [col[0] + "_" + str(col[1]) for col in df.columns.values]

    return df


def selectScaleFeatures(df):
    """
	Loads pre-fit standard scaler and selection objects and applies to input.
	This casts the dataframe as a numpy array, applies the scaler, then applies feature selection. 
	The output an array of numeric features ready for XGB model usage. 
	"""
    # apply a pre-fit standard scaler scaling to data
    ss = pickle.load(open("ss.pkl", "rb"))
    X_scaled = ss.transform(df.to_numpy())

    # select the top features according to previous analysis
    select = pickle.load(open("selection.pkl", "rb"))
    X_select = select.transform(X_scaled)

    return X_select


def preprocess(raw_sensor_data, trim_start_pct=0.05, trim_end_pct=0.05, n_windows=5):

    df = initializeDf(raw_sensor_data)
    df = renameColumns(df)
    df = trimData(df, trim_start_pct=trim_start_pct, trim_end_pct=trim_end_pct)
    df = windowData(df, n_windows=n_windows)
    df = pivotData(df)
    X = selectScaleFeatures(df)
    return X
