import RPi.GPIO as GPIO
import urllib2
import json
import datetime
import time

led = 14
beeper = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(beeper, GPIO.OUT)

def notify_pass(dur):
    for i in range(0,dur):
        GPIO.output(led,GPIO.HIGH)
        if i < 10:
            GPIO.output(beeper,GPIO.HIGH)
        time.sleep(0.10)
        GPIO.output(beeper,GPIO.LOW)
        time.sleep(0.40)
        GPIO.output(led,GPIO.LOW)
        
        time.sleep(0.50)

notify_pass(20)
