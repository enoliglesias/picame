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

button1_pin = 21 # pin for the big red button

# GPIO config

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Functions

def start_photobooth():

  os.chdir("/home/pi/picame")
  remove_hooks()
  camera = sub.Popen("./picam --alsadev hw:1,0", shell=True, stdout=sub.PIPE)
  time.sleep(1)
  sub.Popen("touch hooks/start_record", shell=True, stdout=sub.PIPE)
  time.sleep(5)
  sub.Popen("touch hooks/start_record", shell=True, stdout=sub.PIPE)
  sub.Popen("pgrep -o -x picam | xargs -I {} kill -9 {}", shell=True, stdout=sub.PIPE)
  time.sleep(1)

def remove_hooks():
  sub.Popen("rm -f hooks/*", shell=True, stdout=sub.PIPE)

# Main loop

while True:
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.wait_for_edge(20, GPIO.FALLING)
  start_photobooth()
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(20, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
