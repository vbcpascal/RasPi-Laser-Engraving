#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 提供EasyDriver类及相关方法，用于控制电机

import RPi.GPIO as gpio
import time
import sys

__author__ = "vbcpascal"
__version__ = "0.1"


class EasyDriver(object):
    def __init__(self, pin_step=None, pin_dir=None, pin_ms1=None,
                 pin_ms2=None, pin_slp=None, pin_rst=None, pin_enable=None,
                 delay=1, gpio_mode="BOARD"):
        self.pin_step = pin_step
        self.pin_dir = pin_dir
        self.pin_ms1 = pin_ms1
        self.pin_ms2 = pin_ms2
        self.pin_slp = pin_slp
        self.pin_rst = pin_rst
        self.pin_enable = pin_enable
        self.delay = delay

        if (gpio_mode == "BCM"):
            gpio.setmode(gpio.BCM)
        else:
            gpio.setmode(gpio.BOARD)

        if self.pin_step != None:
            gpio.setup(self.pin_step, gpio.OUT)

        if self.pin_dir != None:
            gpio.setup(self.pin_dir, gpio.OUT)
            gpio.output(self.pin_dir, True)

        if self.pin_ms1 != None:
            gpio.setup(self.pin_ms1, gpio.OUT)
            gpio.output(self.pin_ms1, False)

        if self.pin_ms2 != None:
            gpio.setup(self.pin_ms2, gpio.OUT)
            gpio.output(self.pin_ms2, False)

        if self.pin_slp != None:
            gpio.setup(self.pin_slp, gpio.OUT)
            gpio.output(self.pin_slp, True)

        if self.pin_rst != None:  # > 0
            gpio.setup(self.pin_rst, gpio.OUT)
            gpio.output(self.pin_rst, True)

        if self.pin_enable != None:  # > 0
            gpio.setup(self.pin_enable, gpio.OUT)
            gpio.output(self.pin_enable, False)

    def step(self):
        # print("step true")
        gpio.output(self.pin_step, True)
        time.sleep(self.delay)
        # print("step false")
        gpio.output(self.pin_step, False)
        time.sleep(self.delay)

    def dir(self, dir):
        # print("change to: " + str(dir))
        gpio.output(self.pin_dir, dir)
        gpio.output(self.pin_dir, dir)
        gpio.output(self.pin_dir, dir)
        gpio.output(self.pin_dir, dir)

    def set_full_step(self):
        gpio.output(self.pin_ms1, False)
        gpio.output(self.pin_ms2, False)

    def set_half_step(self):
        gpio.output(self.pin_ms1, True)
        gpio.output(self.pin_ms2, False)

    def set_quarter_step(self):
        gpio.output(self.pin_ms1, False)
        gpio.output(self.pin_ms2, True)

    def set_eight_step(self):
        gpio.output(self.pin_ms1, True)
        gpio.output(self.pin_ms2, True)

    def slp(self):
        gpio.output(self.pin_slp, False)

    def wake(self):
        gpio.output(self.pin_slp, True)

    def enable(self):
        gpio.output(self.pin_enable, False)

    def disable(self):
        gpio.output(self.pin_enable, True)

    def rst(self):
        gpio.output(self.pin_rst, False)
        time.sleep(1)
        gpio.output(self.pin_rst, True)

    def set_delay(self, delay):
        self.delay = delay

    def finish(self):
        gpio.cleanup()


if __name__ == '__main__':
    CW = True       # clockwise
    CCW = False     # counterclockwise

    stepper_x = EasyDriver(pin_step=40, pin_dir=38, delay=0.0001)
    stepper_y = EasyDriver(pin_step=33, pin_dir=31, delay=0.0001)

    try:
        stepper_x.dir(CW)
        stepper_y.dir(CW)
        for i in range(0, 500):
            stepper_y.step()
            stepper_x.step()

        print('change')

        stepper_x.dir(CCW)
        stepper_y.dir(CCW)
        for i in range(0, 500):
            stepper_y.step()
            stepper_x.step()
    except KeyboardInterrupt:
        pass

    # clean up
    print('close')
    stepper_x.finish()
