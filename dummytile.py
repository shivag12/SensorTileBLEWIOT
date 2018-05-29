import ibmiotf.device
import sys 

enviornmentService = "c2 7a ab 86 01 00 0f 01"

envSplit = enviornmentService.split( )
pressure = envSplit[2:6]
temp = envSplit[6:8]

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

def hexStrToInt(hexstr):
    arrreverse = ''.join(reversed(hexstr))
    return int(arrreverse,16)/100

jsonString = "{'temp': %s ,'pressure' : %s}" %(hexStrToInt(temp),hexStrToInt(pressure))
print(jsonString)

deviceIns =  ibmiotfconnection()
deviceIns.publishEvent("env","json",jsonString,1)

#print(int("000f",16))


