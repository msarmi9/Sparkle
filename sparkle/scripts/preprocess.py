import os
import glob
import math
import numpy as np
import pandas as pd


def get_meta_info(df):
    """
    Create metadata df with columns = ["watchOnTwistHand", "n_pills", "pills_low"]
    """
    meta_df = df[["watchOnTwistHand", "n_pills"]].loc[[0]]
    # 1 if n_pills <= 10, 0 otherwise
    meta_df["pills_low"] = (meta_df["n_pills"] <= 10).astype(int)

    return meta_df


def rename_columns(df):
    """
    Rename columns.
    SensorLog's data comes in two different types of column names depending on Apple Watch version.
    """
    try:
        df = df[
            [
                "loggingSample(N)",
                "gyroRotationX(rad/s)",
                "gyroRotationY(rad/s)",
                "gyroRotationZ(rad/s)",
                "accelerometerAccelerationX(G)",
                "accelerometerAccelerationY(G)",
                "accelerometerAccelerationZ(G)",
                "avAudioRecorderPeakPower(dB)",
                "avAudioRecorderAveragePower(dB)",
            ]
        ]
    except:
        df = df[
            [
                "loggingSample",
                "gyroRotationX",
                "gyroRotationY",
                "gyroRotationZ",
                "accelerometerAccelerationX",
                "accelerometerAccelerationY",
                "accelerometerAccelerationZ",
                "avAudioRecorderPeakPower",
                "avAudioRecorderAveragePower",
            ]
        ]

    df.columns = [
        "loggingSample",
        "gyro_x",
        "gyro_y",
        "gyro_z",
        "accel_x",
        "accel_y",
        "accel_z",
        "audio_peak_power",
        "audio_average_power",
    ]
    return df


def trim_data(df, trim_start_pct, trim_end_pct):
    """
    Trim first 'trim_start_pct' and last 'trim_end_pct' of data.
    Ex) trim_data(df, 0.05, 0.05)
    """
    count = df.shape[0]
    new_start = math.floor(count * trim_start_pct)
    new_end = math.ceil(count * (1 - trim_end_pct))

    return df[new_start:new_end]


def window_data(df, n_windows):
    """
    Partition data into equal sized windows and assign 'window' id.
    'window' id ranges from 1 to n_windows.
    """
    df["window"] = pd.qcut(df["loggingSample"], n_windows, range(1, n_windows + 1))

    return df


def pivot_data(df):
    """
    Get 'mean', 'min', 'max', 'std' per window per column and pivot the entire data into a single row.
    Ex) Input df columns: ['loggingSample', 'gyro_x', 'gyro_y',.., 'audio_average_power', 'window']
    Output df columns: ['gyro_x_mean_1', 'gyro_x_mean_2',...,'audio_average_power_std_10']
    """
    df = df.groupby("window")[
        [
            "gyro_x",
            "gyro_y",
            "gyro_z",
            "accel_x",
            "accel_y",
            "accel_z",
            "audio_peak_power",
            "audio_average_power",
        ]
    ].agg(["mean", "min", "max", "std"])

    df.columns = ["_".join(col) for col in df.columns]
    df["temp"] = None  # need None column to use as an index for pivot
    df = df.reset_index()

    df = df.pivot(index="temp", columns="window").reset_index(drop=True)
    df.columns = [col[0] + "_" + str(col[1]) for col in df.columns]

    return df


def process_file(path):
    """
    Preprocess a raw data into a single row data and add meta data columns.s
    """
    df = pd.read_csv(path)

    meta_df = get_meta_info(df)

    df = rename_columns(df)
    df = trim_data(df, trim_start_pct=0.05, trim_end_pct=0.05)
    df = window_data(df, n_windows=10)
    df = pivot_data(df)

    return pd.concat([df, meta_df], axis=1)


def concat_files(paths, file_name):
    """
    Concatenates processed files from the paths into a single dataframe,
    and exports to csv
    """
    df = pd.DataFrame()
    for i, path in enumerate(paths):
        print(i)
        df = pd.concat([df, process_file(path)])
    df.to_csv("data/" + file_name + ".csv", index=False)

    return df
