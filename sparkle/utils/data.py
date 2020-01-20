import time

def renameColumns(df):
    
    df_renamed = None
    
    try:
        
        df = df.select('loggingSample(N)', 
                        'gyroRotationX(rad/s)',
                        'gyroRotationY(rad/s)',
                        'gyroRotationZ(rad/s)',                       
                        'avAudioRecorderPeakPower(dB)',
                        'avAudioRecorderAveragePower(dB)')
    except:
        df = df.select('loggingSample', 
                       'gyroRotationX',
                       'gyroRotationY',
                       'gyroRotationZ', 
                       'avAudioRecorderPeakPower',
                       'avAudioRecorderAveragePower')
                        
    renamed_df = df.toDF('loggingSample',
                         'gyro_x',
                         'gyro_y',
                         'gyro_z',
                         'audio_peak_power',
                         'audio_average_power')
    return renamed_df


def trimData(df, trim_start, trim_end):
    
    count = df.count()
    start_sample = math.ceil(count * trim_start)
    end_sample = math.ceil(count * (1 - trim_end))

    trimmed_df = df.where(f"loggingSample > {start_sample} and loggingSample < {end_sample}")
    trimmed_df = trimmed_df.withColumn("loggingSampleAdjusted", trimmed_df["loggingSample"] - start_sample)
    trimmed_df = trimmed_df.drop("loggingSample").withColumnRenamed("loggingSampleAdjusted","loggingSample")
    return trimmed_df
    
def windowData(df, num_windows):
    count = df.count()
    df = df.where(f"loggingSample < {count}")
    window_size = count / num_windows
    label_window = udf(lambda x : int(x // window_size), IntegerType())
    windowed_df = df.select(label_window('loggingSample'),
                           'loggingSample',
                           'gyro_x',
                           'gyro_y',
                           'gyro_z',
                           'audio_peak_power',
                           'audio_average_power'
                          )
    windowed_df = windowed_df.withColumnRenamed("<lambda>(loggingSample)", "window")
    return windowed_df
    
def transformData(df):
    
    df = df.withColumn("foo", lit("foo"))
    transformed_df = df.groupBy("foo").pivot("window").agg(
                                              min('gyro_x'),
                                              max('gyro_x'), 
                                              avg('gyro_x'), 
                                              stddev('gyro_x'),
                                              min('gyro_y'),
                                              max('gyro_y'), 
                                              avg('gyro_y'), 
                                              stddev('gyro_y'),
                                              min('gyro_z'),
                                              max('gyro_z'), 
                                              avg('gyro_z'), 
                                              stddev('gyro_z'),
                                              min('audio_peak_power'),
                                              max('audio_peak_power'), 
                                              avg('audio_peak_power'), 
                                              stddev('audio_peak_power'),
                                              min('audio_average_power'),
                                              max('audio_average_power'), 
                                              avg('audio_average_power'), 
                                              stddev('audio_average_power'),
                                             ).drop('foo')
    
    renamed_columns = [c.replace("(","_").replace(")","_") for c in transformed_df.columns]
    final_df = transformed_df.toDF(*renamed_columns)
    
    return final_df

def appendMetaInfo(df, tdf):
    
    n_pills, watchOnTwistHand = df.select('n_pills', 'watchOnTwistHand').first()[:]
    tdf = tdf.withColumn('n_pills', lit(n_pills)).withColumn('watchOnTwistHand', lit(watchOnTwistHand))
    return tdf


def preprocess(df, trim_start=0.05, trim_end=0.10, num_windows=5):
        
    # Select out and rename columns of interest
    renamed_df = renameColumns(df)
    
    # Trim off ends of data
    trimmed_df = trimData(renamed_df, trim_start, trim_end)

    # Window data by labeling rows with window assignments 
    windowed_df = windowData(trimmed_df, num_windows)
    
    # Transform from long to wide with summarized statistics
    transformed_df = transformData(windowed_df)
    
    # Append a feature and the data's label to the row
    final_df = appendMetaInfo(df, transformed_df)
    
    return final_df



def get_full_frame(paths):
    start = time.time()
    for i, path in enumerate(paths):
        if i == 0:
            df = ss.read.csv(path, header=True, inferSchema=True)
            full_df = preprocess(df)
        else:
            df = ss.read.csv(path, header=True, inferSchema=True)
            full_df = full_df.union(preprocess(df))
        print(i)
    print(time.time() - start)
    return full_df