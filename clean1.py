#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:07:52 2018

@author: j

created out of the beginning of do1
"""

## packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns

## import data

# cd to folder /Documents/python/trainingdata/
df1_raw = pd.read_csv('data/Traaining.1.csv', parse_dates=True)

# todo: import automatically using https://github.com/underdogio/typeform

# Remove test entries
# first real training date is 2017-01-17 on row 3. entries 0:2 are tests
df1 = df1_raw.drop(df1_raw.tail(3).index)
# nr of workouts
n = df1.shape[0]

# rename columns
colnames = ['IDnumber', 'Date', 'Yoga', 'Cardio_time', 'Legsfront',
            'Legsback', 'Ass', 'Calf', 'Back', 'Biceps', 'Chest',
            'Shoulders','Triceps',
           'Other', 'Muscles_time', 'Stretch_time', 'Notes',
           'StartDate(UTC)', 'SubmitDate(UTC)', 'NetworkID']
df1.columns = colnames

# convert date dtype
df1.Date = pd.to_datetime(df1.Date)

# keep only some columns
keepcols = ['Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Back', 'Biceps', 'Chest', 'Shoulders', 'Triceps',
       'Other', 'Muscles_time', 'Stretch_time', 'Notes', 'SubmitDate(UTC)']
df1 = df1[keepcols]

## Create binary variables and recode NaN

# map binaryvars from not NaN to 1.
binaryvars = ['Legsfront', 'Legsback', 'Ass', 'Calf', 'Back',
             'Biceps', 'Chest', 'Shoulders', 'Triceps']
df1[binaryvars] = df1[binaryvars].notnull().astype(int)
# map from NaN to 0. this affects e.g. Cardio_time, Other and Notes.
df1.fillna(0, inplace=True)

df1.Date.dt.year.min() > 2015 # somehow fillna fucked this up
dayafter = df1.loc[df1.Date.dt.year < 2017].index + 1
df1.loc[dayafter, 'Date']
df1.loc[df1.Date.dt.year < 2017, 'Date'] = pd.to_datetime('2017-12-05')# quick fix
df1.Date.dt.year.min() > 2015


##  Explanation of why I need to create these varaibles

'''
From df1.head() we see 'Chest'='NaN' when I have not trained my chest,
and 'Chest'='Bröst' when I have trained chest (bröst is swedish for chest).
df1.info() reveals the same problem: dtype=objects but I want dtype=float64
Hence we must map from 'NaN' to 0, and from 'some-text-not-NaN' to 1.

Why did this problem occur?
In typeform I have a multiple choice question,
apparently when downloading to csv each choice is converted to a variable.
'''

## back and backday 

# in version 2 I have split back intro three

df1['Backday'] = df1['Back']
del df1['Back']
df1['Lats'] = np.nan
df1['Spine'] = np.nan
df1['Deltoid'] = np.nan
