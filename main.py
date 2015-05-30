#!/usr/bin/python
# -*- coding: <encoding name> -*-

from gevent import monkey; monkey.patch_all()

from time import sleep, time

from capture import screenshot_image, get_windows_bytitle, Screenshot
from ocr import get_stats
from server import Server
from window import Gui
from threading import Thread, Event


def main():
    kill_event = Event()

    socket_server = Server()
    socket_server.start()
    gui = Gui(kill_event)
    gui.start()
    gui.set_status_server(True)


    # =========================================
    #  Main Loop
    # =========================================

    last_results = None
    kill_spree = (0,0)
    while not kill_event.is_set():
        windows = get_windows_bytitle('League of Legends')

        # =========================================
        #  Found Window
        # =========================================

        if windows:
            gui.set_status_game(True)

            window = windows[0]

            # =========================================
            #  Screenshot
            # =========================================

            screenshot = Screenshot(screenshot_image(window))

            # =========================================
            #  Stats
            # =========================================

            try:
                results = get_stats(screenshot)
            except:
                #TODO: save screenshot
                gui.set_status_stats(False)
                continue

            gui.set_status_stats(True)
            gui.set_stats(results)

            # =========================================
            #  Events
            # =========================================

            if last_results and results:

                diff_cs = results['CS'] - last_results['CS']
                diff_kills = results['kills'] - last_results['kills']
                diff_deaths = results['deaths'] - last_results['deaths']
                diff_team_kills = results['team_kills'] - last_results['team_kills']
                diff_team_deaths = results['team_deaths'] - last_results['team_deaths']

                gui.set_cs(results['CS'])

                if diff_cs > 0:
                    socket_server.send({ 'event': 'cs', 'amount': diff_cs, 'total': results['CS'] })

                if diff_kills:
                    time_now = time()
                    time_since_last = time_now - kill_spree[0]

                    if time_since_last <= 10.5:
                        kill_spree = (time_now, kill_spree[1]+diff_kills)
                    else:
                        kill_spree = (time_now, 1)

                    kills = kill_spree[1]

                    socket_server.send({ 'event': 'kill', 'total': results['kills'], 'streak': kills })

                elif diff_team_kills:
                    socket_server.send({ 'event': 'team_kill', 'amount': diff_team_kills, 'total': results['team_kills'] })

                if diff_deaths:
                    socket_server.send({ 'event': 'death', 'total': results['deaths'] })
                elif diff_team_deaths:
                    socket_server.send({ 'event': 'team_death', 'amount': diff_team_deaths, 'total': results['team_deaths'] })

            last_results = results

        # =========================================
        #  Missing Window
        # =========================================

        else:
            gui.set_status_game(False)

        gui.set_status_clients(len(socket_server.clients()))
        sleep(0.1)

    socket_server.stop()

if __name__ == '__main__':
    main()