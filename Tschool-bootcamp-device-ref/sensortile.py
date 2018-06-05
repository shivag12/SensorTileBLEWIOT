import pexpect
import time as ts
import ibmiotf.device
import sys
import os
import datetime

child = pexpect.spawn("gatttool -b %s -I" %sys.argv[1])

print("Connecting to:"),
print(sys.argv[1])

NOF_REMAINING_RETRY = 3

while True:
    try:
        child.sendline("connect")
        child.expect("Connection successful", timeout=5)
    except pexpect.TIMEOUT:
        NOF_REMAINING_RETRY = NOF_REMAINING_RETRY-1
        if (NOF_REMAINING_RETRY > 0):
            print("timeout, retry...")
            continue
        else:
            print("timeout, giving up.")
            break
    else:
        print("Connected!")

        ## Function to convert hexadecimal to signed decimal values (ex : bbfe to -17410) 
        def hexStrToInt(hexstr):
          val = int((''.join(reversed(hexstr))),16)
          if(((val&0x8000)==0x8000)):
              val = -((val^0xffff)+1)
          return val

        ## Function to connect to IBM Watson Iot
        def ibmiotfconnection():
           try:
              options = {
                "org": "aad6tp",
                "type": "sensortile",
                "id": "84321",
                "auth-method": "token",
                "auth-token": "XXXXXXXXXXXXXXXXX",
                "clean-session": True,
               }
              dclient = ibmiotf.device.Client(options)
              dclient.connect()
           except ibmiotf.ConnectionException as identifier:
              print(str(identifier))
              sys.exit()

           return dclient

        iothub = ibmiotfconnection()

        break

## On connection Successful 
while True:

    if NOF_REMAINING_RETRY > 0:

        # Temperature & Air Pressure data (Handle : 000e (read), 000f (write)) and 0100 command 
        # is used to tell the BLE device to notify for changes
        child.sendline("char-write-cmd 000f 0100")
        child.expect("Notification handle = 0x000e value:", timeout=10)
        child.expect("\r\n")
        envHandle = child.before

        # Example : c2 7a ab 86 01 00 0f 01
        # The first 4 bits (c2 7a) are timestamps. The next 8 bits (ab 86 01 00) are air
        # pressure data. The last 4 bits (0f 01) are temperature data from temperature sensor
        # The data is formated in the little endian format, Temp 0f 01 to be read as 01 0f

        envSplit = envHandle.split( )
        pressure = envSplit[2:6]
        temp = envSplit[6:8]

        st = datetime.datetime.fromtimestamp(ts.time()).strftime('%Y-%m-%d %H:%M:%S')

        jsonString = "{'ts' : %s, 'temp': %s ,'pressure' : %s}" %(st,hexStrToInt(temp)/10,hexStrToInt(pressure)/100)

        iothub.publishEvent("env","json",jsonString)
        print("Environmental data published successfully : ",jsonString)


        # MEMS sensor data (Accelerometer,Gyroscope,Magnometer )
        # (Handle : 00011 (read), 00012 (write)) and 0100 command 
        # is used to tell the BLE device to notify for changes
        child.sendline("char-write-cmd 0012 0100")
        child.expect("Notification handle = ", timeout=10)
        child.expect("\r\n")
        memsHandle = child.before


        # Example : d7 32  e5 ff a3 ff fa 03  00 00 f2 ff fc ff  0a ff 04 00 bb fe
        # The first 4 bits (d7 32) are timestamps. The next 12 bits (e5 ff a3 ff fa 03) are Accelerometer
        # data. The next 12 bits (00 00 f2 ff fc ff) are Gyroscope data and the last 12 bits are Magnometer
        # data  (0a ff 04 00 bb fe). The data is formated in the little endian format

        memsSplit = memsHandle.split( )
        #Accelerometer data 
        Accx = memsSplit[2:4]
        Accy = memsSplit[4:6]
        Accz = memsSplit[6:8]

        #Gyroscope data
        gyrox = memsSplit[8:10]
        gyroy = memsSplit[10:12]
        gyroz = memsSplit[12:14]

        #Magnotometer data
        magx = memsSplit[14:16]
        magy = memsSplit[16:18]
        magz = memsSplit[18:20]        

        st = datetime.datetime.fromtimestamp(ts.time()).strftime('%Y-%m-%d %H:%M:%S')

        MEMSjsonString = {
          "acc" : {
            "x" : hexStrToInt(Accx),
            "y" : hexStrToInt(Accy),
            "z" : hexStrToInt(Accz)
            },
          "gyro" : {
            "x" : hexStrToInt(gyrox),
            "y" : hexStrToInt(gyroy),
            "z" : hexStrToInt(gyroz)
            },
          "mag" : {
            "x" : hexStrToInt(magx),
            "y" : hexStrToInt(magy),
            "z" : hexStrToInt(magz)
            },
            "ts" : st
        }

        iothub.publishEvent("env","json",MEMSjsonString)
        print("MEMS data published successfully : ",MEMSjsonString)
                
        #sys.exit(0)
    else:
        print("FAILED!")
        sys.exit(-1)
