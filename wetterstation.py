import urllib
import urllib2
import time

from sensor_BH1750 import BH1750
from sensor_AM2302 import AM2302
import bmp180

THINGSPEAKKEY = 'BQ60SOY9H3O643OC'
THINGSPEAKURL = 'https://api.thingspeak.com/update'

def sendData(url, key, temp, humid, pres, light):
  """
  Send event to internet site
  """

  values = {'key' : key, 'field1' : "{:.1f}".format(temp), 'field2' : "{:.1f}".format(humid), 'field3' : pres, 'field4' : "{:.1f}".format(light)}

  postdata = urllib.urlencode(values)
  req = urllib2.Request(url, postdata)

  log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","
  log = log + "{:.1f}C".format(temp) + ","
  log = log + "{:.1f}%".format(humid) + ","
  log = log + "{:.2f}mBar".format(pres) + ","
  log = log + "{:.1f}lx".format(light) + ","

  try:
    # Send data to Thingspeak
    response = urllib2.urlopen(req, None, 5)
    html_string = response.read()
    response.close()
    log = log + 'Update ' + html_string

  except urllib2.HTTPError, e:
    log = log + 'Server could not fulfill the request. Error code: ' + e.code
  except urllib2.URLError, e:
    log = log + 'Failed to reach server. Reason: ' + e.reason
  except:
    log = log + 'Unknown error'

  print log

light_sensor = BH1750()
humid_sensor = AM2302(23)

light = light_sensor.read()

(temperature, humidity) = humid_sensor.read()

if temperature > 35 or humidity > 100:
    (temperature, humidity) = humid_sensor.read()

(temperature2, pressure) = bmp180.readBmp180(0x77)

sendData(THINGSPEAKURL, THINGSPEAKKEY, temperature2, humidity, pressure, light)
