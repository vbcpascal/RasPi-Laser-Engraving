import numpy as np
import Actions as ac
import EasyDriver as ed
import LaserCtrl as lc
from progressbar import *

# constant
CW = True       # clockwise
CCW = False     # counterclockwise

WORK_DELAY = 0.01
STOP_DELAY = 0.00025


class Worker:
    def __init__(self, work_size=2000):
        self.work_size = work_size
        self.stepper_x = ed.EasyDriver(
            pin_step=40, pin_dir=38, delay=STOP_DELAY)     # up
        self.stepper_y = ed.EasyDriver(
            pin_step=33, pin_dir=31, delay=STOP_DELAY)     # down
        self.stepper_x.dir(CW)
        self.stepper_y.dir(CW)
        self.laser = lc.LaserCtrl(pin_pwm=12)
        self.laser_close()
        self.actions = ac.Actions()
        self.pos = [0, 0]

    def laser_open(self):
        self.stepper_x.set_delay(WORK_DELAY)
        self.laser.open()

    def laser_close(self):
        self.stepper_x.set_delay(STOP_DELAY)
        self.laser.close()

    def set_actions(self, actions):
        self.actions = actions

    def move_to(self, x, y):
        # Bresenham Algorithm to draw a line
        # print(self.pos, x, y)
        self.stepper_x.dir(CW) if self.pos[0] < x else self.stepper_x.dir(CCW)
        self.stepper_y.dir(CW) if self.pos[1] < y else self.stepper_y.dir(CCW)
        dx = abs(x - self.pos[0])
        dy = abs(y - self.pos[1])

        self.pos = [x, y]

        x_step_f = self.stepper_x.step
        y_step_f = self.stepper_y.step

        if dx < dy:
            dx, dy = dy, dx
            x_step_f = self.stepper_y.step
            y_step_f = self.stepper_x.step

        error = dx // 2
        for x in range(dx):
            error = error - dy
            if error < 0:
                y_step_f()
                error = error + dx
            x_step_f()

    def eval(self):
        acts_len = self.actions.get_len()
        print(acts_len)
        pba = ProgressBar(acts_len).start()
        i = 1

        while not self.actions.empty():
            i += 1
            try:
                pba.update(i)
            except:
                print(i)
            act = self.actions.top_pop()
            self.eval_one(act)

        pba.finish()

    def eval_one(self, act):
        act_mode = act[0]

        if act_mode == ac.ACT_MOVE or act_mode == ac.ACT_WORK:
            _, x, y = act
            self.move_to(x, y)

        elif act_mode == ac.ACT_OPEN_LASER:
            self.laser_open()

        elif act_mode == ac.ACT_CLOSE_LASER:
            self.laser_close()

    def test(self):
        print('Test for raspi laser engraving.')
        self.stepper_x.dir(CW)
        self.stepper_y.dir(CW)

        for i in range(0, self.work_size):
            self.stepper_x.step()
            self.stepper_y.step()

        self.stepper_x.dir(CCW)
        self.stepper_y.dir(CCW)

        for i in range(0, self.work_size):
            self.stepper_x.step()
            self.stepper_y.step()
