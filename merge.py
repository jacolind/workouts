#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:08:07 2018

@author: j

merges the datasets in clean1 and clean2. 
creates some basic columns
"""

## Merge 

# assert they have the same cols 
assert set(df1.columns) == set(df2.columns)

# stack datasets on top of each other 
df = pd.concat([df1, df2])

# assert rows sum up
assert df.shape[0] == df1.shape[0] + df2.shape[0]


## Create variable: Chestday and Legday 

# Recall that Backday is created in clean1.py and clean2.py

# It is chestday if I have done any of these: Chest, Triceps
df['Chestday'] = ( (df['Chest'] == 1) +
                   (df['Triceps'] == 1) 
                  ) > 0
# It is legday if I have done any of these: Legsfront, Legsback, Calf.
df['Legday'] = ( df['Legsfront'] +
                 df['Legsback'] +
                 df['Ass']
                ) > 0

## create variable: Daycategory

# less than cardiothreshold minutes of cardio is merely warmup
cardiothreshold = 30

# function to go from binary variables to a categorical variable
def daycategorizer(row):
    if (row['Cardio_time'] > cardiothreshold) & (row['Muscles_time'] > 10):
        day = 'Cardio_and_Muscle'
    elif row['Cardio_time'] > cardiothreshold:
        day = 'Cardio'
    elif row['Chestday'] == True:
        day = 'Chest'
    elif row['Legday'] == True:
        day = 'Leg'
    elif row['Backday'] == True:
        day = 'Back'
    elif row['Yoga'] == 1:
        day = 'Yoga'
    else:
        day = 'Other' 
    return day

# go from binary variables to a categorical variable
df['Daycategory'] = df.apply(daycategorizer, axis=1)
df['Daycategory'] = df['Daycategory'].astype('category')

# remove vars we do not need 
df.drop(['Legday', 'Chestday', 'Backday'], inplace=True)

## create variable: Training_time

df['Training_time'] = df['Cardio_time'] + df['Muscles_time'] + df['Stretch_time']

## create variable: week

df['Week'] = df['Date'].dt.week
