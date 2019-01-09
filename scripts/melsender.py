# coding=utf-8
# This script fetches data from Mitsubishi Electric air conditioning unit cloud controller
# using https://github.com/jurajama/MELCloudLib
from optparse import OptionParser
from melcloudlib import mcloud
import pprint

from influxdb import InfluxDBClient
import datetime

if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-u", "--username", type="string", dest="username", help="MelCloud username")
    parser.add_option("-p", "--password", type="string", dest="password", help="MelCloud password")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    required="username password".split()

    for r in required:
        if options.__dict__[r] is None:
            parser.error("parameter %s required"%r)

    mc = mcloud(debug=options.debug)
    mc.login(options.username, options.password)

    paramNames = ['FanSpeed','RoomTemperature','SetTemperature']
    output = mc.getDeviceParams(paramNames)

    # Debug printout
#    pp = pprint.PrettyPrinter()
#    pp.pprint(output)

#    print "RoomTemperature is " + str(output['RoomTemperature'])

    timestamp = datetime.datetime.utcnow() # <-- get time in UTC
    str_timestamp = timestamp.isoformat("T") + "Z"

    json_temp = [
        {
            "measurement": "mcloud",
            "time": str_timestamp,
            "fields": {
               "RoomTemperature": output['RoomTemperature'],
               "SetTemperature": output['SetTemperature'],
               "FanSpeed": output['FanSpeed']
            }
        }
    ]

    client = InfluxDBClient('10.20.30.40', 8086, 'influxusername', 'influxpassword', 'raspidata', timeout=5)

    client.write_points(json_temp)
