# -*- coding: utf-8 -*-
"""
Created on Wed Jun 04 12:15:10 2019

@author: Tamojit Saha
@website: tamojitsaha.info
"""
import serial
import sys
import time
import serial.tools.list_ports

def connect(baudrate=115200):

    int1 = 0
    comPort = ""
    initialize = 0
    ports = []
    port_labels = ["CH340","Arduino","CP210"]
    marker = '#'
    
    ports = list(serial.tools.list_ports.comports())
    if len(ports) > 0:
        for p in ports:
            if int1 < len(ports) :
                for pl in port_labels:
                    if pl in p[1]:
                        if "COM" in p[1]:
                            firstIndex =  p[1].index('(')+1
                            secondIndex =  p[1].index(')')
                            comPort = str(p[1][firstIndex : secondIndex])
                
                try:
                    ser = serial.Serial(comPort, 115200, timeout=1)
                    ser.setDTR(False)
                    time.sleep(0.5) #Don't ever delete or change this shit
                    ser.close()
                    time.sleep(1)   #Don't ever delete or change this shit
                    ser.open()
                    time.sleep(3)   #Don't ever delete or change this shit
                    
                    if ser.isOpen():
                        ser.write(marker.encode('ascii'))
                        ser.flushInput()
                        ackData = ser.readline().rstrip('\n')
                        ser.flushOutput()
                        ser.close()
                        
                        if ackData == '~': 
                            initialize = 1
                            
                            if initialize == 1:
                                print ("\nValid device found!")
                                return comPort                               
                            
                        else:
                            print ("\nNo valid device found!")
                            return 0                          
# ser.close()
                        
                except Exception as e:
                    print (e)
                    print ("\nConnection Error!")
                    return 0
    else:
        print ("\nHey DickHEAD,")
        print ("COM ports not found!")
        return 0





if __name__ == '__main__':
    connect()

