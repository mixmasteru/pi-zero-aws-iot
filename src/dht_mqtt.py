#!/usr/bin/env python

from __future__ import print_function
import time
import json
import traceback

from config import *
from sensor.DHT22 import DHT22
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException

sleeps = 600
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

last_time = 0
dht = DHT22(gpio)

try:
    # Connect and subscribe to AWS IoT
    print("connecting...")
    myAWSIoTMQTTClient.connect()
    print("connected")
    # myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
    # time.sleep(2)

    # Publish to the same topic in a loop forever
    while True:
        try:
            done = dht.read_sensor()
            if done:
                now = time.time()
                t = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(now))

                if (last_time+intv) <= now:
                    payload = dht.format_payload('temp', now, dht.temperature)
                    print("sending "+str(payload)+" to "+topic_temp+" "+t)
                    myAWSIoTMQTTClient.publish(topic_temp, json.dumps(payload), 1)

                    payload = dht.format_payload('hum', now, dht.humidity)
                    print("sending "+str(payload)+" to "+topic_hum+" "+t)
                    myAWSIoTMQTTClient.publish(topic_hum, json.dumps(payload), 1)

                    last_time = now
            else:
                print("no data from sensor")
            time.sleep(sleeps)
        except publishTimeoutException as pte:
            print("--------------------")
            print(pte.message)
            print("continue")
        except Exception:
            print("--------------------")
            traceback.print_exc()
            raise Exception

except KeyboardInterrupt:
    print('Exit')
