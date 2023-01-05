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
import re

# this script constant parameters:
# @note : these could be cli parameters
CPU_USAGE   = 0.95
COMP_FACTOR = 0.8
MAX_SIZE_HEIGHT = 1440
FILE_TAG = ""
EXTENSIONS = ["mp4", "mkv", "avi"]
BAR_LENGTH = 20

# various ffmpeg regex
_durex  =  r".*Duration: (\d{2}):(\d{2}):(\d{2}).(\d{2}).*bitrate: (\d*) kb/s"
_framex =  r".*frame=\s*(\d{1,}).*"
_forex  =  r".*Stream.*Video: (\S+) .*, (\d{3,})x(\d{3,}).*, (\d*) kb/s, (\d+\.?\d*) fps"


# @func help
# explains how to use
#
def help() :
   print('''
   this script compresses all your videos.
   it can take two inputs : 
    - first the path of the folder containing all your videos
    - second the path of the folder you want to output to
   example :
   python3 ./convert.py ./inputs ./outputs
   '''
   )

#
# @func getThreads
# get a reasonable amount of CPU power
#
def getThreads() -> int:
    return math.floor(os.cpu_count() * CPU_USAGE)

#
# @func getSize
# get the size of a file
#
def getSize(file_path :str) -> int:
    try :
      return int(os.path.getsize(file_path))
    except:
        return 0

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
# @func findFiles
# get all the video files in a path
# @param filepath     the path you want files from
# @param ext          the extension of files
#
def findFiles(filepath : str, ext :str)  -> list:
    glob = []
    for cur, _dirs, files in os.walk(filepath):
        glob = glob + ['/'.join([cur,itr]) for itr in files if str(itr).endswith(ext)]
    return glob

#
# Displays a nice progressbar for    
#
def progressBar(ffmpeg_output, total_frame_count) :
    try:
        fr = re.search(_framex, ffmpeg_output)
        if fr : 
            framecount = int(fr.group(1))
            percent = framecount / (total_frame_count + 1)
            bar = "".join(["#" for i in range(0,int(BAR_LENGTH * percent))] + ["-" for i in range(int(BAR_LENGTH * percent) + 1, BAR_LENGTH)])
            print(f"{round(percent *100)}% |{bar}|", end='\r')
    except:
        pass

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

#
# @func ffmpeg
# perform the actual conversion
#
def ffmpeg(in_file:str, out_file:str) :
    indata = ffprobe(in_file)
    height = int(min(indata['height'], MAX_SIZE_HEIGHT))
    width  = int(math.floor(indata['width'] * (height / indata['height'])))
    max_bitrate = indata['bitrate']
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

#
# @func transcode
# will convert and check if successfully reduced size
#
def compress(video_file : str, output_folder : str) -> bool :
    base_name, extension = os.path.splitext(os.path.basename(video_file))
    new_file_name = "".join([base_name,FILE_TAG, extension]);
    new_file      = os.path.join(output_folder, new_file_name)
    try :
      ffmpeg(video_file, new_file)
      old_size = getSize(video_file)
      new_size = getSize(new_file)
      if new_size in range( int( old_size * COMP_FACTOR * 0.99), int( old_size)) : 
        print(f"success : {video_file} was compressed to {new_file} !")
        os.remove(video_file)
      else:
        print(f"failed : {new_file} is  bigger than {video_file} !")
        try :
            os.remove(new_file)
        except :           
            pass
        print(f"keeping {video_file} !")
        os.rename(video_file,new_file)
    except Exception as error:
        print(f"Error : {video_file} {error}!")
        raise

# Run script if called directly
if __name__ == "__main__":
    args = sys.argv[1:5]
    try :
        if "help" in args[0] : 
            help()
            exit()
        else :
            video_folder  = args[0]
            output_folder = args[1]
        all_vids = []
        for ext in EXTENSIONS : 
            all_vids.extend(findFiles(video_folder, ext))
        all_vids.sort(key = getSize) # sorts vids by size to always start with the easy ones
        # compress all files
        os.makedirs(output_folder, exist_ok=True)
        for vid in all_vids :
            if not FILE_TAG in vid or FILE_TAG == "" :
                print(f"Compressing {vid}")
                compress(vid, output_folder)
            else :
                print(f"{vid} already optimised")
    except Exception as error:
        help()
        print(f"error {error}")
        raise error
    else :
        "that's all folks !"