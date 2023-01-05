#!/usr/bin/python
# progressbar.py
# TODO :
#       add colors
#       improve layout

import math

class ParseException(Warning):
    """ a warning when you fail to parse text """

class ProgressBar:
    """A simple progress bar drawn to console class"""

   # bar length
   _barlgth = 20

   # character use for segments
   _segchar = '#'

   # character use for empty segments
   _empchar = '-'

   # character used on borders
   _brdchar = '|'

   # ffmpeg regex   
   _framex =  r".*frame=\s*(\d{1,}).*"

    # frame count
    _tfc = 0

   # parse for percent in std output
   #     can return an empty string or the actual percent (optional like)
   def _percent(self, ffmpeg_output : str) :
      fr = re.search(self._framex, ffmpeg_output)
            if fr : 
               framecount = int(fr.group(1))
               percent = framecount / (self._tfc + 1)
               return percent
      raise ParseException()

   # draw bar
   def _bar(self, percent : float) :
      seg = math.round(percent *100)
      return "".join(
         [_brdchar]                                                                      +
         [_segchar for i in range(0,int(self._barlgth * percent))]                  + 
         [_empchar for i in range(int(self._barlgth * percent) + 1, self._barlgth)] +
         [_brdchar])
      
   # explicit init
   def init(self, total_frame_count : int) :
      self._tfc = total_frame_count
  
   # update progess display
   def update(self, ffmpeg_output : str) :
    try: 
      percent = self._percent(ffmpeg_output)
      print(f"{round(percent *100)}% {self._bar(percent)}", end='\r')
    except:
        pass

   # implicit init
   def __init__(self, total_frame_count:int) :
      self.init(total_frame_count)

   # default init
   def __init__(self) :
      pass