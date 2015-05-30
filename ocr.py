#!/usr/bin/python
# -*- coding: <encoding name> -*-

import win32gui
import win32ui
import win32con

from PIL import Image

PIXEL_COLOR_BACKGROUND = (7, 20, 20), 14, 14
PIXEL_COLOR_BORDER = (73, 73, 73), 22, 40
PIXEL_COLOR_TEXT = (244, 244, 244), 85, 180
PIXEL_COLOR_TEXT_TEAM_KILLS = (57, 171, 227), 85, 180 # (47,140,181)
PIXEL_COLOR_TEXT_TEAM_DEATHS = (226, 47, 48), 85, 180

STATS_BOX_WIDTH = 423.0
X_BOUNDS_TEAM_KILLS = (0.0 / STATS_BOX_WIDTH, 40.0 / STATS_BOX_WIDTH)
X_BOUNDS_TEAM_DEATHS = (59.0 / STATS_BOX_WIDTH, 96.0 / STATS_BOX_WIDTH)
X_BOUNDS_CS = (299.0 / STATS_BOX_WIDTH, 339.0 / STATS_BOX_WIDTH)
X_BOUNDS_KILLS = (127.0 / STATS_BOX_WIDTH, 167.0 / STATS_BOX_WIDTH)
X_BOUNDS_DEATHS = (188.0 / STATS_BOX_WIDTH, 228.0 / STATS_BOX_WIDTH)
X_BOUNDS_ASSISTS = (243.0 / STATS_BOX_WIDTH, 283.0 / STATS_BOX_WIDTH)
X_BOUNDS_TIME = (349.0 / STATS_BOX_WIDTH, 420.0 / STATS_BOX_WIDTH)

def pixel_match_fuzzy(template, input, forgiving=False):
    values = template[0]
    max_variance = template[2 if forgiving else 1]
    for index, value in enumerate(values):
        if abs(input[index] - value) > max_variance:
            return False
    return True

# Returns top, right, bottom, left - or None
def stats_box_find(screenshot):
    x = int(screenshot.width - 15)
    y = 0
    maxY = int(screenshot.height/10)

    while y < maxY:
        pixel = screenshot.pixel(x, y)
        match = pixel_match_fuzzy(PIXEL_COLOR_BORDER, pixel)
        
        if match:
            minX = x-1
            maxX = x+1

            minY = y
            maxY = y+1

            # Min X
            while pixel_match_fuzzy(PIXEL_COLOR_BORDER, screenshot.pixel(minX, y), forgiving=True):
                minX -= 1
            # Max X
            while pixel_match_fuzzy(PIXEL_COLOR_BORDER, screenshot.pixel(maxX, y), forgiving=True):
                maxX += 1

            # Max Y
            while pixel_match_fuzzy(PIXEL_COLOR_BORDER, screenshot.pixel(x, maxY)):
                maxY += 1
            minY = maxY-1
            maxY += 10
            while not pixel_match_fuzzy(PIXEL_COLOR_BORDER, screenshot.pixel(x, maxY)):
                maxY += 1
            maxY -= 1


            return minY, maxX, maxY, minX
        else:
            y += 1

    return None

# trims a stats box by looking for kills and using that as the bounding height
def stats_box_trim(screenshot, bounding_box):
    min_y, max_x, max_y, min_x = bounding_box

    new_min_y = None
    new_max_y = None
    new_min_x = None

    # Go through vertically and find the kills
    found_ever = False
    x = min_x
    while x <= max_x:
        found_this_iteration = False

        y = min_y
        while y <= max_y:
            matched = pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_KILLS, screenshot.pixel(x,y))
            if matched:
                if new_min_y is None or y < new_min_y:
                    new_min_y = y
                if new_max_y is None or y > new_max_y:
                    new_max_y = y

                if not found_ever:
                    new_min_x = x
                    found_ever = True
                if not found_this_iteration:
                    found_this_iteration = True

            y += 1

        # If we found it before and never found it this time, we've passed it, return
        if found_ever and not found_this_iteration:
            return new_min_y, max_x, new_max_y, min_x

        x += 1

    return None



def get_numbers(screenshot, bounding_box, x_bounds, pixel_color):

    box_width = bounding_box[1] - bounding_box[3]
    y_min = bounding_box[0]
    y_max = bounding_box[2]
    x_min = int(round(x_bounds[0] * box_width)) + bounding_box[3]
    x_max = int(round(x_bounds[1] * box_width)) + bounding_box[3]


    out_debug(screenshot, (y_min, x_max, y_max, x_min), 'chunk')


    found_last_iteration = False
    x = x_min
    x_start = None
    text_to_number_list = []
    while x <= x_max:
        found = found_last_iteration
        y = y_min
        while y <= y_max:
            found = pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y))
            if found:
                break
            y += 1

        if found:
            if not found_last_iteration:
                x_start = x
        else:
            if found_last_iteration:
                #print "DO OCR"
                text_to_number = get_number_ocr(screenshot, (y_min, x-1, y_max, x_start), pixel_color)
                text_to_number_list.extend(text_to_number)
                #print " -- {}".format(text_to_number)

        found_last_iteration = found
        x += 1

    #return text_to_number_list
    return int("".join([str(num) for num in text_to_number_list]))

