#!/usr/bin/python
# ffprobe.py
#               Script to handle ffprobing files

import shlex
import datetime
import time
import sys
import math
import subprocess
import re

# various ffmpeg regex
_durex  =  r".*Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2}).*bitrate: (\d*) kb/s"
_forex  =  r".*Stream.*Video: (\S+) .*, (\d{3,})x(\d{3,}).*, (\d*) kb/s, (\d+\.?\d*) fps"

#
# @func parseDuration
#  Convert the 4 values given by ffmpeg to a timedelta
#
def parseDuration(hr, mn, sc, ct) :
    return  datetime.timedelta(
    microseconds = int(ct) * 10000,
    seconds = int(sc),
    minutes = int(mn),
    hours = int(hr))
    print(cmd)

#
# @func ffprobe
# give you key information about your videos
#
def ffprobe(file) :
    # the regexes:
    # retval
    data = {}
    #cmd
    lines = str(subprocess.run(shlex.split("ffprobe {}".format('"{}"'.format(file))), stdout = subprocess.PIPE, stderr = subprocess.STDOUT).stdout)
    # parse
    dr = re.search(_durex, lines)
    fr = re.search(_forex, lines)
    data['bitrate'] = int(dr.group(5))  if dr else 0
    data['duration'] = parseDuration(dr.group(1), dr.group(2), dr.group(3), dr.group(4)) if dr else datetime.timedelta()
    data['codec']  = fr.group(1)        if fr else "h264"
    data['width']  = int(fr.group(2))   if fr else 0
    data['height'] = int(fr.group(3))   if fr else 0
    data['vbr']    = int(fr.group(4))   if fr else 0
    data['fps']    = float(fr.group(5)) if fr else 0
    return data