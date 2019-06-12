# -*- coding: utf-8 -*-
"""
Created on Wed Jun 05 17:15:17 2019

@author: Tamojit
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


bigData = []
initial_buffer = []    
firstSerialDataFlag = False

def parse(str1,timeData ):    
    buffer = [] 
    global initial_buffer
    global bigData
    global firstSerialDataFlag

    y,m,d,h,m,s,us = timeData
    timeStampData = str(h)+":"+str(m)+":"+str(s)

    # print (y,m,d,h,m,s)
    str1 = ''.join(str1)
    str1 = str1.rstrip()
    for e in str1.split('\t') : 
        buffer.append(int(e))

    if len(initial_buffer) < 1:
        firstSerialDataFlag = True

        for i in buffer: 
            initial_buffer.append(i)
        
        if firstSerialDataFlag == True:
            firstSerialDataList = []
            timeStampData += ":"+str('0')
            firstSerialDataList.append(timeStampData)
            firstSerialDataList.extend(buffer[2:])
            bigData.append(firstSerialDataList)
            # print (firstSerialDataList)
            firstSerialDataFlag = False

        # print (initial_buffer)
        del buffer[:]

    else:
        # str1 mean read serial data        
        # str1 = str1.rstrip()
        #list -> timestamp and all data
        #this list will be appended in a different 
        #list named bigData()
        format_data_list = []
        # add serial data to buffer
        # for e in str1.split('\t') : 
        #     buffer.append(int(e))
        # compare if the current serial data is new
        if buffer[0] > initial_buffer[0]:

            bufferLength = len(buffer)
            newMicros = initial_buffer[1] + buffer[1]
            
            # buffer[1] = newMicros

            # print (buffer[1])
            
            
            format_data_list.append(timeStampData+":"+str(newMicros))
            format_data_list.extend(buffer[2:]) 
            bigData.append(format_data_list)
            initial_buffer[1] =  newMicros
                       





if __name__== '__main__':
    str1 = [["0\t0\t375\t362\t359"],
     ["1\t20014\t785\t457\t654"],
     ["2\t20024\t378\t362\t359"],
     ["3\t20034\t785\t457\t654"],
     ["4\t20044\t375\t362\t359"],
     ["5\t20054\t785\t457\t654"]]
    # str1[6] = "6\t20064\t375\t362\t359"
    # str1[7] = "7\t20074\t785\t457\t654"
    # str1[8] = "8\t20084\t375\t362\t359"
    # str1[9] = "9\t20094\t785\t457\t654"
   
    for i in range(len(str1)):
        parse(str1[i], timestamp())          
    # readSerial()
    #parse(str1, timestamp())
    timestamp()
    print (bigData) 
    


