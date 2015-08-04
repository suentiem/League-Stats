#!/usr/bin/python
# -*- coding: <encoding name> -*-

import win32gui
import win32ui
import win32con

from PIL import Image

PIXEL_COLOR_BACKGROUND = (16, 28, 24), 14, 14
PIXEL_COLOR_BORDER = (23, 54, 54), 8, 40
PIXEL_COLOR_BORDER_EDGE = (16, 27, 27), 1, 40
PIXEL_COLOR_TEXT = (171, 171, 144), 85, 115
PIXEL_COLOR_TEXT_SPLITTER = (137, 142, 121), 35, 35
PIXEL_COLOR_ICON = (171, 171, 144), 45, 50
PIXEL_COLOR_BAR = (171, 171, 144), 45, 80
PIXEL_COLOR_TEXT_TEAM_BLUE = (1, 150, 220), 45, 65 # (47,140,181)
PIXEL_COLOR_TEXT_TEAM_RED = (232, 6, 6), 45, 65

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
    x = screenshot.width
    y = int(screenshot.height*19/20)

    minY, maxX, maxY, minX = None, None, None, None

    # First find the right border
    while x > 1:
        pixel = screenshot.pixel(x, y)
        match = pixel_match_fuzzy(PIXEL_COLOR_BORDER, pixel)

        if match:
            maxX = x
            break

        x -= 1
        if not x > 1:
            return None

    # Ride the border up to the top
    while y > 1:
        pixel = screenshot.pixel(x, y)
        match = pixel_match_fuzzy(PIXEL_COLOR_BORDER, pixel)

        if not match:
            minY = y
            break

        y -= 1
        if not y > 1:
            return None

    # Ride the border to the left until the edge
    y += 1
    while x > 1:
        pixel = screenshot.pixel(x, y)
        match = pixel_match_fuzzy(PIXEL_COLOR_BORDER, pixel, forgiving=True)

        if not match:
            minX = x
            break

        x -= 1
        if not x > 1:
            return None

    # Find the bottom bounds
    x += 1
    while y < screenshot.height:
        pixel = screenshot.pixel(x, y)
        match = pixel_match_fuzzy(PIXEL_COLOR_BORDER_EDGE, pixel)
        check = pixel_match_fuzzy(PIXEL_COLOR_BORDER, pixel, forgiving=True)

        if not check:
            return None

        if match:
            maxY = y
            break

        y += 1
        if not y < screenshot.height:
            return None

    # Ride the border to the left until the edge
    x = minX
    y = maxY - 1
    while x < maxX:
        pixel = screenshot.pixel(x, y)
        match = pixel_match_fuzzy(PIXEL_COLOR_BORDER, pixel, forgiving=True)

        if not match:
            return None

        x += 1

    return minY, maxX, maxY, minX

# trims a stats box by looking for kills and using that as the bounding height
def stats_box_trim(screenshot, bounding_box):
    min_y, max_x, max_y, min_x = bounding_box

    new_min_y = None
    new_max_y = None

    # Go through vertically and find the deaths
    found_ever = False
    x = max_x
    while x >= min_x:
        found_this_iteration = False

        y = min_y
        while y <= max_y:
            matched = pixel_match_fuzzy(PIXEL_COLOR_TEXT_TEAM_RED, screenshot.pixel(x,y))
            if matched:
                if new_min_y is None or y < new_min_y:
                    new_min_y = y
                if new_max_y is None or y > new_max_y:
                    new_max_y = y

                if not found_ever:
                    found_ever = True
                if not found_this_iteration:
                    found_this_iteration = True

            y += 1

        # If we found it before and never found it this time, we've passed it, return
        if found_ever and not found_this_iteration:
            return new_min_y, max_x, new_max_y, min_x

        x -= 1

    return None

