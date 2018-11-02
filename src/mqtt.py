#!/usr/bin/env python

from __future__ import print_function
import time
import json
import traceback

from config import *
from sensor.MyBME280 import MyBME280
from sensor.SDS011 import SDS011
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from AWSIoTPythonSDK.exception.AWSIoTExceptions import publishTimeoutException

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

print("Start\n", flush=True)

last_time = 0
bme = MyBME280(ic2_address=bme280_ic2, t_offset=bme280_offset)
sds = SDS011(sds_port, sds_baudrate)

try:
    # Connect and subscribe to AWS IoT
    print("connecting...", flush=True)
    myAWSIoTMQTTClient.connect()
    print("connected", flush=True)
    # myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
    # time.sleep(2)

    # Publish to the same topic in a loop forever
    while True:
        try:
            now = time.time()

            if (last_time+intv) <= now:
                # SDS011
                done = sds.wake_read_sleep()
                if done:
                    t = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(now))
                    payload = sds.format_payload('pm10', now, sds.pm10)
                    print("sending "+str(payload)+" to "+topic_pm10+" "+t, flush=True)
                    myAWSIoTMQTTClient.publish(topic_pm10, json.dumps(payload), 1)

                    payload = sds.format_payload('pm25', now, sds.pm25)
                    print("sending "+str(payload)+" to "+topic_pm25+" "+t, flush=True)
                    myAWSIoTMQTTClient.publish(topic_pm25, json.dumps(payload), 1)
                else:
                    print("no data from SDS sensor", flush=True)
                # BME280
                done = bme.read_sensor()
                if done:
                    t = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(now))
                    payload = bme.get_temp_payload(now)
                    print("sending "+str(payload)+" to "+topic_temp+" "+t, flush=True)
                    myAWSIoTMQTTClient.publish(topic_temp, json.dumps(payload), 1)

                    payload = bme.get_hum_payload(now)
                    print("sending "+str(payload)+" to "+topic_hum+" "+t, flush=True)
                    myAWSIoTMQTTClient.publish(topic_hum, json.dumps(payload), 1)

                    payload = bme.get_pres_payload(now)
                    print("sending "+str(payload)+" to "+topic_pre+" "+t, flush=True)
                    myAWSIoTMQTTClient.publish(topic_pre, json.dumps(payload), 1)
                else:
                    print("no data from BME280 sensor", flush=True)

                last_time = now
            time.sleep(sleeps)
        except publishTimeoutException as pte:
            print("--------------------", flush=True)
            print(pte.message, flush=True)
            print("continue try connecting...", flush=True)
            myAWSIoTMQTTClient.connect()
            print("connected", flush=True)
        except Exception:
            print("--------------------", flush=True)
            traceback.print_exc()
            print("--------------------", flush=True)
            raise Exception

except KeyboardInterrupt:
    print('Exit', flush=True)
