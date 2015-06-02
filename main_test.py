#!/usr/bin/python
# -*- coding: <encoding name> -*-

import mp3play

from time import sleep, time

from PIL import Image
from capture import Screenshot
from ocr import get_stats


def main_test():

    # Testing
    answers = [
        [30,38,18,9,5,223],
        None,
        [28, 33, 16, 8, 5, 219],
        None,
        [0,1,0,1,0,4],
        [1,7,1,3,0,34],
        [6,13,5,5,0,76],
        [11,17,9,6,0,102],
        [22,27,14,7,3,194],
        None,
        [0,0,0,0,0,0],
        None,
        None,
        None,
        None,
        None,
        [20,6,16,2,1,154],
        None,
        [9,2,6,1,0,94],
        [16,2,13,1,0,120],
        [16,2,13,1,0,120],
    ]
    for index, answer in enumerate(answers):
        screenshot = Screenshot(Image.open('tests/screenshot_{}.bmp'.format(index+1)))
        results = get_stats(screenshot)
        if results:
            results = [results['team_kills'], results['team_deaths'], results['kills'], results['deaths'], results['assists'], results['CS']]

        correct = results is None and answer is None or results and answer and not [i for i in range(5) if not answer[i] == results[i]]

        if not correct:
            print " -- WRONG {} ({} instead of {})".format(index+1, results, answer)
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
    global dump_pics
    dump_pics = True
    screenshot = Screenshot(Image.open('tests/screenshot23.bmp'))

    bounding_box = stats_box_find(screenshot)
    out_debug(screenshot, bounding_box)
    if not bounding_box:
        print "No box found"
    bounding_box = stats_box_trim(screenshot, bounding_box)
    out_debug(screenshot, bounding_box)
    if not bounding_box:
        print "No box trimmed"

    print {
            'CS': get_numbers(screenshot, bounding_box, X_BOUNDS_CS, PIXEL_COLOR_TEXT),
            'team_kills': get_numbers(screenshot, bounding_box, X_BOUNDS_TEAM_KILLS, PIXEL_COLOR_TEXT_TEAM_KILLS),
            'team_deaths': get_numbers(screenshot, bounding_box, X_BOUNDS_TEAM_DEATHS, PIXEL_COLOR_TEXT_TEAM_DEATHS),
            'kills': get_numbers(screenshot, bounding_box, X_BOUNDS_KILLS, PIXEL_COLOR_TEXT),
            'deaths': get_numbers(screenshot, bounding_box, X_BOUNDS_DEATHS, PIXEL_COLOR_TEXT),
            'assists': get_numbers(screenshot, bounding_box, X_BOUNDS_ASSISTS, PIXEL_COLOR_TEXT),
        }


main_test()