def get_number_ocr(screenshot, bounding_box, pixel_color):
    y_min, x_max, y_max, x_min = bounding_box
    height = float(y_max - y_min)+1
    width = float(x_max - x_min)+1

    #print "OCR {} {} {}".format(width, height, height/width)

    # merged character 3x check
    if height/width < .55:
        chunk_width = int(width/3.45)
        chunk_separator = int((width - chunk_width*3) / 2)
        return get_number_ocr(screenshot, (y_min, x_min+chunk_width, y_max, x_min), pixel_color) + \
                get_number_ocr(screenshot, (y_min, x_min+chunk_width*2+chunk_separator, y_max, x_min+chunk_width+chunk_separator), pixel_color) + \
                get_number_ocr(screenshot, (y_min, x_max, y_max, x_max-chunk_width), pixel_color)

    # merged character 2x check
    if height/width < 1:
        half_width = int(width/2.3)
        return get_number_ocr(screenshot, (y_min, x_min+half_width, y_max, x_min), pixel_color) + \
                get_number_ocr(screenshot, (y_min, x_max, y_max, x_max-half_width), pixel_color)

    out_debug(screenshot, (y_min, x_max, y_max, x_min), 'piece')

    # Trim the top and bottom
    found_trim_point = False
    y = y_min
    while y <= y_max and not found_trim_point:
        x = x_min
        while x <= x_max and not found_trim_point:
            if pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y)):
                found_trim_point = True
                y_min = y
            x += 1   
        y += 1 

    found_trim_point = False
    y = y_max
    while y >= y_min and not found_trim_point:
        x = x_min
        while x <= x_max and not found_trim_point:
            if pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y)):
                found_trim_point = True
                y_max = y
            x += 1   
        y -= 1 

    height = float(y_max - y_min)+1

    out_debug(screenshot, (y_min, x_max, y_max, x_min), 'piece-trimmed')

    # =====> 1 <=====
    if height/width > 3.0:
        return [1]

    mid_center_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.5)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.6)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.45)), forgiving=True) 
 
    # =====> 0 <=====
    if not mid_center_match:
        return [0]

    bottom_left_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max))
    bottom_right_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_max))
    bottom_left_match = bottom_left_match_strict or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max), forgiving=True)
    bottom_right_match = bottom_right_match_strict or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max-1, y_max), forgiving=True)

    bottom_mid_center_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.7)))
    mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.5)), forgiving=True)

    #print " stat {}-{} {}-{} {}".format(bottom_left_match_strict, bottom_left_match, bottom_right_match_strict, bottom_right_match, bottom_mid_center_match)


    top_left_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min))
    top_right_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min))
    top_left_match = top_left_match_strict or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min), forgiving=True)
    top_right_match = top_right_match_strict or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min), forgiving=True)
    top_mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.25)), forgiving=True)
    #print " stat2 {} {}".format(top_left_match, top_right_match)

    top_mid_center_right_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.8), y_min+int(height*0.25)), forgiving=True)

    # =====> 4 <=====
    if not bottom_left_match and not top_left_match and top_mid_center_right_match and not top_mid_left_match:
        return [4]

    #print " stat4 {} {} {} {}".format(bottom_left_match, top_left_match, bottom_right_match, top_right_match)
    bottom_mid_right_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min+int(height*0.75)), forgiving=True)

    # =====> 2 <=====
    if not bottom_mid_right_match and bottom_right_match:
        return [2]

    # =====> 7 <=====
    if not bottom_mid_right_match and not top_mid_left_match:
        return [7]

    #print " stat7 {} {} {} {} {}".format(bottom_left_match, top_left_match, bottom_right_match, top_right_match, top_mid_left_match)


    top_mid_left_center_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.15), y_min+int(height*0.4)))

    top_mid_right_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_min+int(height*0.25)), forgiving=True)

    # =====> 3 <=====
    if not top_mid_left_match and not top_mid_left_center_match and top_mid_right_match:
        return [3]

    bottom_mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.75)-1), forgiving=True)

    #print " stat3 {} {} {} {}".format(mid_center_match, top_mid_left_match, bottom_mid_left_match, top_mid_left_center_match)

    # =====> 6 <=====
    if not top_mid_right_match and bottom_mid_left_match:
        return [6]

    # =====> 5 <=====
    if not top_mid_right_match:
        return [5]

    # =====> 8 <=====
    if bottom_mid_left_match:
         return [8]

    # =====> 9 <=====
    return [9]

dump_pics = False
current_numbers = {}
def out_debug(screenshot, bounding_box, name='out'):
    if not dump_pics:
        return
    current_number = current_numbers.get(name, 0)
    crop_box = (bounding_box[3], bounding_box[0], bounding_box[1]+1, bounding_box[2]+1)
    screenshot_box = screenshot.image.crop(crop_box)
    screenshot_box.save('{}{}.bmp'.format(name, current_number))
    current_numbers[name] = current_number+1



def get_stats(screenshot):
    bounding_box = stats_box_find(screenshot)
    if not bounding_box:
        return None

    bounding_box = stats_box_trim(screenshot, bounding_box)
    if not bounding_box:
        return None

    return {
        'team_kills': get_numbers(screenshot, bounding_box, X_BOUNDS_TEAM_KILLS, PIXEL_COLOR_TEXT_TEAM_KILLS),
        'team_deaths': get_numbers(screenshot, bounding_box, X_BOUNDS_TEAM_DEATHS, PIXEL_COLOR_TEXT_TEAM_DEATHS),
        'kills': get_numbers(screenshot, bounding_box, X_BOUNDS_KILLS, PIXEL_COLOR_TEXT),
        'deaths': get_numbers(screenshot, bounding_box, X_BOUNDS_DEATHS, PIXEL_COLOR_TEXT),
        'assists': get_numbers(screenshot, bounding_box, X_BOUNDS_ASSISTS, PIXEL_COLOR_TEXT),
        'CS': get_numbers(screenshot, bounding_box, X_BOUNDS_CS, PIXEL_COLOR_TEXT),
    }