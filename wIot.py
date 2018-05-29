import ibmiotf.device
import sys

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
