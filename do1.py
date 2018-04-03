## about

# Data comes from my training log.
# Search for "concl:" in order to find actionable insights

## directory

## packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns

## import data

# cd to folder /Documents/python/trainingdata/
df_raw = pd.read_csv('data/Traaining.1.csv', parse_dates=True)

# todo: import automatically using https://github.com/underdogio/typeform

# Remove test entries
# first real training date is 2017-01-17 on row 3. entries 0:2 are tests
df = df_raw.drop(df_raw.tail(3).index)
# nr of workouts
n = df.shape[0]

# rename columns
colnames = ['IDnumber', 'Date', 'Yoga', 'Cardio_time', 'Legsfront',
            'Legsback', 'Ass', 'Calf', 'Back', 'Biceps', 'Chest',
            'Shoulders','Triceps',
           'Other', 'Muscles_time', 'Stretch_time', 'Notes',
           'StartDate(TC)', 'SubmitDate(TC)', 'NetworkID']
df.columns = colnames

# convert date dtype
df.Date = pd.to_datetime(df.Date)

# keep only some columns
keepcols = ['Date', 'Yoga', 'Cardio_time', 'Legsfront', 'Legsback',
       'Ass', 'Calf', 'Back', 'Biceps', 'Chest', 'Shoulders', 'Triceps',
       'Other', 'Muscles_time', 'Stretch_time', 'Notes', 'Submit Date (UTC)']
df = df[keepcols]

## Create binary variables and recode NaN

# map binaryvars from not NaN to 1.
binaryvars = ['Legsfront', 'Legsback', 'Ass', 'Calf', 'Back',
             'Biceps', 'Chest', 'Shoulders', 'Triceps']
df[binaryvars] = df[binaryvars].notnull().astype(int)
# map from NaN to 0. this affects e.g. Cardio_time, Other and Notes.
df.fillna(0, inplace=True)

df.Date.dt.year.min() > 2015 # somehow fillna fucked this up
dayafter = df.loc[df.Date.dt.year < 2017].index + 1
df.loc[dayafter, 'Date']
df.loc[df.Date.dt.year < 2017, 'Date'] = pd.to_datetime('2017-12-05')# quick fix
df.Date.dt.year.min() > 2015


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





######################################################################


## Chestday Legday Backday

# It is chestday if I have done any of these: Chest, Triceps
df['Chestday'] = ( (df['Chest'] == 1) +
                   (df['Triceps'] == 1) 
                  ) > 0
# It is legday if I have done any of these: Legsfront, Legsback, Calf.
df['Legday'] = ( df['Legsfront'] +
                 df['Legsback'] +
                 df['Ass']
                ) > 0

df['Backday'] = df['Back']
df['Lats'] = np.nan
df['Spine'] = np.nan
df['Deltoid'] = np.nan

df.Date.dt.year.min() > 2016

## create variable: Daycategory

df.Date.dt.year.min() > 2016

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
        day = 'Other' #
    return day

# go from binary variables to a categorical variable
df['Daycategory'] = df.apply(daycategorizer, axis=1)
# type is categorical
df['Daycategory'] = df['Daycategory'].astype('category')

df.Date.dt.year.min() > 2016


## create variable: Training_time

df['Training_time'] = df['Cardio_time'] + df['Muscles_time'] + df['Stretch_time']

## create variable: week

df['Week'] = df['Date'].dt.week

## create col YearWeek

df['YearWeek'] = df.Date.dt.year + df.Week/100
df.YearWeek.nunique()
# todo: there are weeks when i do not workout. these become hiddne. can be solved by using another dataframe as an index.

# mutually exclusive
# there are rows with both Leg day and chest day.
chest_and_legday = df[(df['Chestday'] == True)
                        & (df['Legday'] == True)
                        ].count().sum()
chest_and_legday == 0
df.loc[(df.Chestday == True) & (df.Legday == True)]

# collectively exhaustive? no
# some days are only yoga / cardio / back, not legs / chest.
0 < df[(df['Chestday'] == False)
              & (df['Legday'] == False)].count().sum()

sum(df['Chestday'])
sum(df['Legday'])
n

df.Date.dt.year.min() > 2016

## yoga is alway 55 min

df.loc[df.Yoga == 1, 'Training_time'] = 55

## all my notes

df.loc[df.Notes != 0, 'Notes']

# because I was lazy in the data entry phase


## resample by week
ts = pd.Series(df.Training_time.values / 60, index = df.Date)
nrweeks = ts.resample('W').sum().count()

## plot nr of workouts / week
ts.resample('W').count().plot()
plt.ylabel('Nr of workouts per week')
plt.title('Nr of wourkouts per week \n (Line is median)')
plt.axhline(y = ts.resample('W').count().median()) # todo make dotted line 
plt.xlabel('')
plt.savefig('plots/nr_perweek.png')

