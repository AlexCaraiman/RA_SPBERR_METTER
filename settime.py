#!/usr/bin/python

import smbus
import time
import datetime
bus = smbus.SMBus(1)
address = 0x68

now = datetime.datetime.now()
isoweekday=now.isoweekday()

print
print "Current date and time using str method of datetime object:"
print str(now)

print
print "Current date and time using instance attributes:"
print "Current year: %d" % now.year
print "Current month: %d" % now.month
print "Current day: %d" % now.day
print "Current hour: %d" % now.hour
print "Current minute: %d" % now.minute
print "Current second: %d" % now.second
print "Current microsecond: %d" % now.microsecond

print
print "Current date and time using strftime:"
print now.strftime("%Y-%m-%d %H:%M")

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



print rtcweekday
print rtcdate

bus.write_byte_data(address, 0x00, rtcseconds) # set seconds and start clock
bus.write_byte_data(address, 0x01, rtcminutes) # set minutes
bus.write_byte_data(address, 0x02, rtchour) # set hours in 24 hour mode
bus.write_byte_data(address, 0x03, rtcweekday) # set day of week
bus.write_byte_data(address, 0x04, rtcdate) # set date
bus.write_byte_data(address, 0x05, rtcmonth) # set month
bus.write_byte_data(address, 0x06, rtcyear) # set year


#bear = bus.read_byte_data(address, 0x03)
#print bear
