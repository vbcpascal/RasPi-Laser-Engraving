import argparse
import os
import sys
import time
from enum import Enum

import cv2 as cv
import numpy as np
from PIL import Image

import Actions

# modes of handling pinctures
MODE_NONE = 0
MODE_CONTOURS = 1
MODE_GRAY = 2


class ImageReader:
    def __init__(self, filename, work_size=2000):
        self.__mode = MODE_NONE
        self.__gray_image = self.__read_cvt_pic(filename, work_size)

    def set_mode(self, mode):
        self.__mode = mode
        self.__init_mode()

    def get_mode(self):
        return self.__mode

    def __read_cvt_pic(self, filename, work_size):
        print('Load image file:', filename)
        img = cv.imread(filename)
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        cv.resize(img, (work_size, work_size))
        return img

    def __init_mode(self):
        if self.__mode == MODE_NONE:
            pass
        elif self.__mode == MODE_CONTOURS:
            self.__contours, _ = self.__gen_contours()

    def __gen_contours(self):
        _, thresh = cv.threshold(self.__gray_image, 127, 255, 0)
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours[1:], hierarchy

    def show_img(self, img, title='Image'):
        cv.imshow(title, img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return

    def get_contours(self):
        if self.__mode != MODE_CONTOURS:
            raise('The mode should be MODE_CONTOURS to get contours.')
        return self.__contours

    def draw_contours(self):
        if self.__mode != MODE_CONTOURS:
            raise('The mode should be MODE_CONTOURS to draw contours.')
        height, width = self.__gray_image.shape
        contours_img = np.zeros((height, width), np.uint8)
        cv.drawContours(contours_img, self.__contours, -1, (255, 255, 255), 1)
        self.show_img(contours_img, 'Contours')
        return


if __name__ == "__main__":
    imw = ImageReader('pics\\logo.png')
    imw.set_mode(MODE_CONTOURS)
    imw.draw_contours()