## plot sum of time / week
tsw_sum = ts.resample('W').sum()
tsw_sum.plot()
plt.title('Sum of training time per week')
plt.ylabel('Hours')
plt.xlabel('')
plt.savefig('plots/hours_perweek.png')

## weeks without training
tsw_sum.isnull().sum() / nrweeks*100
sum(tsw_sum == 0)
# todo: zero and NA, whats the diff?
# which weeks:
tsw_sum[tsw_sum == 0]
tsw_sum[tsw_sum.isnull() == True]
# how many weeks:
empty_weeks =  tsw_sum[tsw_sum == 0].shape[0] + tsw_sum[tsw_sum.isnull() == True].shape[0]
print("weeks without training:", empty_weeks, "out of", nrweeks)

# todo: calculate streak lengths. hint: when cumsum today = cumsaum yesterday a streak has begun



'''
scratch-pad
inte så intressanta
# plot training time / month
ts.resample('M').sum().plot()
plt.title('Sum of training time per month')
plt.ylabel('Hours')

ts.resample('M').mean().plot()
plt.title('Sum of training time / nr sessions, per month')
plt.ylabel('Hours')

weeks = pd.date_range('2017-01-01',
                      pd.to_datetime('today'),
                      freq='W-SUN')
'''

## daycategory pie
tab_freq = df['Daycategory'].value_counts() / df['Daycategory'].count() * 100
tab_freq
tab_freq.plot.pie(autopct='%.0f')
plt.title('Daycategory: Equal split?')
plt.ylabel('')
plt.savefig('plots/daycategory_pie.png')
# maybe use: labels = df.groupby('Daycategory').size()
# todo: sns piechart look beetter?
# make it Leg 20% and n=10 so that we understand it immediately
# todo: insert nr of datapoints as labels.

## Training_time by daycategory?
time_bycat = df.pivot_table(index='Daycategory',
                            values='Training_time', aggfunc='mean')
time_bycat = time_bycat.sort_values(by='Training_time', ascending=False)
time_bycat.plot.barh()
plt.xlabel('Mean Training_time (minutes)')
plt.title('Mean Training_time by category')
plt.savefig('plots/time_bycategory.png')
# todo: remove label in top corner 

# todo: more pivot tables. ask questions.

## training time per session

# Hist for total time
sns.distplot(df.Training_time, kde=False)
plt.xlabel('Training_time (minutes)')
plt.ylabel('Frequency')
plt.title('Total training time')
plt.savefig('plots/time_hist.png')


# Hist for legdays
sns.distplot(df.loc[df.Legday == 1, 'Muscles_time'])
plt.title('Muscles_time for Legdays')

# Hist for chestdays
sns.distplot(df.loc[df.Chestday == 1, 'Muscles_time'])
plt.title('Muscles_time for Chestdays')

# Hist for backdays
sns.distplot(df.loc[df.Back == 1, 'Muscles_time'])
plt.title('Muscles_time for Backdays')

# Hist of Cardio_time (ignoring warmups)
cardiothreshold = 30
sns.distplot(df.loc[df.Cardio_time > cardiothreshold, 'Cardio_time'])
plt.title('Cardio_time (when it is >)', cardiothreshold)

# todo: do many kde in one single plot 
sns.distplot(df.loc[df.Legday == 1, 'Muscles_time'])
sns.distplot(df.loc[df.Chestday == 1, 'Muscles_time'])
sns.distplot(df.loc[df.Back == 1, 'Muscles_time'])


# Stretch_time
print(df['Stretch_time'].describe())
stretch_describe =  [df.Stretch_time.quantile(0.25),
                     df.Stretch_time.quantile(0.50),
                     df.Stretch_time.quantile(0.75)]
stretch_describe = 'Percentiles: 25% ' + str(stretch_describe[0]) +                    ', 50% ' + str(stretch_describe[1]) + ', 75% ' + str(stretch_describe[2])
stretch_describe

# concl: Stretch_time must go up! stretch every session!

# todo: CDF instead of historigram

## Last 6 traning sessions - this decides what next excerceise will be

print("Last 6 training logs:")
print(df[['Date', 'Daycategory', 'Training_time']].head(6))
recent_entries = df[['Date', 'Daycategory', 'Training_time']].head(6)
recent_entries 

## Variability

daycat_dummy = pd.get_dummies(df.Daycategory.values)
daycat_dummy.head() 
daycat_dummy.shift(1).head() # lag 1 day
variability = (daycat_dummy + daycat_dummy.shift(1) == 2).sum()
print("output shows how many times a certain daycategory has been followed by the same daycategory (e.g. legday two days in a row")
variability


# Days since last training
print("Days since last training:",
      pd.to_datetime('today') - pd.to_datetime(df.loc[0, 'Date']))


