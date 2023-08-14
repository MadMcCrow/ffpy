#!/usr/bin/python
# A simple script to compress videos and gain space on your drives
# TODO :


# imports
import os
import sys
import time

import ffprogress
import ffmpeg

# settings
qv_start = 75 # (0-100)
qv_step = 2
compressionRatio = 0.75

# default options for ffmpeg
compress_options =  {
    "-preset" : "slow",
    "-c:v" : "hevc_videotoolbox",
    "-tag:v" : "hvc1",
    "-c:a" : "aac",
    "-b:a" : "128k",
}

def remove(path) :
    try : 
        os.remove(path)
    except :
        print(f"Could not remove {path}, path does not exists")
        pass

# List of video file extensions to check
video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm"]

def convert(input_path, output_path, qv) :
    # use/ update options
    # TODO : allow custom options
    options = compress_options
    options["-q:v"] = f"{qv}"
    
    # create progressbar :
    pbar = ffprogress.ProgressBar(40)
    # launch ffmpeg
    ff = ffmpeg.run(input_path, output_path, options)
    while ff.isrunning() :
        #print(ff.outputs[0].readline().decode('utf-8').strip())
        pbar.progress(*ff.outputs)
        time.sleep(0.1)
    pbar.end()
    ff.kill()
    print(f"\nConversion complete for {input_path}")
    try :
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        ratio = input_size / output_size
    except : 
        ratio = 1
    
    if ratio <= compressionRatio :
        remove(input_path)
        print(f"Deleted original {input_path} as converted video is smaller or equal")
    else :
        remove(output_path)
        print(f"Deleted converted {output_path} as converted video is bigger")
        # retry :
        if qv > qv_step :
            convert(input_path, output_path, qv - qv_step)


def main() :
    try :
        if len(sys.argv) != 3:
            print(f"Usage: python {__name__}.py input_folder output_folder")
            sys.exit(1)

        input_folder = sys.argv[1]
        output_folder = sys.argv[2]

        os.makedirs(output_folder, exist_ok=True)

        # get all videos in folder
        video_files = [x for x in os.listdir(input_folder) if any(x.endswith(ext) for ext in video_extensions)]

        # sort by size : starting with smaller ones 
        video_files.sort(key=lambda x: os.path.getsize(os.path.join(input_folder, x)))

        # Convert or copy each video in the input folder to x265 format
        for input_file in video_files :
            # make sure input and output paths are OK :
            output_filename =  f"{os.path.splitext(input_file)[0]}_x265.mp4"
            input_path  = os.path.abspath(os.path.join(input_folder, input_file))
            output_path = os.path.abspath(os.path.join(output_folder, output_filename))
            
            # remove if already present :
            remove(output_path)
            # if isH265(input_path) :           
            #     print(f"Copying {input_file} (already in x265 format)")
            #     shutil.copy(input_path, output_path)
            print ("converting ...")
            convert(input_path, output_path, qv_start)

    except KeyboardInterrupt : 
        print("Interrupted by user")
        sys.exit(1)
    except Exception as E :
        print(f"Unhandled Error : {E.__class__.__name__} {E}")
        raise
        sys.exit(1)

    else :
        print("All operations complete!")
        sys.exit(0)

# call main function
# Run script if called directly
if __name__ == "__main__":
    main()