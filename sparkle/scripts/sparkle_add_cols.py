#!/usr/bin/env python
# coding: utf-8

import os
import glob
import pandas as pd

# Designate your own data folder path
path = "/Users/stephj/Desktop/git/sparkle/pills-data"
output_path = "/Users/stephj/Desktop/git/sparkle/pills_all_data"

# Create a new folder for the output
os.mkdir(output_path)
folders = sorted(glob.glob(path + "/*"))


# subjects data including handedness
subject_df = pd.read_csv("/Users/stephj/Desktop/git/sparkle/subjects-metadata.csv")


# Add pid and npills columns to csv -> create new .csv
# clean up later
for i, pid_folder in enumerate(folders, 1):
    pid_path = output_path + "/" + "%02d" % i + "-pid"
    # os.mkdir(pid_path)
    pills_folders = sorted(glob.glob(pid_folder + "/*"))
    for pills_folder in pills_folders:
        npill = pills_folder.split("/")[-1]
        pills_path = pid_path + "/" + npill
        # os.mkdir(pills_path)
        data = sorted(glob.glob(pills_folder + "/*"))
        for i, f in enumerate(data, 1):
            trial_no = "%02d" % i
            df = pd.read_csv(f)
            pid = int(f.split("/")[-3].split("-")[-2])
            n_pills = int(f.split("/")[-2].split("-")[-2])
            df["pid"] = pid
            df["n_pills"] = n_pills
            df = pd.merge(df, subject_df, on="pid")
            df["watchOnTwistHand"] = 0
            df.loc[df["watch_hand"] == df["twist_hand"], "watchOnTwistHand"] = 1
            df.to_csv(f"{output_path}/pills-{pid:>02}-{n_pills:>02}-{trial_no:>02}.csv")
