#!/usr/bin/env python3

import argparse
import os
import sys
import multiprocessing
import itertools
import logging
import json

def __run_multi_line_cmd(cmd):
    """
    run a command that consists of several lines that are combined again
    Parameters
    ----------
    cmd : str
        command to run, e.g. cmd="ls \n -la" will run "ls -la"
    TODO: move to utils/system?
    Returns
    -------
    in case of error an error is thrown
    Notes
    -----
    TODO: will be in future version not included in cencro
    """
    # remove multiple spaces in cmd
    cmd = " ".join(cmd.split())
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(f"error in running command {cmd}")


def convert_and_cc(video, result_folder, center_crop=540):
    width = 3840
    height = 2160
    framerate = 60
    pixel_format = "yuv420p"  # we should not go beyond
    center_crop_width = 2 * (int(center_crop * width / height) // 2)
    result_video = os.path.join(
        result_folder,
        os.path.splitext(os.path.basename(video))[0] + f"_cc_{center_crop}p.mp4"
    )
    logging.info(f"{video} convert to {result_video}")
    cmd = f"""
    ffmpeg -nostdin -loglevel quiet -threads 4
    -y
    -i {video}
    -filter:v scale={width}:{height},fps={framerate}
    -an
    -pix_fmt {pixel_format} -strict -1
    -f yuv4mpegpipe pipe:
    |
    ffmpeg -nostdin -loglevel quiet -threads 4
    -y -f yuv4mpegpipe
    -i pipe:
    -filter:v crop={center_crop_width}:{center_crop}
    -pix_fmt {pixel_format}
    -framerate {framerate}
    -c:v libx264
    -crf 22
    -an
    {result_video} 2>/dev/null"""

    __run_multi_line_cmd(cmd)


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='convert video to center cropped crf 22 h.264 version',
                                     epilog="stg7 2020",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", type=str, nargs="+", help="video to convert")
    parser.add_argument("--result_folder", type=str, default="videos", help="folder for storing the generated videos")
    parser.add_argument('--cpu_count', type=int, default=multiprocessing.cpu_count() // 2, help='thread/cpu count')
    parser.add_argument('--cc', type=int, default=540, help='used center crop')

    a = vars(parser.parse_args())

    logging.basicConfig(level=logging.DEBUG)
    logging.info("convert videos")
    logging.info(f"params: {json.dumps(a, indent=4)}")
    os.makedirs(a["result_folder"], exist_ok=True)

    params = [(video, a["result_folder"], a["cc"]) for video in a["video"]]
    if a["cpu_count"] > 1:
        pool = multiprocessing.Pool(a["cpu_count"])
        res = pool.starmap(convert_and_cc, params)
    else:
        res = list(itertools.starmap(convert_and_cc, params))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
