#!/usr/bin/env python
# created by https://github.com/enoliglesias

import os
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
import picamera
from signal import alarm, signal, SIGALRM, SIGKILL

# Global var

button1_pin = 21 # pin for the big red button

# GPIO config

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Functions

def start_photobooth():

  camera = picamera.PiCamera()
  camera.start_preview()
  time.sleep(3)
  camera.stop_preview()
  now = time.strftime("%Y-%m-%d-%H:%M:%S")
  camera.capture('photo-'+now+'.jpg')
  camera.close()

# Main loop

while True:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.wait_for_edge(21, GPIO.FALLING)
  start_photobooth()
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
