#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import pigpio

INPUT = 3
OUTPUT = 2

pi = pigpio.pi()
#pi.set_mode(OUTPUT, pigpio.OUTPUT)
pi.set_mode(INPUT, pigpio.INPUT)
pi.set_pull_up_down(OUTPUT, pigpio.PUD_DOWN)

while True:
    print(pi.read(INPUT))
    if(pi.read(INPUT)==1):
        print("Switch OFF")
    else:
        print("Switch ON")
    time.sleep(2)

#sudo pigpiodを実行すること
