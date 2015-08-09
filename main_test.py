#!/usr/bin/python
# -*- coding: <encoding name> -*-

import mp3play

import os
from time import sleep, time

from PIL import Image
from capture import Screenshot
import ocr
from ocr import get_stats

def main_test():

    # Testing
    answers = [



        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,6],
        [0,0,0,0,0,25],
        [0,0,0,0,0,29],
        [1,0,1,0,0,38],
        [3,0,2,0,0,43],
        [3,1,2,0,0,73],
        None,
        [5,3,4,1,0,95],
        [5,3,4,1,0,95],
        [5,3,4,1,0,95],
        [5,3,4,1,0,95],
        [5,3,4,1,0,95],
        [5,3,4,1,0,95],
        [8,3,5,1,2,97],
        [13,5,10,1,2,106],
        [14,6,11,1,2,112],
        [17,8,14,1,2,126],
        [19,8,16,1,2,139],
        [20,8,17,1,2,143],
        [22,8,19,1,2,148],
        [22,8,19,1,2,157],
        [22,9,19,1,2,169],
        [26,10,23,1,2,186],
        [27,11,24,1,2,200],
        [32,11,25,1,2,221],
        [34,11,26,1,3,226],
        None,
        None,
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,2,0,1,0,26],
        [1,4,0,2,0,50],
        [2,5,0,2,0,62],
        [2,5,0,2,0,62],
        [4,12,1,3,0,81],
        [5,14,2,3,0,89],
        [11,15,5,4,2,105],
        [12,19,5,4,3,118],
        [15,24,8,5,3,135],
        [18,28,11,5,3,168],
        None,
        None,
        [27,36,17,6,4,270],
        [27,36,17,6,4,271],
        [32,40,19,6,5,291],
        [32,41,19,7,5,320],
        [33,43,19,7,5,320],
        [34,45,20,7,5,362],
        [40,46,24,7,6,387],
        [22,14,17,6,1,141],
        None,
        [13,7,8,4,1,120],
        None,
        [2,1,0,0,0,47],
        None,
        [13,7,8,4,1,122],
        [13,7,8,4,1,123],
        [22,14,17,6,1,141],
        None,
        None,
        None,
    ]
    for index, answer in list(enumerate(answers))[:]:
        screenshot = Screenshot(Image.open('test-newerui\\Screen{0:02}.png'.format(index+1)))
        results = get_stats(screenshot)
        if results:
            results = [results['team_kills'], results['team_deaths'], results['kills'], results['deaths'], results['assists'], results['CS'], ]

        correct = results is None and answer is None or results and answer and not [i for i in range(6) if not answer[i] == results[i]]
        wrong = [] if results is None or answer is None else [(results[i], answer[i]) for i in range(6) if not answer[i] == results[i]]

        if not correct:
            print " -- WRONG {} - {} - {}".format(index+1, results, u", ".join(["({} instead of {})".format(a,b) for a,b in wrong]))
        else:
            print "{} OK ({})".format(index+1, results)

    # X_BOUNDS_TEAM_KILLS = (0.0 / STATS_BOX_WIDTH, 42.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_TEAM_DEATHS = (59.0 / STATS_BOX_WIDTH, 101.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_CS = (299.0 / STATS_BOX_WIDTH, 339.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_KILLS = (127.0 / STATS_BOX_WIDTH, 167.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_DEATHS = (188.0 / STATS_BOX_WIDTH, 228.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_ASSISTS = (243.0 / STATS_BOX_WIDTH, 283.0 / STATS_BOX_WIDTH)
    # X_BOUNDS_TIME = (349.0 / STATS_BOX_WIDTH, 420.0 / STATS_BOX_WIDTH)

def main_screenshot():
    window = _get_windows_bytitle('League of Legends')[0]
    win32gui.SetForegroundWindow(window)
    sleep(0.01)
    screenshot_save(window, "-test-1")
    exit()

def main_test_1(number):
    ocr.dump_pics = True
    screenshot = Screenshot(Image.open('test-newerui\\Screen{0:02}.png'.format(number)))
    print get_stats(screenshot, debug=True)

main_test()
#main_test_1(65)