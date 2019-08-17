from PIL import Image
import LaserCtrl as lc
import EasyDriver as ed
import ReadPic as rp
import time
import numpy as np
import os
import sys
import argparse


class Worker:
    CW = True       # clockwise
    CCW = False     # counterclockwise
    work_delay = 0.0003
    stop_delay = 0.0001

    def __init__(self, work_size, work_list):
        self.work_list = work_list
        self.work_size = work_size
        self.stepper_l = ed.EasyDriver(
            pin_step=40, pin_dir=38, delay=self.work_delay)     # up
        self.stepper_r = ed.EasyDriver(
            pin_step=33, pin_dir=31, delay=0)                 # down
        self.laser = lc.LaserCtrl(pin_pwm=12)
        self.stepper_l.dir(self.CW)
        self.stepper_r.dir(self.CCW)
        self.laser_close()
        self.n = 2000 // work_size

    def laser_open(self):
        self.stepper_l.set_delay(self.work_delay)
        self.laser.ChangeDutyCycle(70)

    def laser_close(self):
        self.stepper_l.set_delay(self.stop_delay)
        self.laser.ChangeDutyCycle(0)

    def eval(self):
        i = 0
        for work_line in self.work_list:
            print(i, end=': ')
            print(work_line)
            self.stepper_l.dir(self.CW)
            self.stepper_l.set_delay(self.work_delay)

            work_step = 0
            while work_line:
                p = work_line[0]
                # print(p)
                if len(work_line) == 1 and p[1] == False:   # end this line
                    break

                if p[1]:
                    self.laser_open()
                    time.sleep(0.0001)
                else:
                    self.laser_close()

                work_step += p[0] * self.n
                for j in range(p[0] * self.n):
                    self.stepper_l.step()

                work_line = work_line[1:]

            self.laser_close()
            self.stepper_l.dir(self.CCW)

            print(work_step)
            for j in range(work_step):
                self.stepper_l.step()
            # print('back')
            for j in range(self.n):
                self.stepper_r.step()
                # print('~')
            # print('finish line')

            i += self.n


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

    work_size = 500    # 2000

    if args.m == 'work' and args.n == '':
        work_list = rp.ReadPic(filename=filename)
        worker = Worker(work_size, work_list)
        worker.eval()

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
