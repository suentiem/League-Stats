#!/usr/bin/python
# -*- coding: <encoding name> -*-

import mp3play

from time import sleep, time

from PIL import Image
from capture import screenshot_image, get_windows_bytitle, Screenshot
from ocr import *


def main_test():

    # Testing
    answers = [0,20,28,35,38,47,68,86,96,102,123,20,14,5,23,12,32,44,78,100,200,202,65,52,52,22]
    for index, answer in enumerate(answers):
        screenshot = Screenshot(Image.open('tests/screenshot{}.bmp'.format(index+1)))

        bounding_box = stats_box_find(screenshot)
        bounding_box = stats_box_trim(screenshot, bounding_box)

        result = get_numbers(screenshot, bounding_box, X_BOUNDS_CS, PIXEL_COLOR_TEXT)

        if not result == answer:
            print " -- WRONG {} ({} instead of {})".format(index+1, result, answer)
        else:
            print "{} OK ({})".format(index+1, result)

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