#! /usr/bin/env python

from sensor_BH1750 import BH1750
from sensor_AM2302 import AM2302
from thingspeak import Thingspeak
from display_Nokia_5110 import DisplayNokia5110
import RPi.GPIO as gpio
from pprint import pprint
import bmp180


import json
import time


class Wetterstation:
    def __init__(self, pin_buzzer):
        self.pin_buzzer = pin_buzzer

        self.temperature = 0
        self.temperature2 = 0
        self.humidity = 0
        self.pressure = 0
        self.light = 0

        with open('config.json', 'r') as infile:
            self.config = json.loads(infile.read())

    def read_all(self):
        self.read_sensors()
        self.write_status()
        #self.update_display()
        self.check_alarm()
        self.update_thingspeak()

        gpio.cleanup()

    def read_sensors(self):
        light_sensor = BH1750()
        humid_sensor = AM2302(4)
        self.light = light_sensor.read()

        (self.temperature, self.humidity) = humid_sensor.read()

        # So this here is the first (and maybe last) attempt of an error correction >>>
        if self.temperature > 40 or self.humidity > 110:
            (self.temperature, self.humidity) = humid_sensor.read()
        # <<< Error correction end

        (self.temperature2, self.pressure) = bmp180.readBmp180(0x77)

    def update_thingspeak(self):
        thingspeak = Thingspeak(self.config['thingspeak_api_key'], 'https://api.thingspeak.com/update')

        result = thingspeak.send_data(self.temperature2, self.humidity, self.pressure, self.light)

        print result

    def write_status(self):
        date_time = time.strftime("%d-%m-%Y,%H:%M:%S")

        json_string = '{' \
                      + '"datetime":"' + date_time + '",' \
                      + '"temp":"' + "{:.1f}".format(self.temperature2) + '",'\
                      + '"humid":"' + "{:.1f}".format(self.humidity) + '",' \
                      + '"press":"' + "{:.1f}".format(self.pressure) + '",' \
                      + '"light":"' + "{:.1f}".format(self.light) + '"'\
                      + '}'

        print json_string

        target = open('current_weather.json', 'w')
        target.truncate()
        target.write(json_string)
        target.close()

        jdata = json.loads(json_string)
        pprint(jdata)

    def update_display(self):
        time_now = time.strftime("%d-%m    %H:%M")
        display = DisplayNokia5110()
        display.display_weather_values(time_now, self.temperature2, self.humidity, self.pressure, self.light)

        led_pin = 18

        #gpio.setmode(gpio.BOARD)
        gpio.setmode(gpio.BCM)

        gpio.setup(led_pin, gpio.OUT)

        for i in range(0, 3):
            gpio.output(led_pin, gpio.LOW)
            time.sleep(1)
            gpio.output(led_pin, gpio.HIGH)
            time.sleep(0.5)

    def check_alarm(self):
        if self.config['temp_alarm_status'] != 1:
            return

        temp = int(self.temperature2)
        print temp

        # Temperature alarm!
        if temp > self.config['temp_alarm_value_xx']:
            print "ALARM XX !!!"
            self.run_alarm(20, .1)
        elif temp > self.config['temp_alarm_value_x']:
            print "ALARM X !!!"
            self.run_alarm(15, .2)
        elif temp > self.config['temp_alarm_value']:
            print "ALARM !!!"
            self.run_alarm(10, .3)

    def run_alarm(self, repeats, pause):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.pin_buzzer, gpio.OUT)

        for num in range(0, repeats):
            gpio.output(self.pin_buzzer, 0)
            time.sleep(pause)
            gpio.output(self.pin_buzzer, 1)
            time.sleep(pause)

        gpio.output(self.pin_buzzer, 0)


wetterstation = Wetterstation(17)

wetterstation.read_all()
