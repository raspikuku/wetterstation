#! /usr/bin/env python

from sensor_BH1750 import BH1750
from sensor_AM2302 import AM2302
from thingspeak import Thingspeak
from display_Nokia_5110 import DisplayNokia5110
import RPi.GPIO as gpio
import json
from pprint import pprint
import bmp180

import time

oConfig = open('config.json', 'r')
config = json.loads(oConfig.read())

light_sensor = BH1750()
humid_sensor = AM2302(4)
thingspeak = Thingspeak(config['thingspeak_api_key'], 'https://api.thingspeak.com/update')
# display = DisplayNokia5110()

light = light_sensor.read()

(temperature, humidity) = humid_sensor.read()

# So this here is the first (and maybe last) attempt of an error correction >>>
if temperature > 40 or humidity > 110:
    (temperature, humidity) = humid_sensor.read()
# <<< Error correction end

(temperature2, pressure) = bmp180.readBmp180(0x77)


date_time = time.strftime("%d-%m-%Y,%H:%M:%S")
time_now = time.strftime("%d-%m    %H:%M")

log = date_time + ","
log = log + "{:.1f}C".format(temperature2) + ","
log = log + "{:.1f}%".format(humidity) + ","
log = log + "{:.2f}mBar".format(pressure) + ","
log = log + "{:.1f}lx".format(light) + ","

print log

json_string = '{"datetime":"' + date_time + '",'
json_string = json_string + '"temp":"' + "{:.1f}".format(temperature2) + '",'
json_string = json_string + '"humid":"' + "{:.1f}".format(humidity) + '",'
json_string = json_string + '"press":"' + "{:.1f}".format(pressure) + '",'
json_string = json_string + '"light":"' + "{:.1f}".format(light) + '"'
json_string = json_string + '}'

print json_string

target = open('current_weather.json', 'w')
target.truncate()
target.write(json_string)
target.close()

jdata = json.loads(json_string)
pprint(jdata)
#display.display_weather_values(time_now, temperature2, humidity, pressure, light)

led_pin = 18

#gpio.setmode(gpio.BOARD)
gpio.setmode(gpio.BCM)

gpio.setup(led_pin, gpio.OUT)

for i in range(0, 3):
    gpio.output(led_pin, gpio.LOW)
    time.sleep(1)
    gpio.output(led_pin, gpio.HIGH)
    time.sleep(0.5)

temp = int(temperature2)
print temp

# Temperature alarm!
if temp > config['temp_alarm_value'] and config['temp_alarm_status'] == 1:
    print "ALARM!!!"
    gpio.setup(17, gpio.OUT)

    for num in range(0, 10):
        gpio.output(17, 0)
        time.sleep(.3)
        gpio.output(17, 1)
        time.sleep(.3)

    gpio.output(17, 0)

gpio.cleanup()

# Update Thingspeak

result = thingspeak.send_data(temperature2, humidity, pressure, light)

print result
