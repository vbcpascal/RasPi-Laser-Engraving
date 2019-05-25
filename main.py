import LaserCtrl as lc
import EasyDriver as ed
import cv2
import time
import numpy as np
import os, sys
import argparse

class Worker:
    CW = True       # clockwise
    CCW = False     # counterclockwise

    def __init__(self, work_size, work_list):
        self.work_list = work_list
        self.work_size = work_size
        self.stepper_l = ed.EasyDriver(pin_step=40, pin_dir=38, delay=0.01)     # up
        self.stepper_r = ed.EasyDriver(pin_step=33, pin_dir=31)                 # down
        self.laser = lc.LaserCtrl(pin_pwm=12)
        self.stepper_l.dir(self.CW)
        self.stepper_r.dir(self.CW)
        self.laser_close()

    def laser_open(self, power):
        print('open')
        self.stepper_l.delay(0.1)

    def laser_close(self):
        print('close')
        self.stepper_l.delay(0.01)

    def eval(self):
        for i in range(self.work_size):
            print(self.work_list[i])
            self.stepper_l.dir(self.CW)
            self.stepper_l.delay(0.1)
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
            self.stepper_l.delay(0.0001)
            for j in range(self.work_size):
                self.stepper_l.step()

            self.stepper_r.step()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, default='./pic.png', help='The file name of picture to read. Default: ./pic.png')
    parser.add_argument('-r', type=str, default='stretch', help='Method of resize the picture. You can choose "pad", "stretch". Default: "stretch"')
    parser.add_argument('-n', type=str, default='none', help='import a .npy file instead of read a image')
    args = parser.parse_args()

    filename = args.f
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    work_size = 2000

    rsz = cv2.resize(img, (work_size, work_size))
    cv2.imshow('', rsz)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    input('Please manually adjust to the initial position.')
    
    work_list = []
    get_st = lambda x: True if x < 128 else False
    for i in range(work_size):
        work_line = []
        status = get_st(rsz[i][0])
        l = 0
        for j in range(work_size):
            if get_st(rsz[i][j]) != status:
                work_line.append([l, status])
                status = get_st(rsz[i][j])
                l = 0
            l += 1
        work_line.append([l, status])
        work_list.append(work_line)

    print('Load image succeed')
    
    worker = Worker(work_size, work_list)
    worker.eval()