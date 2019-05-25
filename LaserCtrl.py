#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 提供LaserCtrl类及相关方法，用于控制激光头

import RPi.GPIO as gpio
import time

__author__ = 'vbcpascal'
__version__ = '0.1'

class LaserCtrl(object):
    def __init__(self, pin_pwm=None, frequency=50,
        gpio_mode="BOARD"):
        self.pin_pwm = pin_pwm
        self.frequency = frequency

        if (gpio_mode == "BCM"):
            gpio.setmode(gpio.BCM)
        else:
            gpio.setmode(gpio.BOARD)

        if self.pin_pwm != None:
            gpio.setup(pin_pwm, gpio.OUT)
            self.p = gpio.PWM(pin_pwm, frequency)     # set frequency
            self.p.start(0)

    def ChangeDutyCycle(self, i):
        self.p.ChangeDutyCycle(i)
 
    def finish(self):
        self.p.ChangeDutyCycle(0)
        self.p.stop()

if __name__ == '__main__':
    p = LaserCtrl(pin_pwm=12)
    max_range = 30
    wait_time = 0.1

    try:
        while True:
            i = int(input('power: '))
            p.ChangeDutyCycle(i)

        '''
        while True:
            for i in range(0, max_range + 1, 5):
                print(i)
                p.ChangeDutyCycle(i)
                time.sleep(wait_time)
            for i in range(max_range, -1, -5):
                print(i)
                p.ChangeDutyCycle(i)
                time.sleep(wait_time)
        '''
    except KeyboardInterrupt:
        print('close')
        p.ChangeDutyCycle(0)
        p.finish()