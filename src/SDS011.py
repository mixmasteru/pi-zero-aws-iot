# -*- coding: utf-8 -*-
#  SDS011
#
#  based on work from luetzel <webmaster_at_raspberryblog.de>
from __future__ import print_function
import serial, struct, sys, time


class SDS011:

    pm10 = None
    pm25 = None

    def __init__(self, port, baudrate):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.open()
        self.ser.flushInput()

    def dump_data(self, d):
        print(' '.join(x.encode('hex') for x in d))

    def process_frame(self, d):
        # dump_data(d) #debug
        r = struct.unpack('<HHxxBBB', d[2:])
        pm25 = r[0]/10.0
        pm10 = r[1]/10.0
        checksum = sum(ord(v) for v in d[2:8])%256
        print("PM 2.5: {} μg/m^3  PM 10: {} μg/m^3 CRC={}".format(pm25, pm10, "OK" if (checksum==r[2] and r[3]==0xab) else "NOK"))

        if checksum == r[2] and r[3] == 0xab:
            return pm10, pm25
        else:
            return None, None

    def sensor_read(self):
        byte = 0
        while byte != "\xaa":
            byte = self.ser.read(size=1)
        d = self.ser.read(size=10)
        if d[0] == "\xc0":
            return self.process_frame(byte + d)

    # 0xAA, 0xB4, 0x06, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x06, 0xAB
    def sensor_wake(self):
        bytes = ['\xaa', #head
                 '\xb4', #command 1
                 '\x06', #data byte 1
                 '\x01', #data byte 2 (set mode)
                 '\x01', #data byte 3 (sleep)
                 '\x00', #data byte 4
                 '\x00', #data byte 5
                 '\x00', #data byte 6
                 '\x00', #data byte 7
                 '\x00', #data byte 8
                 '\x00', #data byte 9
                 '\x00', #data byte 10
                 '\x00', #data byte 11
                 '\x00', #data byte 12
                 '\x00', #data byte 13
                 '\xff', #data byte 14 (device id byte 1)
                 '\xff', #data byte 15 (device id byte 2)
                 '\x05', #checksum
                 '\xab'] #tail

        for b in bytes:
            self.ser.write(b)

    # xAA, 0xB4, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x05, 0xAB
    def sensor_sleep(self):
        bytes = ['\xaa', #head
                 '\xb4', #command 1
                 '\x06', #data byte 1
                 '\x01', #data byte 2 (set mode)
                 '\x00', #data byte 3 (sleep)
                 '\x00', #data byte 4
                 '\x00', #data byte 5
                 '\x00', #data byte 6
                 '\x00', #data byte 7
                 '\x00', #data byte 8
                 '\x00', #data byte 9
                 '\x00', #data byte 10
                 '\x00', #data byte 11
                 '\x00', #data byte 12
                 '\x00', #data byte 13
                 '\xff', #data byte 14 (device id byte 1)
                 '\xff', #data byte 15 (device id byte 2)
                 '\x05', #checksum
                 '\xab'] #tail

        for b in bytes:
            self.ser.write(b)

    def wake_read_sleep(self):
        self.pm10 = None
        self.pm25 = None
        self.sensor_wake()
        time.sleep(15)
        self.ser.flushInput()
        self.pm10, self.pm25 = self.sensor_read()
        time.sleep(5)
        self.sensor_sleep()
        if self.pm10 is not None and self.pm25 is not None:
            return True
        else:
            return False

    def format_payload(self, type, now, value):
        localtime = time.localtime(now)
        pl = {'timestamp': int(now),
              'type': type,
              'datetime': time.strftime("%Y%m%d%H%M%S", localtime),
              'value': value}

        return pl