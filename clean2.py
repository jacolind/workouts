#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:07:16 2018

@author: j

created out of "do3"
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
df2.rename(columns={'date':'Date', 
                    'Submit Date (UTC)':'SubmitDate(UTC)'},
                    inplace=True)
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

## Create backday 

df2['Backday'] = ( df2['Deltoid'] +
                 df2['Spine'] +
                 df2['Lats']
                ) > 0
