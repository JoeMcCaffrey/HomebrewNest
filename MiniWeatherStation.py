#!/usr/bin/python

import json
import sys
import time
import datetime

# libraries
import sys
import urllib2
from sense_hat import SenseHat
import psycopg2

# clear the sensehat 
sense = SenseHat()
sense.clear()		
sense.set_rotation(180)
sense.low_light = True

# Gather unix timestamp
timestamp = int(time.time())

# Read tempature, pressure and humidity from sensors
temp = sense.get_temperature()
temp = round(temp, 1)
humidity = sense.get_humidity()
humidity = round(humidity, 1)

pressure = sense.get_pressure()
pressure = round(pressure, 1)

# 8x8 RGB clear it and write Pressure with value in blue
sense.clear()
info = 'Pressure: ' + str(pressure)
sense.show_message(info, text_colour=[0, 0, 255])

#Enter credentials for postgres database
conn = psycopg2.connect(host="pellefant.db.elephantsql.com", database= "database", user="user", password="password")

cur = conn.cursor()

# insert into 2 tables one with just pressure and timestamp and one with other data
cur.execute('''INSERT INTO pressure (timestamp, pressure, id) VALUES (%s, %s, %s);''', (timestamp, pressure, 1,))


cur.execute('''INSERT INTO other_data (timestamp, temp, humidity, id) VALUES (%s, %s, %s, %s);''', (timestamp, temp, humidity, 1,))

conn.commit()
cur.close()
sense.clear()
