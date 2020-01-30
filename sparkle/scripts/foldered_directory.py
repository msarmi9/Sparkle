#!/usr/bin/env python
# coding: utf-8
# author: Stephanie Jung
import os
import glob
import pandas as pd


# Designate your own data folder path
data_path = '/Users/stephj/Desktop/git/sparkle/pills-data'

# Designate the output folder path to be created
output_path = '/Users/stephj/Desktop/git/sparkle/foldered_all'

# Subject metadata file
metadata = '/Users/stephj/Desktop/git/sparkle/subjects-metadata.csv'


def merge_metadata_to_foldered_directory(data_path=data_path, output_path=output_path, metadata=metadata):
    """Add pid and npills columns to each csv,
    merges with subject metadata, 
    and saves each csv file to a hierarchical directory.
    
    Returns:
    csv files of sensor data with subject metadata
    """

    # Create a new folder for the output
    os.mkdir(output_path)

    df_subject = pd.read_csv(metadata)

    # Get all the sub-folders in 'pills-data' folder.
    # The sensor data is stored in a directory structure.
    folders = sorted(glob.glob(data_path+'/*'))

    for i, pid_folder in enumerate(folders, 1):
        
        # create subdirectories with each pid. ex) /01-pid, /02-pid..
        pid_path = output_path+'/'+'%02d'%i+'-pid'
        os.mkdir(pid_path)

        pills_folders = sorted(glob.glob(pid_folder+'/*'))
        for pills_folder in pills_folders:
            
            # create subdirectories with each number of pills. ex) /00-pills
            npill = pills_folder.split('/')[-1]
            pills_path = pid_path+'/'+npill
            os.mkdir(pills_path)

            data = sorted(glob.glob(pills_folder+'/*'))
            for i, f in enumerate(data, 1):
                trial_no = '%02d'%i
                df_trial = pd.read_csv(f)
                pid = int(f.split('/')[-3].split('-')[-2])
                n_pills = int(f.split('/')[-2].split('-')[-2])
                df_trial['pid'] = pid
                df_trial['n_pills'] = n_pills
                df_trial = pd.merge(df_trial, df_subject, on='pid')
                
                # if the subject's watch_hand is their twist_hand, ['watchOnTwistHand'] -> 1. otherwise -> 0.
                df_trial['watchOnTwistHand'] = 0
                df_trial.loc[df_trial['watch_hand']==df_trial['twist_hand'], 'watchOnTwistHand'] = 1
                
                # output file directory : /foldered_all/01-pid/00-pills/trial01.csv
                df_trial.to_csv(pills_path+'/trial'+trial_no+'.csv')

if __name__ == "__main__":
    merge_metadata_to_foldered_directory(data_path, output_path, metadata)

