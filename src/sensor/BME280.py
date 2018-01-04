from .Base import Base
from Adafruit_BME280 import *


class BME280(Base):

    temperature = None
    pressure = None
    humidity = None

    def __init__(self, gpio):
        self.sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def read_sensor(self):
        self.temperature = None
        self.pressure = None
        self.humidity = None

        self.temperature = self.sensor.read_temperature()
        pascals = self.sensor.read_pressure()
        self.pressure = self.pascals / 100
        self.humidity = self.sensor.read_humidity()
        return True

    def get_temp_payload(self, now):
        return super(BME280, self).format_payload('temperature', now, self.temperature)

    def get_hum_payload(self, now):
        return super(BME280, self).format_payload('humidity', now, self.humidity)

    def get_pres_payload(self, now):
        return super(BME280, self).format_payload('pressure', now, self.pressure)
