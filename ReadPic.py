from PIL import Image
import time
import numpy as np
import os
import sys
import argparse


def get_st(x):
    return True if x < 128 else False


def ReadPic(filename='pic.png', npyname='tmp.npy', mode='none'):

    work_size = 500    # 2000

    print('Load image file: ' + filename)
    img = Image.open(filename)
    img = img.convert('L')
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    rsz = img.resize((work_size, work_size))
    # rsz.show()
    img_array = np.array(rsz)
    # print(img_array)

    if mode != 'none':
        for x in range(work_size):
            for y in range(work_size):
                oldpixel = img_array[x][y]
                newpixel = 255 if oldpixel > 128 else 0
                img_array[x][y] = newpixel
                quant_error = oldpixel - newpixel
                try:
                    img_array[x][y + 1] = img_array[x][y + 1] + \
                        quant_error * 7.0 / 16
                    img_array[x + 1][y] = img_array[x + 1][y] + \
                        quant_error * 5.0 / 16
                    img_array[x + 1][y + 1] = img_array[x + 1][y + 1] + \
                        quant_error * 1.0 / 16
                    img_array[x + 1][y - 1] = img_array[x + 1][y - 1] + \
                        quant_error * 3.0 / 16
                except:
                    pass

        # 8-bit pixels, black and white
        img = Image.fromarray(np.uint8(img_array), 'L')
    img.show()
    img.save('tmp.png')

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

    print('Get work_list succeed')
    np.save(npyname, work_list)

    print('Save npy succeed')
    return work_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, default='pic.png',
                        help='The file name of picture to read. Default: pic.png')
    parser.add_argument('-n', type=str, default='tmp.npy')
    parser.add_argument('-m', type=str, default='none')
    args = parser.parse_args()

    ReadPic(filename=args.f, npyname=args.n, mode=args.m)
