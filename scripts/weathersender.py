# coding=utf-8
# This script sends outdoors temperature info to InfluxDB.
# Temperature is fetched from FMI open data using https://github.com/jurajama/FMIWeatherClient
from optparse import OptionParser
from fmiweatherlib import fmiweather
import pprint

from influxdb import InfluxDBClient
import datetime

if __name__ == '__main__':
    parser = OptionParser('usage: %prog [options]')

    parser.add_option("-l", "--location", type="string", dest="location", help="Location for which weather data is searched")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Enable debug mode")

    (options, args) = parser.parse_args()

    required="location".split()

    for r in required:
        if options.__dict__[r] is None:
            parser.error("parameter %s required"%r)

    w = fmiweather(debug=options.debug)

    measTime = None
    temperature = 0.0

    measTime, temperature = w.getCurrentWeather(location=options.location, historyMinutes=30)
    

    json_temp = [
        {
            "measurement": "weather",
            "time": measTime,
            "fields": {
               "OutTemperature": temperature
            }
        }
    ]

#    print "result: " + measTime + " : " + temperature

    if measTime!=None and temperature!=None:
        client = InfluxDBClient('10.20.30.40', 8086, 'username', 'password', 'raspidata', timeout=5)
        client.write_points(json_temp)
