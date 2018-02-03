from .Base import Base
from Adafruit_BME280 import *


class MyBME280(Base):

    temperature = None
    pressure = None
    humidity = None
    t_offset = None

    def __init__(self, ic2_address, t_offset=0.0):
        self.t_offset = t_offset
        self.sensor = BME280(address=ic2_address,
                             t_mode=BME280_OSAMPLE_8,
                             p_mode=BME280_OSAMPLE_8,
                             h_mode=BME280_OSAMPLE_8)

    def read_sensor(self):
        self.temperature = None
        self.pressure = None
        self.humidity = None

        self.temperature = self.sensor.read_temperature()-self.t_offset
        pascals = self.sensor.read_pressure()
        self.pressure = pascals / 100
        self.humidity = self.sensor.read_humidity()
        return True

    def get_temp_payload(self, now):
        return super(MyBME280, self).format_payload('temperature', now, round(self.temperature, 2))

    def get_hum_payload(self, now):
        return super(MyBME280, self).format_payload('humidity', now, round(self.humidity, 2))

    def get_pres_payload(self, now):
        return super(MyBME280, self).format_payload('pressure', now, round(self.pressure, 2))
