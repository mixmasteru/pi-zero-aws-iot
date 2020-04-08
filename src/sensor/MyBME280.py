from .Base import Base
from BME280 import BME280


class MyBME280(Base):
    temperature = None
    pressure = None
    humidity = None
    t_offset = None

    def __init__(self, ic2_address, t_offset=0.0):
        self.t_offset = t_offset
        self.sensor = BME280()

    def read_sensor(self):
        self.temperature = None
        self.pressure = None
        self.humidity = None
        data = self.sensor.get_data()
        self.temperature = data['c'] - self.t_offset
        self.pressure = data['p']
        self.humidity = data['h']
        return True

    def get_temp_payload(self, now):
        return super(MyBME280, self).format_payload('temperature', now, round(self.temperature, 2))

    def get_hum_payload(self, now):
        return super(MyBME280, self).format_payload('humidity', now, round(self.humidity, 2))

    def get_pres_payload(self, now):
        return super(MyBME280, self).format_payload('pressure', now, round(self.pressure, 2))
