#!/usr/bin/python
# A simple script to compress videos and gain space on your drives
# TODO :
#       Add a way to set parameters
#       work with a Video-class to simplify parsing
#       work with a codec-class to simplify parameters

import os
import shlex
import datetime
import time
import sys
import math
import subprocess


class ffmpeg() :



    #
    # @func ffmpeg
    # perform the actual conversion
    #
    def run(self, in_file:str, out_file:str) :
        indata = ffprobe(in_file)
        height = int(min(indata['height'], MAX_SIZE_HEIGHT))
        width  = int(math.floor(indata['width'] * (height / indata['height'])))
        max_bitrate = indata['bitrate'] * 2 # give some breathing room
        bitrate     = math.floor( indata['bitrate'] * COMP_FACTOR)
        # "h264_vaapi (nv12) or hevc_vaapi (p010)
        cmd = "ffmpeg -progress /dev/stdout -hwaccel vaapi -hwaccel_output_format vaapi -y -threads {threads} -i {input_file} -vf 'hwupload,scale_vaapi=w={width}:h={height}:format=nv12' -c:v h264_vaapi -b:v {bitrate} -maxrate {max_bitrate} -c:a copy {output_file}"
        cmd = cmd.format(
                    input_file  = f"\"{in_file}\"",
                    output_file = f"\"{out_file}\"",
                    height = height,
                    width  = width, 
                    bitrate     = f"{bitrate}K",
                    max_bitrate = f"{max_bitrate}K",
                    threads = f"{getThreads()}")
        frame_count = int(indata["fps"] * indata["duration"].total_seconds())
        try:
            process = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE, stderr = subprocess.PIPE )
            while process.poll() is None:
                    line = ""
                    try :
                        line = process.stdout.readline().decode('utf-8')
                        progressBar(line, frame_count)
                    except KeyboardInterrupt :
                        process.kill()
                        stdout, stderr = process.communicate()
                        exit()
                    except:
                        break
                    time.sleep(0.01)
            process.kill()
            stdout, stderr = process.communicate()
            return str(stderr)
        except Exception as error:
            print(f"Error while converting : {error}")
            try:
                process.kill()
                process.communicate()
            except : 
                pass
            raise
