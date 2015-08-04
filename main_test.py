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
        [256,27,1,6,44,26],
        [247,26,1,6,43,26],
        [239,26,1,6,41,25],
        [234,23,1,6,38,25],
        [230,22,1,6,37,25],
        [213,20,1,6,33,20],
        [193,18,1,5,29,19],
        [191,17,1,5,28,19],
        [174,15,1,5,26,14],
        [166,14,1,5,25,14],
        [160,12,1,5,23,14],
        [157,11,1,5,22,14],
        [157,10,1,5,21,14],
        [151,10,1,2,18,13],
        [148,9,1,2,17,13],
        [143,8,1,2,15,13],
        [139,8,0,2,15,13],
        [124,7,0,2,14,10],
        [118,6,0,1,11,10],
        [115,5,0,1,10,9],
        [113,5,0,0,9,9],
        [90,4,0,0,7,5],
        [74,1,0,0,3,2],
        [53,0,0,0,2,1],
        [43,0,0,0,1,1],
        [40,0,0,0,1,1],
        [30,0,0,0,1,1],
        [20,0,0,0,1,1],
        [17,0,0,0,1,0],
        [11,0,0,0,0,0],
        [9,0,0,0,0,0],
        [7,0,0,0,0,0],
        [1,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [98,6,0,0,6,2],
        [102,6,0,0,6,2],
        [109,9,0,0,9,2],
        [124,9,0,0,9,2],
        [92,2,3,1,4,7],
        None,
        None,
        [4,0,0,0,0,0],
        [262,20,1,0,27,18],
        None,
        None,
    ]
    for index, answer in enumerate(answers):
        screenshot = Screenshot(Image.open('test-newui\\screenshot-{}.bmp'.format(index)))
        results = get_stats(screenshot)
        if results:
            results = [results['CS'], results['kills'], results['deaths'], results['assists'], results['team_kills'], results['team_deaths'], ]

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

def main_test_1():
    ocr.dump_pics = True
    screenshot = Screenshot(Image.open('test-newui\\screenshot-42.bmp'))
    print get_stats(screenshot, debug=True)

main_test()