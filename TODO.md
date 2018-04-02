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
