#!/usr/bin/env python
# coding: utf-8
import os
import glob
import math

import numpy as np
import pandas as pd

# point this to your local data directory (data not on Github)
paths = glob.glob('new_data/*')
paths = sorted(paths)[1:]
paths



def getMetaInfo(df):
    
    meta_df = df[["watchOnTwistHand", "n_pills"]].loc[[0]]
    meta_df["pills_low"] = (meta_df["n_pills"] <= 10).astype(int)
    
    return meta_df


def renameColumns(df):
    try:
        df = df[['loggingSample(N)', 
                'gyroRotationX(rad/s)',
                'gyroRotationY(rad/s)',
                'gyroRotationZ(rad/s)',                       
                'avAudioRecorderPeakPower(dB)',
                'avAudioRecorderAveragePower(dB)']]
    except:
        df = df[['loggingSample', 
                 'gyroRotationX',
                 'gyroRotationY',
                 'gyroRotationZ', 
                 'avAudioRecorderPeakPower',
                 'avAudioRecorderAveragePower']]
        
    df.columns = ['loggingSample',
                   'gyro_x',
                   'gyro_y',
                   'gyro_z',
                   'audio_peak_power',
                   'audio_average_power']
    return df


def trimData(df, trim_start_pct, trim_end_pct):
    
    count = df.shape[0]
    new_start = math.floor(count * trim_start_pct)
    new_end = math.ceil(count * (1 - trim_end_pct))
    
    return df[new_start:new_end]


def windowData(df, n_windows):
    
    df["window"] = pd.qcut(df["loggingSample"], 
                           n_windows, 
                           range(1,n_windows+1))
    
    return df


def pivotData(df):
    
    df = df.groupby('window')[["gyro_x", "gyro_y", "gyro_z", 
                    "audio_peak_power","audio_average_power"]]\
                    .agg(["mean", "min", "max", "std"])
    
    df.columns = ["_".join(col).strip() for col in df.columns.values]
    df["temp"] = None
    df = df.reset_index()
    
    df = df.pivot("temp", "window").reset_index(drop=True)
    df.columns = [col[0] + "_" + str(col[1]) for col in df.columns.values]
    
    return df


def processFile(path):
    
    df = pd.read_csv(path)
    
    meta_df = getMetaInfo(df)
    
    df = renameColumns(df)
    df = trimData(df, trim_start_pct=0.05, trim_end_pct=0.05)
    df = windowData(df, n_windows=30)
    df = pivotData(df)
    
    return pd.concat([df, meta_df], axis=1)   



processed_df = pd.DataFrame()

for i, path in enumerate(paths):
    print(i)
    processed_df = pd.concat([processed_df, processFile(path)])


processed_df = processed_df.reset_index(drop=True)
assert processed_df.isna().values.any() == False

# processed_df is ready for modeling

