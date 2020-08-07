''' gRPC Server for TimescaleDB '''
# TODO > Fill out the author details in the right format.

import pandas as pd


'''
Clean the CSV File using a Pandas Dataframe
'''
# Directly import the local CSV file as type String
df = pd.read_csv(f"meterusage.csv", dtype=str)
# Confirm dataframe created, its shape and the meterusage column's type
print(df)
print(df.shape)
print(df.meterusage.describe())
# Change the meterusage datatype to float and convert errors to NaN
df['meterusage'] = df['meterusage'].apply(pd.to_numeric, errors='coerce', downcast='float')
# Drop any rows containing NaN and reset the frame's index
df = df.dropna()
df = df.reset_index(drop=True)
# Confirm its shape and the meterusage column's type has changed
print(df)
print(df.shape)
print(df.meterusage.describe())

# TODO - convert the time colum into 'time' format.