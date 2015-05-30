#!/usr/bin/python
# -*- coding: utf8 -*-

import mp3play
import time

clip = mp3play.load("sounds/sonic_ring.mp3")
clip.play()
time.sleep(clip.seconds())
clip.stop()

print "done"