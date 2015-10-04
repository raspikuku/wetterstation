#!/usr/bin/python

from sensor_BH1750 import BH1750
from sensor_AM2302 import AM2302
from thingspeak import Thingspeak
from display_Nokia_5110 import DisplayNokia5110

import bmp180

import time

THINGSPEAK_KEY = 'P3WBYMYKA5R6AZLV'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

light_sensor = BH1750()
humid_sensor = AM2302(4)
thingspeak = Thingspeak(THINGSPEAK_KEY, THINGSPEAK_URL)
display = DisplayNokia5110()

light = light_sensor.read()

(temperature, humidity) = humid_sensor.read()

if temperature > 40 or humidity > 110:
    (temperature, humidity) = humid_sensor.read()

(temperature2, pressure) = bmp180.readBmp180(0x77)

result = thingspeak.send_data(temperature2, humidity, pressure, light)

print result

date_time = time.strftime("%d-%m-%Y,%H:%M:%S")
time_now = time.strftime("%d-%m    %H:%M")

log = date_time + ","
log = log + "{:.1f}C".format(temperature2) + ","
log = log + "{:.1f}%".format(humidity) + ","
log = log + "{:.2f}mBar".format(pressure) + ","
log = log + "{:.1f}lx".format(light) + ","

print log

display.display_weather_values(time_now, temperature2, humidity, pressure, light)
