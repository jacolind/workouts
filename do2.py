#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 12:06:57 2018

@author: j

like do1.py but allows for different back excerxises:
lats, deltoid, spine - instead of rygg. 
however I need to set = np.na before a certain date, 
and after that date have the new cols. 
sript is not run - untested!
"""

## about

'''
Data comes from my training log.
Search for "concl:" in order to find actionable insights
'''

## directory

### import data

# packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# cd to folder /Documents/python/trainingdata/
df_raw = pd.read_csv('data/Traaining.1.csv', parse_dates=True)

# todo: import automatically using https://github.com/underdogio/typeform

### clean data 

# Remove test entries
# first real training date is 2017-01-17 on row 3. entries 0:2 are tests
df = df_raw.drop(df_raw.tail(3).index)
# nr of workouts
n = df.shape[0]

## rename columns

# todo: change the list below based on df.columns printout
# it needs to be in a certain order since I don't do ".map" merely write over df.columns
colnames = ['IDnumber', 'Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Biceps', 'Chest', 'Shoulders', 'Triceps', 'Other', 
       'Lats', 'Deltoid', 'Spine', # the new cols instead of 'Back'
       'Muscles_time', 'Stretch_time', 'Notes',
       'StartDate(TC)', 'SubmitDate(TC)', 'NetworkID']
df.columns = colnames

# convert date dtype 
df.Date = pd.to_datetime(df.Date)

## keep only some columns

keepcols = ['Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Biceps', 'Chest', 'Shoulders', 'Triceps', 'Other', 
       'Lats', 'Deltoid', 'Spine', #new cols
       'Muscles_time', 'Stretch_time', 'Notes']
df = df[keepcols]

## Create binary variables and recode NaN

# map binaryvars from not NaN to 1.
binaryvars = ['Legsfront', 'Legsback', 'Ass', 'Calf', 
              'Lats', 'Deltoid', 'Spine',
             'Biceps', 'Chest', 'Shoulders', 'Triceps']
df[binaryvars] = df[binaryvars].notnull().astype(int)
# map from NaN to 0. this affects e.g. Cardio_time, Other and Notes.
df.fillna(0, inplace=True)

##  Explanation of why I need to create these varaibles

'''
From df.head() we see 'Chest'='NaN' when I have not trained my chest,
and 'Chest'='Bröst' when I have trained chest (bröst is swedish for chest).
df.info() reveals the same problem: dtype=objects but I want dtype=float64
Hence we must map from 'NaN' to 0, and from 'some-text-not-NaN' to 1.

Why did this problem occur? 
In typeform I have a multiple choice question,
apparently when downloading to csv each choice is converted to a variable.
'''

## Chestday vs Legday

# It is chestday if I have done any of these: Chest, Triceps
df['Chestday'] = ( (df['Chest'] == 1)   |
                   (df['Triceps'] == 1)
                  )
# It is legday if I have done any of these: Legsfront, Legsback, Calf.
df['Legday'] = ( df['Legsfront'] +
                 df['Legsback'] + 
                 df['Ass']
                ) > 0

df['Backday'] = ( df['Lats'] +
                 df['Deltoid'] + 
                 df['Spine']
                ) > 0

# mutually exclusive
# there are rows with both Leg day and chest day.
chest_and_legday = df[(df['Chestday'] == True) 
                        & (df['Legday'] == True)
                        ].count().sum()
assert chest_and_legday == 0

# collectively exhaustive? no
# some days are only yoga / cardio / back, not legs / chest.
assert 0 < df[(df['Chestday'] == False) 
              & (df['Legday'] == False)].count().sum()

# chestday and backday (will probably not happen)
df[(df['Chestday'] == True) & (df['Backday'] == True)].count().sum()
# legday and backday  (might happen)
df[(df['Legday'] == True) & (df['Backday'] == True)].count().sum()

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
        day = 'Back.' #use a dot to distinguish from do1.py 
    elif row['Yoga'] == 1:
        day = 'Yoga'
    else:
        day = 'Other' #
    return day

## go from binary variables to a categorical variable
df['Daycategory'] = df.apply(daycategorizer, axis=1)
# type is categorical
df['Daycategory'] = df['Daycategory'].astype('category')


## EDA  

# same as in do1.py

