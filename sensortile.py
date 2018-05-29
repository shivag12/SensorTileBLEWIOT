import pexpect
import time
import sys
import os

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
    if (NOF_REMAINING_RETRY>0):
      print "timeout, retry..."
      continue
    else:
      print "timeout, giving up."
      break
  else:
    print("Connected!")
    break

while True:

 
  if NOF_REMAINING_RETRY>0:

    # Temperature & Air Pressure data
    child.sendline("char-write-cmd 000f 0100")
    child.expect("Notification handle = 0x000e value:",timeout=10)
    child.expect("\r\n")
    print("Pressure & Temperature:  ")
    temp = child.before
    pressure = child.before

    tempsplit = temp.split( )
    presuresplit = pressure.split( )
    
    temperature = tempsplit[6:8]
    pressure = presuresplit[2:6]
    
    iotjsonstring =  "{'temp': %s , 'pressure' : %s}" %(temperature,pressure)
    print(iotjsonstring) 

    # Accerlometer Gyroscope & Magnotometer 
    child.sendline("char-write-cmd 0012 0100")
    #child.expect("Characteristic value was written successfully",timeout=10)
    #child.expect("Characteristic value/descriptor: ",timeout=10)
    child.expect("Notification handle = 0x0011 value:",timeout=10)
    child.expect("\r\n")
    print("Accerlometer Gyroscope & Magnotometer : "),
    print(child.before)

    #sys.exit(0)
  else:
    print("FAILED!")
    sys.exit(-1)