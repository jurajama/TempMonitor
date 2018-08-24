from influxdb import InfluxDBClient
import Adafruit_DHT
import datetime

# This script reads temperature data from temperature sensor and
# sends data to InfluxDB in cloud
# See driver installation instructions in:
# https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated


# Primary server
client = InfluxDBClient('Add-DB-IP-here', 8086, 'raspi', 'raspi123', 'raspidata', timeout=5)

sensor = 22  # sensor model
pin    = 4   # GPIO pin#4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)

timestamp = datetime.datetime.utcnow() # <-- get time in UTC
str_timestamp = timestamp.isoformat("T") + "Z"

json_temp = [
    {
        "measurement": "temps",
        "time": str_timestamp,
        "fields": {
           "temperature": temperature,
           "humidity": humidity
        }
    }
]

client.write_points(json_temp)
