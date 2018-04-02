import pandas as pd

with open('report/summary.txt', 'w') as f:
    f.write(str(pd.to_datetime('today')))
    f.write('\n\n')
    #f.write(str(empty_weeks))

print("weeks without training:", empty_weeks, "out of", nrweeks)

    f.write("Last 6 training logs:")
    #f.write(str(print(df[['Date', 'Daycategory', 'Training_time']].head(6))))

