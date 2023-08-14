#!/usr/bin/python
#
#   ffprobe.py :
#       class to run ffprobe and read it's info
# 
#   TODO : implement getting all relevant data !
#

# default options for ffprobe
ffprobeOptions = {
    "-v" : "error",
    "-select_streams" : "v:0",
    "-show_entries" : "stream=codec_name",
    "-of" : "default=noprint_wrappers=1:nokey=1",
}

def isH265(input_file) :
    return False
    try :
        codec = subprocess.check_output(["ffprobe", *optionToList(ffprobeOptions), input_file], universal_newlines=True).strip()
        return any ( codec == x for x in ["hevc", "vp9", "x265", "h265"])
    except :
        return False