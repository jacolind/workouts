## about

# Data comes from my training log.
# Search for "concl:" in order to find actionable insights

## packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## import data

# cd to folder /Documents/python/trainingdata/
df_raw = pd.read_csv('Traaining.1-report.csv', parse_dates=True)

# todo: import automatically using https://github.com/underdogio/typeform

# Remove test entries
# first real training date is 2017-01-17 on row 3. entries 0:2 are tests
df = df_raw[3:]

## rename columns

colnames = ['IDnumber', 'Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Back', 'Biceps', 'Chest', 'Shoulders', 'Triceps',
       'Other', 'Muscles_time', 'Stretch_time', 'Notes',
       'StartDate(TC)', 'SubmitDate(TC)', 'NetworkID']
df.columns = colnames

## keep only some columns

keepcols = ['Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Back', 'Biceps', 'Chest', 'Shoulders', 'Triceps',
       'Other', 'Muscles_time', 'Stretch_time', 'Notes']
df = df[keepcols]

## Create binary variables and recode NaN

# map binaryvars from NaN to 0 and map from not NaN to 1.
binaryvars = ['Legsfront', 'Legsback', 'Ass', 'Calf', 'Back',
             'Biceps', 'Chest', 'Shoulders', 'Triceps']
df[binaryvars] = df[binaryvars].notnull().astype(int)
# map from NaN to 0. this affects e.g. Cardio_time, Other and Notes.
df.fillna(0, inplace=True)

##  Explanation of why I need to create these varaibles

# From df.head() we see 'Chest'='NaN' when I have not trained my chest,
# and 'Chest'='Bröst' when I have trained chest (bröst is swedish for chest).
# df.info() reveals the same problem: dtype=objects but I want dtype=float64
# Hence we must map from 'NaN' to 0, and from 'some-text-not-NaN' to 1.
#
# Why did this problem occur? In typeform I have a multiple choice question,
# apparently when downloading to csv each choice is converted to a variable.

## Chestday vs Legday

# It is chestday if I have done any of these: Chest, Triceps
df['Chestday'] = ( (df['Chest'] == 1)   |
                   (df['Triceps'] == 1)
                  )
# It is legday if I have done any of these: Legsfront, Legsback, Calf.
df['Legday'] = ( (df['Legsfront'] == 1) |
                 (df['Legsback'] == 1)  |
                 (df['Calf'] == 1)
                )
# below is True. there is no rows with both Leg day and chest day.
df[(df['Chestday'] == True) & (df['Legday'] == True)].count().sum() == 0
# below is False. some days are only yoga / cardio / back, not legs / chest.
df[(df['Chestday'] == False) & (df['Legday'] == False)].count().sum() == 0

# is legday vs chestday balanced?
print(sum(df['Chestday']))
print(sum(df['Legday']))

## create variable: Daycategory

# less than cardiothreshold minutes of cardio is merely warmup
cardiothreshold = 30

# function to go from binary variables to a categorical variable
def daycategorizer(row):
    if (row['Cardio_time'] > cardiothreshold) & (row['Muscles_time'] > 0):
        day = 'Cardio & Muscle'
    elif row['Cardio_time'] > cardiothreshold:
        day = 'Cardio'
    elif row['Chestday'] == True:
        day = 'Chest'
    elif row['Legday'] == True:
        day = 'Leg'
    elif row['Back'] == True:
        day = 'Back'
    elif row['Yoga'] == 1:
        day = 'Yoga'
    else:
        day = 'Other' #
    return day

# go from binary variables to a categorical variable
df['Daycategory'] = df.apply(daycategorizer, axis=1)
# type is categorical
df['Daycategory'] = df['Daycategory'].astype('category')
# frequency table
print(df['Daycategory'].value_counts() / df['Daycategory'].count() * 100)
# concl: good split of types

## create variable: Training_time

df['Training_time'] = df['Cardio_time'] + df['Muscles_time'] + df['Stretch_time']

## create variable: Datetime, week

df['Datetime'] = pd.to_datetime(df['Date'])
df['Week'] = df['Datetime'].dt.week
df = df.drop('Date', 1)

## Is Training_time related to category?

df.pivot_table(index='Daycategory', values='Training_time', aggfunc='sum')

# todo: more pivot tables. ask questions.

## Histograms of training time

# Hist for total time
pd.DataFrame.hist(df, column='Training_time')
# concl: I see two groups. maybe legday is a long workout and chestday is shorter.

# Hist by daycateogry
# pd.DataFrame.hist(df, column='Training_time', by='Daycategory')
# this histogram has too few datapoints - must split by legday/chestday instead

# Hist for legdays
pd.DataFrame.hist(df[df.Legday==True], column='Muscles_time')
plt.title('Muscles_time for Legdays')
# Hist for chestdays
pd.DataFrame.hist(df[df.Chestday==True], column='Muscles_time')
plt.title('Muscles_time for Chestdays')

# Stretch_time
print(df['Stretch_time'].describe())
# concl: Stretch_time must go up! stretch every session!

## Last 6 traning sessions - this decides what next excerceise will be

df[['Datetime', 'Daycategory']].tail(6)
df.tail(6)

## Days since last training

nrows = df['Datetime'].count()
pd.to_datetime('today') - pd.to_datetime(df['Datetime'][nrows])

## How much cardio per week?

# Hist of Cardio_time (ignoring warmups)
warmup_threshold = 10
pd.DataFrame.hist(df[df.Cardio_time > warmup_threshold], column='Cardio_time')

# Cardio_time and Muscles_time, per week
tbl1 = pd.pivot_table(df, index='Week',
                          values=['Cardio_time', 'Muscles_time'],
                          aggfunc='sum')
tbl1

# number of weeks with no cardio for an entire week
tbl1[tbl1.Cardio_time == 0].Cardio_time.count()
# fraction of weeks with cardio
n_days = (df['Datetime'].max() - df['Datetime'].min())
n_days = (n_days / np.timedelta64(1, 'D')).astype(int)
n_weeks = n_days / 7
print(tbl1[tbl1.Cardio_time == 0].Cardio_time.count() / n_weeks * 100)
# concl: too many weeks that I do zero cardio!
