#!/usr/bin/env python3

# ---- LIBRARIES -------

import plotly.graph_objects as go
import pandas as pd
import datetime
from collections import *

# ----------------------

# pandas reads in csv file and labels headings
df = pd.read_csv('log.csv')
df.columns = ["measure", "date"]

# empty lists (used in cleanup process)
log = []
days = []

# ---- CLEAN UP ----------

# for every value in the date column
for i in df["date"]:

        # splits the string into 3 separate components (27/05/2021 --> ['27', '05', '2021'])
        new = i.split('/')

        # for every number in the 'new' list
        for x in new:
                # changes the string number to integer
                x = int(x)
                # adds integer to temporary 'log' list
                log.append(x)

        # changes the date to a day of the week
        numbers = datetime.date(log[2], log[1], log[0])
        days.append(numbers.strftime("%A"))

        # clears log list for the next date in the 'date' column
        log = []

# ---- GRAPH -------

# puts 'days' list in counter function
count = Counter(days)

# uses collections library to count each occurance of the day of the week in the 'days' list
y = [count["Monday"], count["Tuesday"], count["Wednesday"], count["Thursday"], count["Friday"]]

# adds 5 days of the week labels
x = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# adds values to bar chart and changes bar colours (greenish)
fig = go.Figure(go.Bar(x=x, y=y, marker_color='#1A7512'))

# adds titles to heading, x and y axis

fig.update_xaxes(title='Days of the week')
fig.update_yaxes(title='Number of low measurement alerts')
fig.update_layout(title='Low measurements per day')

# produces graph in browser
fig.show()