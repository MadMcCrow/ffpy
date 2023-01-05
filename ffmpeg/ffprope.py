#!/usr/bin/python
# ffprobe.py
#   Script to handle ffprobing files
#   TODO :
#       command class
#       audio infos

from dataclasses import dataclass
import shlex
from datetime import timedelta as Time
import subprocess
import re


class FFprobeException(Error):
    """ Error raised when failed to get a FFProbe output """
    def __init__(self, *args):
        super().__init__(args)
    def __str__(self):
        return f'Failed to get a result from ffprobe'

@dataclass
class Format:
    """Video Format, ie. size on screen """
    
    # width
    x : int
    #height
    y : int

@dataclass
class Video:
    """Class for storing all ffprobe results for a video"""

    # video duration
    duration : Time
    # video bitrate
    bitrate : int
    # codec used
    codec : str
    # dimensions idurationn pixel
    scale : Format
    # vbr : variable bitrate, if found
    vbr : int
    # fps : frame per seconds
    fps : float

#
# @func parseDuration
#  Convert the 4 values given by ffmpeg to a timedelta
#
def _parseDuration(hr, mn, sc, ct) ->Time :
    return  Time(
    microseconds = int(ct) * 10000,
    seconds = int(sc),
    minutes = int(mn),
    hours = int(hr))


#
# @func duration_bitrate
#  parse the duration line for duration and bitrate 
#
def _duration_bitrate(lines) :
    _regex  =  r".*Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2}).*bitrate: (\d*) kb/s"
    db = re.search(_regex, lines)
    if db :
        return parseDuration(db.group(1), db.group(2), db.group(3), db.group(4)), int(db.group(5))
    else  :
        return Time(), 0

#
# @func _video
#  parse the video lines for infos 
#
def _video(lines) :
    _regex  =  r".*Stream.*Video: (\S+) .*, (\d{3,})x(\d{3,}).*, (\d*) kb/s, (\d+\.?\d*) fps"
    fr = re.search(_regex, lines)
    codec = fr.group(1)         if fr else "h264"
    width = int(fr.group(2))    if fr else 0
    height = int(fr.group(3))   if fr else 0
    vbr    = int(fr.group(4))   if fr else 0
    fps    = float(fr.group(5)) if fr else 0
    return codec, width, height, vbr, fps

#
# @func ffprobe
# give you key information about your videos
#
def ffprobe(file : str) -> Video :
    try :
        lines = str(subprocess.run(shlex.split("ffprobe {}".format('"{}"'.format(file))), stdout = subprocess.PIPE, stderr = subprocess.STDOUT).stdout)
        db = _duration_bitrate(lines)
        vd = _video(lines)
        data  = Video(
            duration = db[0]
            bitrate  = db[1]
            codec    = vd[0]
            scale    = Format(x = vd[1], y = vd[2])
            vbr      = vd[3]
            fps      = vd[4])
        return data
    except : 
        raise FFprobeException()