# import datetime
# import time as ts

# st = datetime.datetime.fromtimestamp(ts.time()).strftime('%Y-%m-%d %H:%M:%S')

# print(st)

import sys as sys

def hexStrToInt(hexstr):
    val = int((''.join(reversed(hexstr))),16)
    if ((val&0x8000)==0x8000): # treat signed 16bits
        val = -((val^0xffff)+1)
    return val


print("Device Id %s" %(sys.argv[1]))

#ffbf