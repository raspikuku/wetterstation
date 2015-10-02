import Adafruit_DHT

class AM2302:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.pin)
        return (temperature, humidity)


