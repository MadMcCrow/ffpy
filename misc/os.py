#!/usr/bin/python
# os.py
#  Collection of helpful functions

# avoid killing cpu usage :
_CPU_USAGE   = 0.95

#
# @func getThreads
# get a reasonable amount of CPU power
#
def getThreads() -> int:
    return math.floor(os.cpu_count() * _CPU_USAGE)

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