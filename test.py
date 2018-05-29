import datetime
import time as ts

st = datetime.datetime.fromtimestamp(ts.time()).strftime('%Y-%m-%d %H:%M:%S')

print(st)