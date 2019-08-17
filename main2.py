from PIL import Image

import LaserCtrl as lc
import EasyDriver as ed
import time
import numpy as np
import os
import sys
import argparse


class Worker:
    CW = True       # clockwise
    CCW = False     # counterclockwise

    def __init__(self, work_size, img_array):
        self.img_array = img_array
        self.work_size = work_size
        self.stepper_l = ed.EasyDriver(
            pin_step=40, pin_dir=38, delay=0.005)     # up
        self.stepper_r = ed.EasyDriver(
            pin_step=33, pin_dir=31, delay=0.0003)     # down
        self.laser = lc.LaserCtrl(pin_pwm=12)
        self.stepper_l.dir(self.CW)
        self.stepper_r.dir(self.CCW)
        self.laser_close()

    def laser_open(self, power=100):
        self.laser.ChangeDutyCycle(int(power))

    def laser_close(self):
        self.laser.ChangeDutyCycle(0)

    def eval(self):
        p = 0
        line = 0
        for limg in self.img_array:
            print('line: ' + str(line))
            line += 1
            print(limg)

            self.stepper_l.dir(self.CW)
            self.stepper_l.set_delay(0.005)
            for i in limg:
                if p != i:
                    p = i
                    self.laser_open((255 - i) / 256.0 * 100)
                self.stepper_l.step()

            self.laser_close()
            self.stepper_l.dir(self.CCW)
            self.stepper_l.set_delay(0.0001)
            for j in range(self.work_size):
                self.stepper_l.step()

            self.stepper_r.step()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, default='./pic.png',
                        help='The file name of picture to read. Default: ./pic.png')
    parser.add_argument('-r', type=str, default='stretch',
                        help='Method of resize the picture. You can choose "pad", "stretch". Default: "stretch"')
    parser.add_argument('-m', type=str, default='work',
                        help='mode: work, test')
    args = parser.parse_args()

    filename = args.f

    work_size = 2000

    if args.m == 'work':
        print('Load image file: ' + filename)
        img = Image.open(filename)
        img = img.convert('L')
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        rsz = img.resize((work_size, work_size))
        # rsz.show()
        img_array = np.array(rsz)
        # print(img_array)

        print('Load image succeed')
        worker = Worker(work_size, img_array)
        worker.eval()
        print('print succeed')

    elif args.m == 'test':
        print('Test for raspi laser engraving.')
        stepper_l = ed.EasyDriver(
            pin_step=40, pin_dir=38, delay=0.001)     # up
        stepper_r = ed.EasyDriver(
            pin_step=33, pin_dir=31, delay=0.001)     # down
        stepper_l.dir(True)   # CW
        stepper_r.dir(False)  # CCW

        for i in range(0, 1800):
            stepper_l.step()
            stepper_r.step()

    else:
        print('Unknown mode')
