import wIot as watsoniot


deviceClient = watsoniot.ibmiotfconnection()

deviceClient.publishEvent("status","json","{'temp' : 70}")

print(int("FFFFF63C",16))