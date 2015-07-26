#!/usr/bin/env python
# created by https://github.com/enoliglesias

import os
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
import picamera
from signal import alarm, signal, SIGALRM, SIGKILL
import subprocess as sub

# Global var

button1_pin = 26
button2_pin = 12

# GPIO config

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Functions

def take_photo(n):
  camera = picamera.PiCamera()
  camera.start_preview()
  time.sleep(3)
  camera.stop_preview()
  now = time.strftime("%Y-%m-%d-%H:%M:%S")
  camera.capture('photo-'+now+'.jpg')
  camera.close()

def take_video(n):
  os.chdir("/home/pi/picam")
  remove_hooks()
  camera = sub.Popen("./picam --alsadev hw:0,0", shell=True, stdout=sub.PIPE)
  time.sleep(1)
  sub.Popen("touch hooks/start_record", shell=True, stdout=sub.PIPE)
  time.sleep(5)
  sub.Popen("touch hooks/start_record", shell=True, stdout=sub.PIPE)
  sleep(2)
  sub.Popen("pgrep -o -x picam | xargs -I {} kill -9 {}", shell=True, stdout=sub.PIPE)

def remove_hooks():
  sub.Popen("rm -f hooks/*", shell=True, stdout=sub.PIPE)

GPIO.add_event_detect(button1_pin, GPIO.FALLING, callback=take_photo, bouncetime=200)
GPIO.add_event_detect(button2_pin, GPIO.FALLING, callback=take_video, bouncetime=200)

# Main loop

while True:
  time.sleep(0.5)