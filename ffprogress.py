#!/usr/bin/python
#
#   ffprogress.py :
#       module to display a progressbar
#

import re
import datetime
import math 

# static constants
_dur_re = re.compile(r".*Duration:\W*(\d+):(\d+):(\d+)\.(\d+),.*")
_fra_re = r".*frame=\W*(\d+)"
_tim_re = r".*time=\W*(\d+):(\d+):(\d+)\.(\d+)"

## durations are just time deltas 
class FFMPEGDuration (datetime.timedelta) :
    
    # timestamp is a tuple of hours, minutes, sec, centi
    def __init__(self, timestamp) :
        h,m,s,c = timestamp
        map (lambda x : int(x), hmsc)
        u = c * 1000
        d = int(math.floor(h/24))
        __init__(self, d, m, s, u )

    def __div__() :
        return self.total_seconds() / other.total_seconds()


## parse ffmpeg output
class FFMPEGOutput :

    frame = None
    timecode = None
    duration = None
    clear_new_frame = False

    def __init__(self, clear_new_frame = False) :
        self.clear_new_frame = clear_new_frame
    
    def parse(self, stderr, stdout):
        lines =  map(lambda x : x.readline().decode('utf-8').strip(), [stdout, stderr])
        for line in lines :
            try:
                d = FFMPEGDuration(_dur_re.findall(line)[0])
            except :
                d = None
                pass
            try : 
                t = FFMPEGDuration(_tim_re.findall(line)[0])
            except :
                t = None
                pass
            try :
               f = FFMPEGDuration(_fra_re.findall(line)[0])
            except :
                f = None
                pass
        self.duration = d if d != None  else self.duration
        self.timecode = t if t != None  else self.timecode
        self.frame    = f if f != None  else self.frame
    
    @property
    def progress(self) : 
        try : 
            return timecode / duration
        except: 
            return 0 


# a progressbar that display conversion progress
class ProgressBar :
    def __init__(self, bar_length, output : FFMPEGOutput = None) :
        self.bar_length = bar_length
        self.output = output if output != None else FFMPEGOutput()

    def progress(self, stdout, stderr) :
        output.parse(stdout, stderr)
        try : 
            percent = min(1.0, max(0.0, output.progress))
            bar = '#' * int(percent * bar_length) +  '-' * int((1 - percent) * bar_length)
            print(f"\rprogress = {round(percent * 100, 2)}% [{bar}] (frame={frame})", end="")
        except Exception as E :
            print(f"error : {E.__class__.__name__} , {E}")
            pass

    def __del__(self):
        print("\n")
