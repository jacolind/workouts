#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 16:56:43 2018

@author: j

i dont think do2 will work. 
i will import training.2 csv and clean that
"""

## packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns

## import data

# cd to folder /Documents/python/trainingdata/

file = 'data/Traaining.2_1.csv' #fake file
df2_raw = pd.read_csv(file, parse_dates=True) 
df2 = df2_raw

## clean data 

# basic cleaning 
df2.rename(columns={'date':'Date'}, inplace=True)
df2.Date = pd.to_datetime(df.Date)
cols_drop = ['#', 'Start Date (UTC)', 'Network ID']
df2.drop(cols_drop, axis=1, inplace=True)

# binarize the Muscles column 
dict_rename = {'Baksida lÃ¥r':'Legsback', 'Bröst':'Chest', 
               'Framsida lÃ¥r':'Legsfront', 'Vader':'Calf', 
               'Rumpa':'Ass', 'Axlar':'Shoulders'}
# todo: change the entries in my form so that it is in english instead?
muscles = df2.Muscles.str.get_dummies(sep=' / ')
muscles.rename(columns=dict_rename, inplace=True)
df2.drop('Muscles', axis=1, inplace=True)
df2 = pd.concat([df2, muscles], axis=1)
df2.columns # check 

######################################################################

## Chestday Legday Backday

# It is chestday if I have done any of these: Chest, Triceps
df2['Chestday'] = ( (df2['Chest'] == 1) +
                   (df2['Triceps'] == 1) 
                  ) > 0

# It is legday if I have done any of these: Legsfront, Legsback, Calf.
df2['Legday'] = ( df2['Legsfront'] +
                 df2['Legsback'] +
                 df2['Ass']
                ) > 0

# It is legday if I have done any of these: Deltoid, lats, spine
df2['Backday'] = ( df2['Deltoid'] +
                 df2['Lats'] +
                 df2['Spine']
                ) > 0


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
        day = 'Other' #
    return day

# go from binary variables to a categorical variable
df2['Daycategory'] = df2.apply(daycategorizer, axis=1)
# type is categorical
df2['Daycategory'] = df2['Daycategory'].astype('category')


## create variable: Training_time
# same as in do1.py

print(df2.Daycategory.value_counts())

# cols in one df not the other 
set(df.columns) - set(df2.columns)
set(df2.columns) - set(df.columns)
# cols in df AND df2
len(set(df.columns) & set(df2.columns))
len(df2.columns)

## merge the two 

# now they have the same columns and can be merged