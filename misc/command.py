#!/usr/bin/python
#  command.py
#  parses argv and tell what to do
#  TODO : maybe not do this here

from dataclasses import dataclass
from enum import Enum

# argument start and end
_ARGSRT = 1
_ARGEND = 5
_COMP_FACTOR = 0.8
_MAX_SIZE_HEIGHT = 1440
_FILE_TAG = ""
_EXTENSIONS = ["mp4", "mkv", "avi"]


# types of actions
class Goto(Enum):
    HELP     = 0
    COMPRESS = 1
    
# get the arguments for transcode
@dataclass
class CommandArgs:
    """ Arguments for compressing video """
    InputFolder  : str
    OutputFolder : str
    OutputTag    : str
    
    Extensions   : list = []


def ParseArgs() :
    args = sys.argv[_ARGSRT:_ARGEND]
    for arg in args :
        if "help" in arg :
            return Goto.HELP

    DataArgs(OutputFolder = args[1], )
      = args[0]
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