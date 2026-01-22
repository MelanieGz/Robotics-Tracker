import RPi.GPIO as GPIO
import time
import csv
import os
from datetime import datetime
import pytz
import requests

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

THRESHOLD = 150
COOLDOWN = 3
TIMEZONE = pytz.timezone("America/Los_Angeles")
API_URL = "http://localhost:8000/trackers"
FILENAME = "sensor_data.csv"
FILE_EXISTS = os.path.exists(FILENAME)
last_time = 0
num_of_people = 0
person = False

def get_dist():
  GPIO.output(TRIG, False)
  time.sleep(0.05)
  GPIO.output(TRIG, True)
  time.sleep(0.00002)
  GPIO.output(TRIG, False)
  start = time.time()
  end = time.time()
  while GPIO.input(ECHO) == 0:
    start = time.time()
  while GPIO.input(ECHO) == 1:
    end = time.time()
  duration = end - start
  distance = (duration * 34300) / 2
  print(f"Distance: {distance:.2f} cm")
  return distance

try:
    with open(FILENAME, "a", newline="") as f:
       writer = csv.writer(f)
       if not FILE_EXISTS:
          writer.writerow(["date", "time", "value"]) 
       while True:
          distance = get_dist()
          if (distance < THRESHOLD and person == False):
             person = True
             num_of_people += 1
             now = datetime.now(TIMEZONE)
             date1 = now.strftime("%Y-%m-%d")
             time1 = now.strftime("%H:%M:%S")
             requests.post(API_URL, json={"value": num_of_people})
             writer.writerow([date1, time1, num_of_people])
             while (distance < THRESHOLD):
                distance = get_dist()
                time.sleep(0.5)
                continue
          if (distance < THRESHOLD and person == True):
             person = False
             while(distance < THRESHOLD):
                distance = get_dist()
                time.sleep(0.5)
                continue
          last_time = time.time()
          print(num_of_people)
          time.sleep(0.3)

except KeyboardInterrupt:
  print("\nStopping Sensor")
  GPIO.cleanup()
