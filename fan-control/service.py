#!/usr/bin/env python3

import os
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
p = GPIO.PWM(11, 200)

def get_temp():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=","").replace("'C\n",""))


last_dc = 0.0
while True:
    try:
        temp = get_temp()
        dc = 0.0
        if temp >= float(50):
            dc = 90.0
        elif temp < float(50) and temp >= float(40):
            dc = 50.0
        elif temp <float(40) and temp > float(35):
            dc = 20.0
        else:
            dc = 0.0
        if last_dc != dc:
            print("Current temp is {}, setting dc to {}".format(temp, dc))
            if last_dc == 0 and dc < 30:
                p.start(100)
                time.sleep(1.4)
            p.start(dc)
            last_dc = dc
        else:
            print("Current temp is {}, dc kept to {}".format(temp, dc))
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        GPIO.cleanup()
    except Exception as e:
        print('an error occurred: {}'.format(e))
    
    time.sleep(10)
