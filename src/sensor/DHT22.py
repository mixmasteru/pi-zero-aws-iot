import Adafruit_DHT
import time


class DHT22:

    sensor = Adafruit_DHT.DHT22
    gpio = None
    humidity = None
    temperature = None

    def __init__(self, gpio):
        self.gpio = gpio

    def read_sensor(self):
        self.humidity = None
        self.temperature = None
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio)

        if self.humidity is not None and self.temperature is not None:
            self.humidity = round(humidity, 2)
            self.temperature = round(temperature, 2)
            return True

        return False

    def format_payload(self, type, now, value):
        localtime = time.localtime(now)
        pl = {'timestamp': int(now),
              'type': type,
              'datetime': time.strftime("%Y%m%d%H%M%S", localtime),
              'value': value}

        return pl


