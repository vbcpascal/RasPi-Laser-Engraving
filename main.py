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
    work_delay = 0.001
    stop_delay = 0.0001

    def __init__(self, work_size, work_list):
        self.work_list = work_list
        self.work_size = work_size
        self.stepper_l = ed.EasyDriver(
            pin_step=40, pin_dir=38, delay=self.work_delay)     # up
        self.stepper_r = ed.EasyDriver(
            pin_step=33, pin_dir=31)                 # down
        self.laser = lc.LaserCtrl(pin_pwm=12)
        self.stepper_l.dir(self.CW)
        self.stepper_r.dir(self.CCW)
        self.laser_close()

    def laser_open(self):
        self.stepper_l.set_delay(self.work_delay)
        self.laser.ChangeDutyCycle(100)

    def laser_close(self):
        self.stepper_l.set_delay(self.stop_delay)
        self.laser.ChangeDutyCycle(0)

    def eval(self):
        for i in range(self.work_size):
            print(i, end=': ')
            print(self.work_list[i])
            self.stepper_l.dir(self.CW)
            self.stepper_l.set_delay(self.work_delay)
            for p in self.work_list[i]:
                if p[1]:
                    self.laser_open()
                    for j in range(p[0]):
                        self.stepper_l.step()
                else:
                    self.laser_close()
                    for j in range(p[0]):
                        self.stepper_l.step()

            self.laser_close()
            self.stepper_l.dir(self.CCW)
            self.stepper_l.set_delay(self.stop_delay)
            for j in range(self.work_size):
                self.stepper_l.step()

            self.stepper_r.step()


def get_st(x):
    return True if x < 128 else False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, default='./pic.png',
                        help='The file name of picture to read. Default: ./pic.png')
    parser.add_argument('-r', type=str, default='stretch',
                        help='Method of resize the picture. You can choose "pad", "stretch". Default: "stretch"')
    parser.add_argument('-m', type=str, default='work',
                        help='mode: work, test')
    parser.add_argument('-n', type=str, default='',
                        help='use a .npy file instead of image')
    args = parser.parse_args()

    filename = args.f

    work_size = 2000

    if args.m == 'work' and args.n == '':
        print('Load image file: ' + filename)
        img = Image.open(filename)
        img = img.convert('L')
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        rsz = img.resize((work_size, work_size))
        # rsz.show()
        img_array = np.array(rsz)
        # print(img_array)

        print('Load image succeed')
        work_list = []

        for i in range(work_size):
            # print(i)
            work_line = []
            status = get_st(img_array[i][0])
            l = 0
            for j in range(work_size):
                if get_st(img_array[i][j]) != status:
                    work_line.append([l, status])
                    status = get_st(img_array[i][j])
                    l = 0
                l += 1
            work_line.append([l, status])
            work_list.append(work_line)

        print('Load image succeed')
        np.save('tmp.npy', work_list)

        worker = Worker(work_size, work_list)
        worker.eval()
        print('print succeed')

    elif args.m == 'work':
        work_list = np.load(args.n)
        worker = Worker(work_size, work_list)
        worker.eval()

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
