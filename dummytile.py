import ibmiotf.device
import sys 

enviornmentService = "d7 32 e5 ff a3 ff fa 03 00 00 f2 ff fc ff 0a ff 04 00 bb fe"

envSplit = enviornmentService.split( )

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


def hexStrToInt(hexstr):
    val = int((''.join(reversed(hexstr))),16)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val


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
     }
}

print(MEMSjsonString)


# pressure = envSplit[2:6]
# temp = envSplit[6:8]

# def ibmiotfconnection():
#     try:
#         options = {
#             "org": "aad6tp",
#             "type": "sensortile",
#             "id": "84321",
#             "auth-method": "token",
#             "auth-token": "4b&*XpLFmddph7RdBq",
#             "clean-session": True,
#         }

#         dclient = ibmiotf.device.Client(options)
#         dclient.connect()
#     except ibmiotf.ConnectionException as identifier:
#         print(str(identifier))
#         sys.exit()

#     return dclient

# def hexStrToInt(hexstr):
#     arrreverse = ''.join(reversed(hexstr))
#     return int(arrreverse,16)/100

# jsonString = "{'temp': %s ,'pressure' : %s}" %(hexStrToInt(temp),hexStrToInt(pressure))
# print(jsonString)

# deviceIns =  ibmiotfconnection()
# deviceIns.publishEvent("env","json",jsonString,1)

#print(int("000f",16))


