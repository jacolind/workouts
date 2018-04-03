läs denna todo.md och inuti eda.py finns todo oxå.
rimligtivs bör saker flyttas från todo.md till readme.me ang split av två olika datasets.

# continous data stream

In the future, I plan to use the “typeform” package to pull the data directly from the web. Then  I can make the python script publish som key metrics directly on jacoblindberg.com/workout Giving out that link to a few friends will create a public commitment to workout, and ask them to harrass me when I haven’t trained. I can also see my key metrics without having to run the script on my computer.

change the script to allow for:
lats, deltoid, spine as well as abs.
this changes the nr of cols, thereby many steps in the script e.g. df.columns =
as well as he daycategorizer
abs+spine is "core"

# KPI

develop more KPI's. done in the `EDA` sections.


# change in script

step 1: write the script as if all rows have the newer dataframe. done.

step 2: see how typeform handles a changed form (maybe i will just use a new URL instead?)

step 3: depending on 2, choose how to handle it. maybe I will have one file clean_data_version1 and another clean_data_version2 which runs depends on what date the row is in.

# report

make a report, so that all printouts are saved to a text that can be read as a report. ideally with pictures also. Have a folder called /report and inside a folder with the date gets created. Inside that folder are printouts and plots as well as a file called comments and conslusions which I type in my own.

this is done now (2018-01-02). all i have to do is to run
```python
python do1.py
python jinja.py
```

then view the html-file.

when you want to change something you will have to make sure

- the variable exists in the do-file (e.g. `title = 'First header'`)
- the variable "key" exists in the html-file (e.g. `{{ title }}`)
- the variable and its key exists in the form of a dictionary inside `jinja.py` (e.g. `'title': str(title)`)

todo next action: save plots to file. and then include them in the html.

# do1 and do2

do2 is my attempt att allowing for changes in the form. it is a newer version of do1, but it only contains a subsection (part of the data cleaning). for details see the file itself.

# output problems for graphs

graphs look weird when running in the terminal `python do1.py` but look fine if using Spyder to render the plots. same code. what happens? below are the errors i see:

```
@jl1:~/Dropbox/git/workouts$ python do1.py
weeks without training: 13 out of 53
Traceback (most recent call last):
  File "do1.py", line 272, in <module>
    plt.title('Cardio_time (when it is >)', cardiothreshold)
  File "/home/j/anaconda3/lib/python3.6/site-packages/matplotlib/pyplot.py", line 1382, in title
    return gca().set_title(s, *args, **kwargs)
  File "/home/j/anaconda3/lib/python3.6/site-packages/matplotlib/axes/_axes.py", line 189, in set_title
    title.update(fontdict)
  File "/home/j/anaconda3/lib/python3.6/site-packages/matplotlib/text.py", line 243, in update
    bbox = kwargs.pop("bbox", sentinel)
AttributeError: 'int' object has no attribute 'pop'
```

# data format

Newer data format puts the multiple choice question into a single column and separates the entry with `/ `. Here we can use pandas "contains".

```
#,date,Yoga,Cardio_time,Muscles,Muscles_time,Stretch_time,Notes,Start Date (UTC),Submit Date (UTC),Network ID
068127e3d5e9ca5f5fac8e04fa692a9e,2010-01-01,0,10," / Biceps / Deltoid / Framsida lÃ¥r / Lats / Spine / Triceps",12,0,testing form,2018-04-03 09:05:14,2018-04-03 09:05:40,d3560842b2
```

Old data format puts the multiple choice question into many columns. Here we can replace NaN with zero and not NaN with one, to indicate that a certain muscle was trained.

```
#,date,Yoga,Cardio_time,Framsida lår,Baksida lår,Rumpa,Vad,Rygg,Biceps,Bröst,Axlar,Triceps,Other,Muscles_time,Stretch_time,Notes,Start Date (UTC),Submit Date (UTC),Network ID
851b2aafd17e789d3776d131f761192c,2018-03-26,,5,,,,Vad,Rygg,,,,,,55,10,,2018-03-26 14:25:43,2018-03-26 14:26:09,55833cdf57
```

Our cleaning must allow for this. Create a function that imports and cleans the old format, and a separate one for the new format. Then a thirs function which wraps these two into one so that if dataformat='new' then clean in one style, otherwise in another style.

I can do one of two things:
- edit the old typeform ".1" and see how the export looks, and depending on that use what I wrote above. (If it exports in the new format I don't need to use both)
- stop using ".1" and only use ".2" when I analyze my data I import both .1 and .2 csv files. this is probably easier.

hur gör jag med back vs indelningen i tre st muskelgrupper? gammaldata: back = backday. ny data: ngn av de tre är backday. och om jag ska anlysera finare nivå så sätte rjag bara NaN på dom musklerna innan ett visst datum. enkelt.

- clean1.py imports and cleans the data. it drops some cols, renames them, etc.
- clean2.py same as above, but version 2 i.e. when I have three ways of splitting back excercises plus the new typeform download format where multi choice is separated with slashes
- merge.py merges the datasets used in clean1 and clean2. it creates a few new columns also.
- eda.py is the actual analysis, it starts with the creation of new columns.

maybe merge can be put inside eda

# small fixes

`df2['Legday']` can probably be created in a more clean way, see cheat sheet or google rowwise sum of certain columns

#
