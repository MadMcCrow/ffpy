# helper to run FFMPEG

#!/usr/bin/python
#
#   ffmpeg.py :
#       class to run ffmpeg
#

# imports
import subprocess as sbp
from shlex import split as sp
from os import path as pt

_ffmpeg_cmd = "ffmpeg -progress /dev/stdout -i {input} {options} {output}"

def _san_path(path) : 
    return f"\'{pt.abspath(path)}\'"

class run : 
    # store process for operation
    process = None

    # convert option dict to list for ffmpeg
    @classmethod
    def option2list(options : dict) :
        return [val for pair in options.items() for val in pair]

    # will run ffmpeg with otions
    def __init__(self, in_path, out_path, options) :
        cmd = _ffmpeg_cmd.format(input=_san_path(in_path), options = options, output=_san_path(out_path))
        self.process = sbp.Popen( sp(cmd), stdout = sbp.PIPE, stderr = sbp.PIPE )

    @property
    def isrunning(self) :
        return self.process.poll() != None

    @property
    def outputs(self) :
        try :
            return (self.process.stdout , self.process.stderr)
        except :
            return None, None

    def kill(self) :
        try :
            self.process.kill()
            stdout, stderr = self.process.communicate()
            print(stderr)
        except :
            pass

    def __del__(self) :
        try :
            self.kill()
        except: 
            pass