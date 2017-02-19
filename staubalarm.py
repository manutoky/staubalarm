#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:21:02 2017

@author: manu
"""
import requests
import json

debug = True
sensor_ip = "192.168.100.68"
ifttt_event = "Feinstaub"
ifttt_key   = "******"

# Get data from sensor
requestString = "http://" + sensor_ip + "/data.json"
r = requests.get(requestString)
sensorData = json.loads(r.content.decode("utf-8"))
if debug: 
    print("Reply")
    print(sensorData)
    print("\nSensor values")

# Get dust sensdor values
val_PM10 = 0
val_PM25 = 0
for i in sensorData['sensordatavalues']:
    if i['value_type'] == "SDS_P1":
        val_PM10 = i['value']
        if debug: print("PM10  : " + i['value'])
    if i['value_type'] == "SDS_P2":
        val_PM25 = i['value']
        if debug: print("PM2.5 : " + i['value'])
if debug: print("\n")        

# Trigger IFTTT
if float(val_PM10) > 50:
    if debug: print("Triggering IFTTT")
    requestString = "https://maker.ifttt.com/trigger/" + ifttt_event + "/with/key/" + ifttt_key
    payload = {'value1':val_PM10, 'value2':val_PM25}
    r = requests.post(requestString, data = payload)
    