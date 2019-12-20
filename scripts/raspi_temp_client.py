from influxdb import InfluxDBClient
import board
import adafruit_dht
import datetime, sys, time

import my_config as conf

# This script reads temperature data from temperature sensor and
# sends data to InfluxDB in cloud
# See driver installation instructions in:
# https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

def sendDataToInflux(temperature, humidity):
    client = InfluxDBClient(conf.INFLUXDB_HOST, conf.INFLUXDB_PORT, conf.INFLUXDB_USER, conf.INFLUXDB_PWD, conf.INFLUXDB_DATABASE, timeout=5)

    timestamp = datetime.datetime.utcnow()
    str_timestamp = timestamp.isoformat("T") + "Z"

    json_temp = [
        {
            "measurement": "temps",
            "tags": {
                "sensorId": "1"
            },
            "time": str_timestamp,
            "fields": {
            "temperature": temperature,
            "humidity": humidity
            }
        }
    ]

    client.write_points(json_temp)


###########################################
# Main function
###########################################

if __name__ == '__main__':

  gpio_pin    = board.D4   # GPIO pin#4
  dhtDevice   = adafruit_dht.DHT22(gpio_pin)

  read_count = 0

  while(read_count<3):
      try:
          read_count += 1

          temperature = dhtDevice.temperature
          humidity    = dhtDevice.humidity

          if humidity is not None and temperature is not None:
              print('Temp={0:0.1f} C  Humidity={1:0.1f}%'.format(temperature, humidity))
              sendDataToInflux(temperature, humidity)
              sys.exit(0)
          else:
              print('Failed to get reading from sensor.')

      except RuntimeError as error:
          # Errors happen fairly often, DHT's are hard to read, just keep going
          print(error.args[0])

      time.sleep(2)
