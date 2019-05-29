import RPi.GPIO as GPIO
import time
import datetime
import requests
import random
#import httplib.request
import urllib.request
import webbrowser
new=2
import string

GPIO.setmode(GPIO.BCM)

led = 4
GPIO.setup(led, GPIO.OUT)
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization


trig = 23
echo = 25
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
GPIO.output(trig, False)
def thingspeak_post():
#    threading.Timer(15,thingspeak_post).start()
    val= checkdist()
    

    URL='https://api.thingspeak.com/update?api_key='
    KEY='dnF7wLhWwD9hBfvKlN-AKH'
    HEADER='&field1={}&field2={}'.format(val,val)
    NEW_URL=URL+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)

def checkdist():
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    t1 = time.time()
    t2 = time.time()
    while GPIO.input(echo) == 0:
        t1 = time.time()
    while GPIO.input(echo) == 1:
        t2 = time.time()
    distance = (t2-t1)*34300/2
    return distance


pwm = GPIO.PWM(led, 80)

pwm.start(0)
try:
    while True:
        distance = checkdist()
        print("distance = %.1f cm" % distance)
        time.sleep(1)
        if   45<checkdist()<50:
            pwm.ChangeDutyCycle(10)
        elif 40<checkdist()<45:
            pwm.ChangeDutyCycle(20)
        elif 35<checkdist()<40:
            pwm.ChangeDutyCycle(30)
        elif 30<checkdist()<35:
            pwm.ChangeDutyCycle(40)
        elif 25<checkdist()<30:
            pwm.ChangeDutyCycle(60)
        elif 20<checkdist()<25:
            pwm.ChangeDutyCycle(70)
        elif 15<checkdist()<20:
            pwm.ChangeDutyCycle(80)
        elif 10<checkdist()<15:
            pwm.ChangeDutyCycle(90)
        elif 5<checkdist()<10:
            pwm.ChangeDutyCycle(100)
        else:
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(12.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            time.sleep(0.5)
        URl = "file:///home/pi/photon.html"
        webbrowser.open(URl, new=new)
        r = requests.get("https://maker.ifttt.com/trigger/work_complete/with/key/dnF7wLhWwD9hBfvKlN-AKH/" )
        #webbrowser.open(URl, new=new)
except KeyboardInterrupt:
	pass

pwm.stop()

GPIO.cleanup()
