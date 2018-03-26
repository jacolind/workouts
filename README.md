# workouts

Summarize data from my training logs

## Background

In January 2016, I started filling out a quick form after each workout. My goal is to summarize the key metrics to give me clear pointers — supported by data — on where to improve.

## Problem statement

According to my own training logs, how do I exercise?

## Data

I use _Typeform.com_ thanks to their nice interface when completing the form. Unfortunately, the data is far from tidy. For example, the answer to a multiple choice question has been recoded into one column per answer, so I have to melt those columns into a categorical variable.

## Method

I have written a python script where I clean the data, and summarize some key metrics — such as (a) distribution of total training time per workout, (b) stretching time per workout, (c) total cardio time per week, and (d) having a 50/50 split between upper/lower strength training.

##  Conclusions

I run the script whenever I feel the need to anlayze my workouts. Below I have summarized the key findings when I did some analysis at a certain date (format: yyyy-mm-dd)

### 2017-11-15


1. I train my upper body just as often as my lower body.
2. I split my training into: cardio, legs, chest, back, and yoga. The leg workouts are longer than the chest workouts.
3. The time I spend on stretching is too little.
4. There are too many weeks that I have not done any cardio at all. I should do at least one cardio session per week.
