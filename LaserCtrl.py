#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 提供LaserCtrl类及相关方法，用于控制激光头

import RPi.GPIO as gpio
import time

__author__ = 'vbcpascal'
__version__ = '1.0'

OPENED = True
CLOSED = False


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

        self.status = CLOSED

    def open(self):
        self.change_duty_cycle(85)
        self.status = OPENED

    def close(self):
        self.change_duty_cycle(0)
        self.status = CLOSED

    def get_status(self):
        return self.status

    def change_duty_cycle(self, i):
        self.p.ChangeDutyCycle(i)

    def finish(self):
        self.p.ChangeDutyCycle(0)
        self.p.stop()

    def test(self):
        try:
            while True:
                try:
                    i = int(input('power: '))
                    self.change_duty_cycle(i)
                except:
                    print('error input. Please input a number between 1 and 100.')
        except KeyboardInterrupt:
            print('close')
            self.finish()


if __name__ == '__main__':
    p = LaserCtrl(pin_pwm=12)
    p.test()
