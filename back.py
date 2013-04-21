#!/usr/bin/python

import smbus
import time
import datetime
from datetime import timedelta
import RPi.GPIO as GPIO
import subprocess

bus = smbus.SMBus(1)  # bus number 2
address = 0x68

now = datetime.datetime.now()
isoweekday=now.isoweekday()

tempSgn=bin(bus.read_byte_data(address, 0x11))[2:].zfill(8)[:-7]
tempH=bin(bus.read_byte_data(address, 0x11))[2:].zfill(8)[1:]
tempL=bin(bus.read_byte_data(address, 0x12))[2:].zfill(8)[:-6]
temp=int('0b'+tempH+tempL,2)*0.25
if not tempSgn: temp=-temp
tempStr=str(temp)

subprocess.call(["mosquitto_pub","-h","api.cosm.com","-u","QDMFqFHDe26IU9zUyS2A0R2sR5SSAKxQanI3YUozVDJaOD0g","-t","/v2/feeds/126698/datastreams/0.csv","-m",tempStr])

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)

print
print "Current date and time: " + now.strftime("%Y-%m-%d %H:%M")

alarmdelta=timedelta(minutes=1)
alarmtime=now+alarmdelta

print "Alarm date and time: " + alarmtime.strftime("%Y-%m-%d %H:%M")

rtcseconds=int('0b0'+bin(int(now.second/10))[2:].zfill(3)+bin(now.second%10)[2:].zfill(4),2)
rtcminutes=int('0b0'+bin(int(now.minute/10))[2:].zfill(3)+bin(now.minute%10)[2:].zfill(4),2)
if now.hour>=20:
    rtchour=int('0b0010'+bin(now.hour%10)[2:].zfill(4),2)
else:
    rtchour=int('0b000'+bin(int(now.hour/10))[2:]+bin(now.hour%10)[2:].zfill(4),2)
rtcweekday=isoweekday
rtcdate=int('0b00'+bin(int(now.day/10))[2:].zfill(2)+bin(now.day%10)[2:].zfill(4),2)
rtcmonth=int('0b000'+bin(int(now.month/10))[2:]+bin(now.month%10)[2:].zfill(4),2)
rtcyear=int('0b'+bin(int((now.year-2000)/10))[2:].zfill(4)+bin(now.year%10)[2:].zfill(4),2)

bus.write_byte_data(address, 0x00, rtcseconds) # set seconds and start clock
bus.write_byte_data(address, 0x01, rtcminutes) # set minutes
bus.write_byte_data(address, 0x02, rtchour) # set hours in 24 hour mode
bus.write_byte_data(address, 0x03, rtcweekday) # set day of week
bus.write_byte_data(address, 0x04, rtcdate) # set date
bus.write_byte_data(address, 0x05, rtcmonth) # set month
bus.write_byte_data(address, 0x06, rtcyear) # set year

alarmseconds=int('0b0'+bin(int(alarmtime.second/10))[2:].zfill(3)+bin(alarmtime.second%10)[2:].zfill(4),2)
alarmminutes=int('0b0'+bin(int(alarmtime.minute/10))[2:].zfill(3)+bin(alarmtime.minute%10)[2:].zfill(4),2)
if alarmtime.hour>=20:
    alarmhour=int('0b0010'+bin(alarmtime.hour%10)[2:].zfill(4),2)
else:
    alarmhour=int('0b000'+bin(int(alarmtime.hour/10))[2:]+bin(alarmtime.hour%10)[2:].zfill(4),2)
alarmdate=int('0b00'+bin(int(alarmtime.day/10))[2:].zfill(2)+bin(alarmtime.day%10)[2:].zfill(4),2)

bus.write_byte_data(address, 0x07, alarmseconds) # set seconds and start clock
bus.write_byte_data(address, 0x08, alarmminutes) # set minutes
bus.write_byte_data(address, 0x09, alarmhour) # set hours in 24 hour mode
bus.write_byte_data(address, 0x0a, alarmdate) # set date


bus.write_byte_data(address, 0x0e, 0x05) # set alarm1 on
bus.write_byte_data(address, 0x0f, 0x88) # clear old alarm

subprocess.call("halt")
GPIO.cleanup()
