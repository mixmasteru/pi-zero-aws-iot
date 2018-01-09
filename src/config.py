import os
dir = os.path.dirname(__file__)

device_name = "pizero"
host = "ABCDEFGHIJKLMN.iot.ZONE.amazonaws.com"
topic_root = "n4/outdoor1/"
topic_temp = topic_root+"temperature"
topic_hum = topic_root+"humidity"
topic_pre = topic_root+"pressure"
topic_pm10 = topic_root+"pm10"
topic_pm25 = topic_root+"pm25"
root_crt = os.path.join(dir, 'root-CA.crt')
cert = os.path.join(dir, 'cert.pem')
key = os.path.join(dir, 'private.key')
gpio = 4
bme280_ic2 = 0x76

sds_port = "/dev/ttyUSB0"
sds_baudrate = 9600
