## about

# Data comes from my training log.
# Search for "concl:" in order to find actionable insights

## directory

## packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## import data

# cd to folder /Documents/python/trainingdata/
df_raw = pd.read_csv('data/Traaining.1.csv', parse_dates=True)

# todo: import automatically using https://github.com/underdogio/typeform

# Remove test entries
# first real training date is 2017-01-17 on row 3. entries 0:2 are tests
df = df_raw.drop(df_raw.tail(3).index)
# nr of workouts
n = df.shape[0]

## rename columns

colnames = ['IDnumber', 'Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Back', 'Biceps', 'Chest', 'Shoulders', 'Triceps',
       'Other', 'Muscles_time', 'Stretch_time', 'Notes',
       'StartDate(TC)', 'SubmitDate(TC)', 'NetworkID']
df.columns = colnames

# convert date dtype 
df.Date = pd.to_datetime(df.Date)

## keep only some columns

keepcols = ['Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Back', 'Biceps', 'Chest', 'Shoulders', 'Triceps',
       'Other', 'Muscles_time', 'Stretch_time', 'Notes']
df = df[keepcols]

## Create binary variables and recode NaN

# map binaryvars from not NaN to 1.
binaryvars = ['Legsfront', 'Legsback', 'Ass', 'Calf', 'Back',
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

# mutually exclusive
# there are rows with both Leg day and chest day.
chest_and_legday = df[(df['Chestday'] == True) 
                        & (df['Legday'] == True)
                        ].count().sum()
assert chest_and_legday == 0
df.loc[(df.Chestday == True) & (df.Legday == True)]
# collectively exhaustive? no
# some days are only yoga / cardio / back, not legs / chest.
assert 0 < df[(df['Chestday'] == False) 
              & (df['Legday'] == False)].count().sum()

sum(df['Chestday'])
sum(df['Legday'])
n

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

## create variable: week

df['Week'] = df['Date'].dt.week

## Is Training_time related to category?

df.pivot_table(index='Daycategory', values='Training_time', aggfunc='mean')

# todo: more pivot tables. ask questions.

## Histograms of training time

from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns

# Hist for total time
sns.distplot(df.Training_time, kde=False)
# pd.DataFrame.hist(df, column='Training_time')
# concl: I see two groups. maybe legday is a long workout and chestday is shorter.

# Hist by daycateogry
# pd.DataFrame.hist(df, column='Training_time', by='Daycategory')
# this histogram has too few datapoints - must split by legday/chestday instead

# Hist for legdays
sns.distplot(df.loc[df.Legday == 1, 'Muscles_time'])
plt.title('Muscles_time for Legdays')

# Hist for chestdays
sns.distplot(df.loc[df.Chestday == 1, 'Muscles_time'])
plt.title('Muscles_time for Chestdays')

# Stretch_time
print(df['Stretch_time'].describe())
# concl: Stretch_time must go up! stretch every session!

## Last 6 traning sessions - this decides what next excerceise will be

print("Last 6 training logs:")
print(df[['Date', 'Daycategory', 'Training_time']].head(6))

## Variability 

df.Daycategory.values # if two consecutive days have the same training the =1. sum all 1's. / n. it is a measure. 

## Days since last training

pd.to_datetime('today') - pd.to_datetime(df.loc[0, 'Date'])

## How much cardio per week?

# Hist of Cardio_time (ignoring warmups)
cardiothreshold
pd.DataFrame.hist(df[df.Cardio_time > cardiothreshold], column='Cardio_time for cardio sessions')

# Cardio_time and Muscles_time, per week
tbl1 = pd.pivot_table(df, index='Week',
                          values=['Cardio_time', 'Muscles_time'],
                          aggfunc='sum')
tbl1= tbl1 / 60
tbl1.plot()
plt.title('Total training hours per week')
print("Hours per week \n", tbl1.describe())

# number of weeks with no cardio for an entire week
tbl1[tbl1.Cardio_time == 0].Cardio_time.count()
# fraction of weeks with cardio
n_days = (df['Date'].max() - df['Date'].min())
n_days = (n_days / np.timedelta64(1, 'D')).astype(int)
n_weeks = n_days / 7
print(tbl1[tbl1.Cardio_time == 0].Cardio_time.count() / n_weeks * 100)
# concl: too many weeks that I do zero cardio!

# qq data error to fix 
df.loc[df.Date.idxmin(), 'Date']
# if date = 1 then set = previous+1 (as a heuristic).
df.loc[df.Date.idxmax(), 'Date']