def get_numbers(screenshot, bounding_box, x_bounds, pixel_color):

    box_width = bounding_box[1] - bounding_box[3]
    y_min = bounding_box[0]
    y_max = bounding_box[2]
    x_min, x_max = x_bounds

    out_debug(screenshot, (y_min, x_max, y_max, x_min), 'chunk')

    found = False
    found_last_iteration = False
    x = x_min
    x_start = None
    text_to_number_list = []
    while x <= x_max+1:
        y = y_min
        while y <= y_max:
            found = pixel_match_fuzzy(pixel_color, screenshot.pixel(x, y))
            if found:
                break
            y += 1

        if found and x <= x_max:
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

    #out_debug(screenshot, (y_min, x_max, y_max, x_min), 'piece', force=True)

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
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.45)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.38)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.6), y_min+int(height*0.6)), forgiving=True) or \
                        pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min+int(width*0.5), y_min+int(height*0.62)), forgiving=True) 
 
    # =====> 0 <=====
    if not mid_center_match:
        return [0]

    bottom_left_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max))
    bottom_right_match_strict = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_max, y_max))
    bottom_left_match = bottom_left_match_strict or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max), forgiving=True) \
                                                 or pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_max-int(height*0.1)), forgiving=True)
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

    bottom_mid_left_match = pixel_match_fuzzy(pixel_color, screenshot.pixel(x_min, y_min+int(height*0.8)-1), forgiving=True)

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

def find_block_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_ICON, fails_possible=0, forgiving=True):
    minY, maxX, maxY, _minX = bounding_box
    matchMinX = None
    matchMaxX = None

    found = False
    found_ever = False
    x = minX
    while x < maxX:
        matched = False
        y = minY
        while y < maxY:
            pixel = screenshot.pixel(x, y)
            match = pixel_match_fuzzy(color, pixel, forgiving=forgiving)

            if match:
                matched = True
                break

            y += 1

        if matched:
            fails_left = fails_possible
            found = True

            if not found_ever:
                found_ever = True
                matchMinX = x
        else:
            if found:
                if fails_left == fails_possible:
                    matchMaxX = x-1

                fails_left -= 1
                if fails_left <= 0:
                    return matchMinX, matchMaxX

        x += 1

    return None

def find_splitter_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_TEXT_SPLITTER, threshold=1, fails_possible=2, min_matches=3):
    minY, maxX, maxY, _minX = bounding_box
    matchMinX = None
    matchMaxX = None

    #print "== SPLIT ========="
    fails_left = 0
    x = minX
    x_matches = 0
    last_x_match_y = maxY
    # Detect thin pixel areas
    while x < maxX:
        y_touches = 0
        last_match = False
        last_match_y = maxY
        y = maxY

        while y >= minY:
            pixel = screenshot.pixel(x, y)
            match = pixel_match_fuzzy(color, pixel, forgiving=True)

            if match and not last_match:
                y_touches += 1

            if y_touches > threshold:
                last_match_y = maxY
                x_matches = 0
            
            if match:
                last_match_y = y

            last_match = match

            y -= 1

        if y_touches == 0:
            if fails_left >= 0:
                fails_left -= 1
            elif x_matches >= min_matches:
                return matchMinX, matchMaxX
            else:
                x_matches = 0
                last_x_match_y = maxY
        elif y_touches > threshold or \
                last_match_y > last_x_match_y or \
                x_matches == 0 and last_match_y < (maxY-minY)*2/3+minY:

            if x_matches >= min_matches:
                return matchMinX, matchMaxX
            x_matches = 0
            last_x_match_y = maxY
        else:
            if x_matches == 0:
                matchMinX = x
            matchMaxX = x
            x_matches += 1
            fails_possible = fails_left

        last_x_match_y = last_match_y

        #print "splitter: {} {}".format(y_touches, x_matches)

        x += 1

    return None

dump_pics = False
current_numbers = {}
def out_debug(screenshot, bounding_box, name='out', force=False):
    if not dump_pics and not force:
        return
    current_number = current_numbers.get(name, 0)
    crop_box = (bounding_box[3], bounding_box[0], bounding_box[1]+1, bounding_box[2]+1)
    screenshot_box = screenshot.image.crop(crop_box)
    screenshot_box.save('output/{}{}.bmp'.format(name, current_number))
    current_numbers[name] = current_number+1

