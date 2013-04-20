#!/usr/bin/python

import smbus

def BCD2Up( bcd ):    # function to cut 4 upper bits from byte
        return (str(bcd >> 4))

def BCD2Lo( bcd ):     # function to cut 4 lower bits from byte
        return (str(bcd & 0x0F))

bus = smbus.SMBus(1)  # bus number 2

czas = []
data = []

# read raw data from DS1307
sec = bus.read_byte_data(0x68, 0)
min = bus.read_byte_data(0x68, 1)
hour = bus.read_byte_data(0x68, 2)
day = bus.read_byte_data(0x68, 3)
date = bus.read_byte_data(0x68, 4)
month = bus.read_byte_data(0x68, 5)
year = bus.read_byte_data(0x68, 6)

#       print "RAW - ", hour, min, sec
#       print "RAW - ", day, date, month, year
# convert to strings
czas.append(BCD2Up(hour & 0x3F))
czas.append(BCD2Lo(hour & 0x3F))
czas.append(BCD2Up(min))
czas.append(BCD2Lo(min))
czas.append(BCD2Up(sec))
czas.append(BCD2Lo(sec))

data.append(BCD2Up(date))
data.append(BCD2Lo(date))
data.append(BCD2Up(month))
data.append(BCD2Lo(month))
data.append(BCD2Up(year))
data.append(BCD2Lo(year))

sc = czas[0] + czas[1] + ':' + czas[2] + czas[3] + ':' + czas[4] + czas[5]
sd = data[0] + data[1] + '/' + data[2] + data[3] + '/20' + data[4] + data[5]

print "Current time is: " + sc + "   " + sd

tempH=bus.read_byte_data(0x68, 0x11)
print bin(tempH)
tempL=bus.read_byte_data(0x68, 0x12)
print bin(tempL)