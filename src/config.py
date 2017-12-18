import os
dir = os.path.dirname(__file__)

device_name = "kellerpi"
host = "ABCDEFGHIJKLMN.iot.ZONE.amazonaws.com"
topic_root = "n4"
topic_temp = topic_root+"/keller/temperature"
topic_hum = topic_root+"/keller/humidity"
root_crt = os.path.join(dir, 'root-CA.crt')
cert = os.path.join(dir, 'cert.pem')
key = os.path.join(dir, 'private.key')
gpio = 4