def get_stats(screenshot, debug=False):

    bounding_box = stats_box_find(screenshot)
    if not bounding_box:
        return None
    if debug:
        print ("Found Box: {}".format(bounding_box))
        out_debug(screenshot, bounding_box, force=True)

    bounding_box = stats_box_trim(screenshot, bounding_box)
    if not bounding_box:
        return None
    if debug:
        print ("Trim Box: {}".format(bounding_box))
        out_debug(screenshot, bounding_box, force=True)

    # Find minion kills
    minY, maxX, maxY, minX = bounding_box

    minion_icon_bounds = find_block_x(screenshot, bounding_box, minX, color=PIXEL_COLOR_ICON)
    minion_kills_bounds_x = find_block_x(screenshot, bounding_box, minion_icon_bounds[1]+1, fails_possible=10)
    kda_icon_bounds = find_block_x(screenshot, bounding_box, minion_kills_bounds_x[1]+1, color=PIXEL_COLOR_ICON)
    kda_bounds_x = find_block_x(screenshot, bounding_box, kda_icon_bounds[1]+1, fails_possible=10)
    team_red_kills_x = find_block_x(screenshot, bounding_box, kda_bounds_x[1]+1, color=PIXEL_COLOR_TEXT_TEAM_RED, fails_possible=10)
    team_blue_kills_x = find_block_x(screenshot, bounding_box, kda_bounds_x[1]+1, color=PIXEL_COLOR_TEXT_TEAM_BLUE, fails_possible=10)

    is_player_red = True if team_red_kills_x[0] < team_blue_kills_x[0] else False
    team_kills_x = team_red_kills_x if is_player_red else team_blue_kills_x
    team_deaths_x = team_red_kills_x if not is_player_red else team_blue_kills_x

    kills_deaths_splitter_bounds_x = find_splitter_x(screenshot, bounding_box, kda_bounds_x[0])
    deaths_assists_splitter_bounds_x = find_splitter_x(screenshot, bounding_box, kills_deaths_splitter_bounds_x[1]+1)

    kills_bounds_x = [kda_bounds_x[0], kills_deaths_splitter_bounds_x[0]-2]
    deaths_bounds_x = [kills_deaths_splitter_bounds_x[1]+2, deaths_assists_splitter_bounds_x[0]-2]
    assists_bounds_x = [deaths_assists_splitter_bounds_x[1]+2, kda_bounds_x[1]]

    if debug:
        out_debug(screenshot, [minY, minion_kills_bounds_x[1], maxY, minion_kills_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, kda_bounds_x[1], maxY, kda_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, team_kills_x[1], maxY, team_kills_x[0]], force=True)
        out_debug(screenshot, [minY, team_deaths_x[1], maxY, team_deaths_x[0]], force=True)
        out_debug(screenshot, [minY, kills_bounds_x[1], maxY, kills_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, deaths_bounds_x[1], maxY, deaths_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, assists_bounds_x[1], maxY, assists_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, kills_deaths_splitter_bounds_x[1], maxY, kills_deaths_splitter_bounds_x[0]], force=True)
        out_debug(screenshot, [minY, deaths_assists_splitter_bounds_x[1], maxY, deaths_assists_splitter_bounds_x[0]], force=True)


    return {
        'team_kills': get_numbers(screenshot, bounding_box, team_kills_x, PIXEL_COLOR_TEXT_TEAM_RED if is_player_red else PIXEL_COLOR_TEXT_TEAM_BLUE),
        'team_deaths': get_numbers(screenshot, bounding_box, team_deaths_x, PIXEL_COLOR_TEXT_TEAM_RED if not is_player_red else PIXEL_COLOR_TEXT_TEAM_BLUE),
        'kills': get_numbers(screenshot, bounding_box, kills_bounds_x, PIXEL_COLOR_TEXT),
        'deaths': get_numbers(screenshot, bounding_box, deaths_bounds_x, PIXEL_COLOR_TEXT),
        'assists': get_numbers(screenshot, bounding_box, assists_bounds_x, PIXEL_COLOR_TEXT),
        'CS': get_numbers(screenshot, bounding_box, minion_kills_bounds_x, PIXEL_COLOR_TEXT),
    }