#!/usr/bin/env python

from __future__ import print_function
import time
import json
import traceback
from config import *
from DHT22 import DHT22
from SDS011 import SDS011
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

sleeps = 60
intv = 600

myAWSIoTMQTTClient = AWSIoTMQTTClient(device_name)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(root_crt, key, cert)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

print("Start\n")
# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
print("connected\n")
# myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
# time.sleep(2)
last_time = 0
dht = DHT22(gpio)
sds = SDS011(sds_port, sds_baudrate)
try:
    # Publish to the same topic in a loop forever
    while True:
        try:
            now = time.time()
            localtime = time.localtime(now)

            if (last_time+intv) <= now:
                # SDS011
                done = sds.wake_read_sleep()
                if done:
                    payload = sds.format_payload('pm10', now, sds.pm10)
                    myAWSIoTMQTTClient.publish(topic_pm10, json.dumps(payload), 1)
                    payload = dht.format_payload('pm25', now, sds.pm25)
                    myAWSIoTMQTTClient.publish(topic_pm25, json.dumps(payload), 1)
                    print("pm10: "+str(sds.pm10)+" pm25: "+str(sds.pm25))
                else:
                    print("no data from SDS sensor")
                # DHT2302
                done = dht.read_sensor()
                if done:
                    payload = dht.format_payload('temp', now, dht.temperature)
                    myAWSIoTMQTTClient.publish(topic_temp, json.dumps(payload), 1)
                    payload = dht.format_payload('hum', now, dht.humidity)
                    myAWSIoTMQTTClient.publish(topic_hum, json.dumps(payload), 1)
                    print("temp: "+str(dht.temperature)+" hum: "+str(dht.humidity))
                else:
                    print("no data from DHT sensor")

                last_time = now
            time.sleep(sleeps)
        except Exception:
            print("--------------------")
            traceback.print_exc()
            raise Exception

except KeyboardInterrupt:
    print('Exit')
