import numpy as np
import Actions as ac
import EasyDriver as ed
import LaserCtrl as lc

# constant
CW = True       # clockwise
CCW = False     # counterclockwise

WORK_DELAY = 0.0003
STOP_DELAY = 0.0001


class Worker:
    def __init__(self, work_size):
        self.work_size = work_size
        self.stepper_x = ed.EasyDriver(
            pin_step=40, pin_dir=38, delay=STOP_DELAY)     # up
        self.stepper_y = ed.EasyDriver(
            pin_step=33, pin_dir=31, delay=STOP_DELAY)     # down
        self.stepper_x.dir(CW)
        self.stepper_y.dir(CCW)
        self.laser = lc.LaserCtrl(pin_pwm=12)
        self.laser_close()
        self.actions = ac.Actions()
        self.pos = (0, 0)

    def laser_open(self):
        self.stepper_x.set_delay(WORK_DELAY)
        self.laser.open()

    def laser_close(self):
        self.stepper_x.set_delay(STOP_DELAY)
        self.laser.close()

    def set_actions(self, actions):
        self.actions = actions

    def move_to(self, x, y):
        # Bresenham 算法画直线
        self.stepper_x.dir(CW) if self.pos[0] < x else self.stepper_x.dir(CCW)
        self.stepper_y.dir(CW) if self.pos[1] < y else self.stepper_y.dir(CCW)
        dx = abs(x - self.pos[0])
        dy = abs(y - self.pos[1])

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

        self.pos = (x, y)

    def eval(self):
        while not self.actions.empty():
            act = self.actions.top_pop()
            act_mode = act[0]

            if act_mode == ac.ACT_MOVE or act_mode == ac.ACT_WORK:
                _, x, y = act
                self.move_to(x, y)

            elif act_mode == ac.ACT_OPEN_LASER:
                self.laser_open()

            elif act_mode == ac.ACT_CLOSE_LASER:
                self.laser_close()
