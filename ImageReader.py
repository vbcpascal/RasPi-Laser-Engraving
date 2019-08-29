import argparse
import os

import cv2 as cv
import numpy as np

__author__ = "vbcpascal"
__version__ = "1.0"

# modes of handling pinctures
MODE_NONE = 0
MODE_CONTOURS = 1
MODE_GRAY = 2


class ImageReader:
    def __init__(self, filename, work_size=1800):
        self.__work_size = work_size
        self.__mode = MODE_NONE
        self.__gray_image = self.__read_cvt_pic(filename)

    def __read_cvt_pic(self, filename):
        print('Load image file:', filename)
        img = cv.imread(filename)
        img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        img = cv.resize(img, (self.__work_size, self.__work_size))
        return img

    def set_mode(self, mode):
        self.__mode = mode
        self.__init_mode()

    def get_mode(self):
        return self.__mode

    def __init_mode(self):
        if self.__mode == MODE_NONE:
            pass
        elif self.__mode == MODE_CONTOURS:
            self.__contours, _ = self.__gen_contours()
        elif self.__mode == MODE_GRAY:
            self.__floyd_image = self.__gen_floyd()

    def __gen_contours(self):
        _, thresh = cv.threshold(self.__gray_image, 127, 255, 0)
        contours, hierarchy = cv.findContours(
            thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return contours[1:], hierarchy

    def get_contours(self):
        if self.__mode != MODE_CONTOURS:
            raise('The mode should be MODE_CONTOURS to get contours.')
        return self.__contours

    def __gen_floyd(self):
        floyd_image = self.__gray_image.copy()
        for x in range(self.__work_size):
            for y in range(self.__work_size):
                old_pixel = self.__gray_image[x][y]
                new_pixel = 255 if old_pixel > 128 else 0
                floyd_image[x][y] = new_pixel
                quant_error = old_pixel - new_pixel
                try:
                    floyd_image[x][y + 1] += quant_error * 7.0 / 16
                    floyd_image[x + 1][y] += quant_error * 5.0 / 16
                    floyd_image[x + 1][y + 1] += quant_error * 1.0 / 16
                    floyd_image[x + 1][y - 1] += quant_error * 3.0 / 16
                except:
                    pass
        return floyd_image

    def get_floyd(self):
        if self.__mode != MODE_GRAY:
            raise('The mode should be MODE_GRAY to get floyd.')
        return self.__floyd_image

    def test_draw_contours(self):
        if self.__mode != MODE_CONTOURS:
            raise('The mode should be MODE_CONTOURS to draw contours.')
        height, width = self.__gray_image.shape
        contours_img = np.zeros((height, width), np.uint8)
        cv.drawContours(contours_img, self.__contours, -1, (255, 255, 255), 3)
        self.__show_img(contours_img, 'Contours')
        return

    def __show_img(self, img, title='Image'):
        img = cv.resize(img, (700, 700))
        cv.imshow(title, img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Read pictures and show contours.')
    parser.add_argument('file', metavar='file',
                        type=str, help='File name to read.')
    args = parser.parse_args()

    imr = ImageReader(args.file)
    imr.set_mode(MODE_CONTOURS)
    imr.test_draw_contours()
    contours = imr.get_contours()
    print('number of contours: ', len(contours))
