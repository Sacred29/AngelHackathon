import pandas as pd
import re

def process_fares(text):
    pattern = r'[+-]?\d*\.\d+'
    match = re.search(pattern, text)
    if match:
        val = match.group()
        if val == '40.2':
            return '40.3'
        if val != '3.2':
            return val
        return '0'
    return None

def get_fare(type, distance):
    df = pd.read_csv("dataset/Fares_cleaned.csv")
    df = df[df['fare_type'] == fare_type[type]]

    # check max
    if distance >= float(df.iloc[-1]['distance']):
        return df.iloc[-1]['fare_per_ride']
    
    # iterate for fare range
    for index, row in df.iterrows():
        if distance < float(row['distance']):
            return df.iloc[index-1]['fare_per_ride']

fare_type = {
    0:"Adult card fare",
    1:"Senior citizen card fare",
    2:"Student card fare",
    3:"Workfare transport concession card fare",
    4:"Persons with diabilities card fare"
}

df = pd.read_csv("dataset/FaresforMRTandLRTEffectivefrom23December2023.csv")
df = df[df['applicable_time'] == 'All other timings'].drop('applicable_time', axis=1)
df['distance'] = df['distance'].apply(process_fares)
df.to_csv("dataset/Fares_cleaned.csv")
    
print(get_fare(0, 10))