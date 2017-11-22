#! /usr/bin/python3

import datetime
import sys
import numpy as nd
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Connect to postgres database with credentials
conn = psycopg2.connect(host="host", database= "database", user="user", password="password")

# Extract data functions using pandas
def readPressure():
    return pd.read_sql_query("SELECT pressure FROM pressure", conn)

def readTimestamp():
    return pd.read_sql_query("SELECT timestamp FROM pressure", conn)

# Do not extract any data that is 0
def readTable():
    return pd.read_sql_query("SELECT * FROM pressure where pressure != 0",conn)

# read the sql table 
table = readTable()

# convert timestamp into datetime object
table['timestamp'] = pd.to_datetime(table['timestamp'], unit='s', dayfirst=True)

#plot with axis
plot = table.plot(x='timestamp', y='pressure', kind='line')

# get current time and use it in the filename
time = str(datetime.datetime.now().date())
time = time.replace('-',"_")
filename = 'pressure'+ time+ '.png'

# set axis max and min
plt.ylim([925, 1000])

plt.title('last updated: ' + time)
# save and show
plt.savefig(filename)
plt.show()
