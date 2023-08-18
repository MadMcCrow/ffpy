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

_ffmpeg_cmd = "ffmpeg {prefix} -i {input} {options} {output}"

def _san_path(path) : 
    return f"\'{pt.abspath(path)}\'"

class run : 
    # store process for operation
    process = None

    # convert option dict to list for ffmpeg
    @staticmethod
    def options2list(options : dict) :
        return [val for pair in options.items() for val in pair]

    @staticmethod
    def options2str(options : dict) :
        return ' '.join(run.options2list(options))

    # will run ffmpeg with otions
    def __init__(self, in_path, out_path, options, subprocess=True) :
        # ffmpeg command line 
        cmd = _ffmpeg_cmd.format( 
            prefix = "-progress /dev/stdout" if subprocess else "",
            input=_san_path(in_path),
            options = run.options2str(options),
            output=_san_path(out_path))
        # echo
        print (f"running ffmpeg with :{cmd}\n")
        # run
        if subprocess :
            self.process = sbp.Popen( sp(cmd), stdout = sbp.PIPE, stderr = sbp.PIPE )
        else :
            sbp.run( sp(cmd))

    def isrunning(self) :
        try :
            return self.process.poll() == None
        except :
            return True



    @property
    def outputs(self) :
        try :
            return self.process.stdout , self.process.stderr
        except :
            return None, None

    def kill(self) :
        try :
            if self.isrunning() :
                print ("process killed")
                self.process.kill()
        except AttributeError :
            pass

    def __del__(self) :
        self.kill()