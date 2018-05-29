import pexpect
import time as ts
import ibmiotf.device
import sys
import os
import datetime

child = pexpect.spawn("gatttool -t random -b C0:7A:18:31:3E:48 -I")

print("Connecting to:"),
print("C0:7A:18:31:3E:48")

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

        def hexStrToInt(hexstr):
            arrreverse = ''.join(reversed(hexstr))
            return int(arrreverse, 16)/100

        def ibmiotfconnection():
           try:

              options = {
                "org": "aad6tp",
                "type": "sensortile",
                "id": "84321",
                "auth-method": "token",
                "auth-token": "4b&*XpLFmddph7RdBq",
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

while True:

    if NOF_REMAINING_RETRY > 0:

        # Temperature & Air Pressure data
        child.sendline("char-write-cmd 000f 0100")
        child.expect("Notification handle = 0x000e value:", timeout=10)
        child.expect("\r\n")
        print("Pressure & Temperature:  ")
        envHandle = child.before

        envSplit = envHandle.split( )
        pressure = envSplit[2:6]
        temp = envSplit[6:8]

        st = datetime.datetime.fromtimestamp(ts.time()).strftime('%Y-%m-%d %H:%M:%S')

        jsonString = "{'ts' : %s, temp': %s ,'pressure' : %s}" %(st,hexStrToInt(temp),hexStrToInt(pressure))

        iothub.publishEvent("env","json",jsonString)
                
        # sys.exit(0)
    else:
        print("FAILED!")
        sys.exit(-1)
