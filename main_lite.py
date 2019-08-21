# An example program without using OpenCV

import argparse
import os
import sys
import time

import numpy as np

import Actions as ac
import Worker as wk

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', choices=['test', 'work'], default='test',
                        help='Mode: test, work.')
    parser.add_argument('-f', type=str, default='cache/logo.npy',
                        help='The file name of .npy file.')
    parser.add_argument('-n', type=int, default=1800,
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
            print('Reading picture files is not supported in main_lite.')
            os._exit(0)

        worker.eval()

    else:
        print('Unknown mode')
