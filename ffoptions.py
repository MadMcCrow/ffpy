#!/usr/bin/python
#
#   ffoptions.py :
#       module containing functions and variable to set options for output
#

def scale_vaapi(width, height) :
    ''' scale output, vaapi only '''
    return  {
        "-vf" : f"'hwupload,scale_vaapi=w={width}:h={height}:format=nv12'",
        "-c:v" : "h264_vaapi",
    }

def bitrate_limit(bitrate, maxrate) :
    ''' limit bitrate of output '''
    return {
        "-b:v" : f"{bitrate}",
        "-maxrate" : f"{max_bitrate}",
    }

# MAC OS best option
hevc_videotoolbox =  {
    "-preset" : "slow",
    "-c:v" : "hevc_videotoolbox",
    "-tag:v" : "hvc1",
    "-q:v" : "70",
    "-c:a" : "aac",
    "-b:a" : "128k",
}

# AMD / Intel card Linux best option
hevc_linux_vaapi = {
    "-hwaccel" : "vaapi",
    "-hwaccel_output_format" : "vaapi",
    "-c:v" : "h264_vaapi",
    "-c:a" : "copy",
}