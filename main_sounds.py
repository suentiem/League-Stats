#!/usr/bin/python
# -*- coding: <encoding name> -*-

import mp3play

from time import sleep, time

from capture import screenshot_image, get_windows_bytitle
from ocr import get_numbers, stats_box_trim, stats_box_find

VOLUME = 50

def main():
    clip_sonic = mp3play.load("sounds/sonic_ring.mp3")
    clip_hitmarker = mp3play.load("sounds/hitmarker.mp3")
    clip_airporn = mp3play.load("sounds/airporn.mp3")
    clip_airhorn = mp3play.load("sounds/airhorn.mp3")
    clip_fart = mp3play.load("sounds/fart.mp3")
    clip_2sed = mp3play.load("sounds/2sed4airhorn.mp3")
    clip_wow = mp3play.load("sounds/wow.mp3")
    clip_triple = mp3play.load("sounds/triple.mp3")
    clip_mom_get_the_camera = mp3play.load("sounds/mom_get_the_camera.mp3")
    clip_ohmygod = mp3play.load("sounds/ohmygod.mp3")
    clip_skrillex = mp3play.load("sounds/skrillex.mp3")



    clip_sonic.volume(VOLUME)
    clip_hitmarker.volume(VOLUME)
    clip_airporn.volume(VOLUME)
    clip_airhorn.volume(VOLUME)
    clip_fart.volume(VOLUME)
    clip_2sed.volume(VOLUME)
    clip_wow.volume(VOLUME)
    clip_triple.volume(VOLUME)
    clip_mom_get_the_camera.volume(VOLUME)
    clip_ohmygod.volume(VOLUME)
    clip_skrillex.volume(VOLUME)


    lastResults = None

    kill_spree = (0,0)

    while True:
        sleep(0.1)

        windows = get_windows_bytitle('League of Legends')
        if windows:
            window = windows[0]

            try:
                screenshot = Screenshot(screenshot_image(window))

                bounding_box = stats_box_find(screenshot)
                if not bounding_box:
                    print "No box found"
                    continue

                bounding_box = stats_box_trim(screenshot, bounding_box)

                results = {
                    'team_kills': get_numbers(screenshot, bounding_box, X_BOUNDS_TEAM_KILLS, PIXEL_COLOR_TEXT_TEAM_KILLS),
                    'team_deaths': get_numbers(screenshot, bounding_box, X_BOUNDS_TEAM_DEATHS, PIXEL_COLOR_TEXT_TEAM_DEATHS),
                    'kills': get_numbers(screenshot, bounding_box, X_BOUNDS_KILLS, PIXEL_COLOR_TEXT),
                    'deaths': get_numbers(screenshot, bounding_box, X_BOUNDS_DEATHS, PIXEL_COLOR_TEXT),
                    'assists': get_numbers(screenshot, bounding_box, X_BOUNDS_ASSISTS, PIXEL_COLOR_TEXT),
                    'CS': get_numbers(screenshot, bounding_box, X_BOUNDS_CS, PIXEL_COLOR_TEXT),
                }
                print results

                if lastResults and results:
                    if results['CS'] > lastResults['CS']:
                        clip_sonic.play()

                    if results['kills'] > lastResults['kills']:
                        time_now = time()
                        time_since_last = time_now - kill_spree[0]

                        if time_since_last <= 10.5:
                            kill_spree = (time_now, kill_spree[1]+1)
                        else:
                            kill_spree = (time_now, 1)

                        kills = kill_spree[1]

                        clip_ohmygod.stop()
                        clip_mom_get_the_camera.stop()
                        clip_triple.stop()
                        clip_airporn.stop()
                        clip_airhorn.stop()

                        if kills >= 5:
                            clip_ohmygod.play()
                        elif kills >= 4:
                            clip_mom_get_the_camera.play()
                        elif kills >= 3:
                            clip_triple.play()
                        elif kills >= 2:
                            clip_airporn.play()
                        elif kills >= 1:
                            clip_airhorn.play()


                    elif results['team_kills'] > lastResults['team_kills']:
                        clip_wow.play()

                    if results['deaths'] > lastResults['deaths']:
                        clip_2sed.play()
                    elif results['team_deaths'] > lastResults['team_deaths']:
                        clip_fart.play()
                    # sleep(clip.seconds())
                    # clip.stop()

                lastResults = results
            except Exception as e:
                print "FAILUUUU {}".format(e)
        else:
            print "No window found"

main()