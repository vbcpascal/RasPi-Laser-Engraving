import argparse
import os
import sys
import time

import numpy as np

import Actions as ac
import ImageReader as ir
import Worker as wk

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', choices=['test', 'work'], default='test',
                        help='Mode: test, work.')
    parser.add_argument('-f', type=str, default='pics/pic.png',
                        help='The file name of picture or .npy file.')
    parser.add_argument('-n', type=int, default=2000,
                        help='Steps of stepping motor.')
    args = parser.parse_args()

    mode = args.m
    filename = args.f
    work_size = args.n

    worker = wk.Worker(work_size)

    if mode == 'test':
        worker.test()

    elif mode == 'work':
        if filename[-3:] == 'npy':
            worker.actions.load(filename)
        else:
            reader = ir.ImageReader(filename)
            reader.set_mode(ir.MODE_CONTOURS)
            contours = reader.get_contours()
            worker.actions.add_contours(contours)

        worker.eval()

    else:
        print('Unknown mode')
