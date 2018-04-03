#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:07:00 2018

@author: j
"""


## yoga is alway 55 min

df.loc[df.Yoga == 1, 'Training_time'] = 55


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


