#!/usr/bin/python
# A simple script to compress videos and gain space on your drives
# TODO :
#       Add a way to set parameters
#       work with a Video-class to simplify parsing
#       work with a codec-class to simplify parameters

import misc.help 
import ffmpeg.ffprobe as ffprobe
import ffmpeg.ffmpeg  as ffmpeg
import misc.os

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
    except Exception as error:
        help()
        print(f"error {error}")
        raise error
    else :
        "that's all folks !"