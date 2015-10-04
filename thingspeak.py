import urllib
import urllib2


class Thingspeak:
    def __init__(self, key, url):
        self.key = key
        self.url = url

    def send_data(self, temp, humid, press, light):
        """
        Send event to internet site
        """

        values = {
            'key': self.key,
            'field1': "{:.1f}".format(temp),
            'field2': "{:.1f}".format(humid),
            'field3': press,
            'field4': "{:.1f}".format(light)
        }

        post_data = urllib.urlencode(values)
        req = urllib2.Request(self.url, post_data)

        try:
            # Send data to Thingspeak
            response = urllib2.urlopen(req, None, 5)
            html_string = response.read()
            response.close()
            log = 'Update ' + html_string

        except urllib2.HTTPError, e:
            log = 'Server could not fulfill the request. Error code: ' + e.code
        except urllib2.URLError, e:
            log = 'Failed to reach server. Reason: ' + e.reason
        except:
            log = 'Unknown error'

        return log

