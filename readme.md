## Wetterstation

* Install `Raspbian Jessie` from https://www.raspberrypi.org/downloads/raspbian/
* clone `git@github.com:raspikuku/wetterstation.git`
* Enable I2C http://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi/
* `sudo apt-get install python-smbus i2c-tools`

#### Links

* Temperature: included both in humidity and pressure sensors
* Humidity: AM2302 
    https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging?view=all
    https://github.com/adafruit/Adafruit_Python_DHT
* Pressure: BMP180 I2C Digital Barometric Pressure Sensor
    http://www.raspberrypi-spy.co.uk/2015/04/bmp180-i2c-digital-barometric-pressure-sensor/
* Light: BH1750FVI I2C Digital Light Intensity Sensor
    http://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/
* Display Nokia 5110
    https://github.com/adafruit/Adafruit_Nokia_LCD
    `sudo apt-get install python-imaging`

#### Cron

    */10 * * * * cd /home/pi/wetterstation && /usr/bin/sudo /usr/bin/python wetterstation.py