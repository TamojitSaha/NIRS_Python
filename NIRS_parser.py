# -*- coding: utf-8 -*-
"""
Created on Wed Jun 05 17:15:17 2019

@author: Tamojit Saha
@website: tamojitsaha.info
"""
import numpy as np
from time import sleep
import datetime
import sys
from connectArduino import connect
import serial
import serial.tools.list_ports


def timestamp():    
    time = datetime.datetime.now() 
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    mins = time.minute
    secs = time.second
    micro = time.microsecond
    #print (hour,mins,secs)
    return year,month,day,hour,mins,secs,micro

marker = '#'
def readSerial():
    try:
        comport = connect()
        if comport == 0:
            print ("Device disconnected!")
            return 0
        else:
            ser = serial.Serial(comport, 115200, timeout=None, rtscts=False, dsrdtr=False)
            ser.flush()
            return ser.readline()
            
            # ser.setDTR(False)
            # sleep(0.5) #Don't ever delete or change this shit
            # ser.close()
            # sleep(1)   #Don't ever delete or change this shit
            # ser.open()
            # sleep(3)
            # ser.write(marker.encode('ascii'))
            # ser.flushInput()
            # ackData = ser.readline().rstrip('\n')
            # ser.flushOutput()
            
            # if ackData == '~':
            #     try:
            #         data = ser.readline()
            #         return data
            #     except Exception as e:
            #         return 0
            #         sys.exit()

    except Exception as e:
        print ("\nRead error!")
        print (e)


bigdata = []
def parse(str1,timeData):    
    buffer = [] 
    initial_buffer = []    

    y,m,d,h,m,s,us = timeData
    # print (y,m,d,h,m,s)
    str1 = str1.rstrip()
    
    for e in str1.split('\t') : 
        buffer.append(int(e))

    if len(initial_buffer) < 1:
        for i in buffer: initial_buffer.append(i)
        del buffer[:]

    else:
        # str2 mean read serial data
        timeData = str(h)+":"+str(m)+":"+str(s)
        str2 = str2.rstrip()
        #list -> timestamp and all data
        #this list will be appended in a different 
        #list named bigData()
        format_data_list = []
        # add serial data to buffer
        for e in str2.split('\t') : 
            buffer.append(int(e))
        # compare if the current serial data is new
        if buffer[0] > initial_buffer[0]:
            bufferLength = len(buffer)
            newMicros = initial_buffer[1] + buffer[1]
            buffer[1] = newMicros
            
            format_data_list.append(timeData)
            format_data_list.extend(buffer[2:]) 
            bigData.append(format_data_list)            





if __name__== '__main__':
    str1 = "0\t0\t375\t362\t359\t"
    str2 = "1\t20014\t785\t457\t654"
    # readSerial()
    parse(str1, timestamp())
    timestamp()
    


