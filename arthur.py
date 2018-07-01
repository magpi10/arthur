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

def get_next_pass():
    try:
        req = urllib2.Request("http://api.open-notify.org/iss-pass.json?lat=-25.989&lon=28.003&alt=1400&n=10")
        response = urllib2.urlopen(req)
        obj = json.loads(response.read())
        n = len(obj['response'])
        if n == 0:
            return None, 0
        else:
            dur = obj['response'][0]['duration']
            rtime = datetime.datetime.utcfromtimestamp(obj['response'][0]['risetime'])
            ltime = datetime_from_utc_to_local(rtime)
            return ltime,dur
    except Exception as err:
        print(str(err))
        return None, 0

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

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

nextstart = None
while nextstart == None:
    nextstart,nextdur = get_next_pass()
    if nextstart == None:
        time.sleep(10)
nextend = nextstart + datetime.timedelta(seconds=nextdur)
       
while True:
    dt = datetime.datetime.now()
    print('Next start = ' + str(nextstart) + ', Dur = ' + str(nextdur) + ', Now = ' + str(dt))
    if dt >= nextstart and dt <= nextend:
        dif = nextend - dt
        print('Notifying of pass for ' + str(dif.seconds) + ' seconds.')
        notify_pass(dif.seconds)
        nextstart = None
        while nextstart == None:
            nextstart,nextdur = get_next_pass()
            if nextstart == None:
                time.sleep(10)
        nextend = nextstart + datetime.timedelta(seconds=nextdur)
    time.sleep(60)
