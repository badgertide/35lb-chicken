import csv
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import utils as Utils

"""set the base template for each chunk of episodes
this can help save time if the theme song changes each season
or certain segments start/stop being utilized"""
TEMPLATE = [
    {
    "start": 0,
    "end": 14.973291666666666,
    "name": 'production'
    },
    {
    "start": 14.973291666666666,
    "end": 124.99987499999999,
    "name": 'themeopen'
    },
    {
    "start": 124.99987499999999,
    "end": 779.9875416666666,
    "name": 'segment'
    },
    {
    "start": 779.9875416666666,
    "end": 786.9945416666666,
    "name": 'eyecatcher'
    },
    {
    "start": 786.9945416666666,
    "end": 794.5020416666666,
    "name": 'eyecatcher'
    },
    {
    "start": 794.5020416666666,
    "end": 1390.0136249999998,
    "name": 'segment'
    },
    {
    "start": 1390.0136249999998,
    "end": 1460.0002083333331,
    "name": 'themeclose'
    },
    {
    "start": 1460.0002083333331,
    "end": 1489.9885,
    "name": 'teaser'
    },
    {
    "start": 1489.9885,
    "end": 1500.0302083333331,
    "name": 'signoff'
    }
]

def find_files_for_projgen(root: Path):
    """
    walks the target directory for pairs of matching video and LosslessCut project files.
    (0001.mkv, 0001-proj.llc) qualifies as a pair
    in order to generate a file, the walk must find
    a: an mkv file that meets naming scheme (TODO set a naming scheme)
    b: there is NOT already a LLC file for this file
    c: there is NOT already a rendered video in the same directory
    """
    pairs = []
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)
        for filename in filenames:
            # skip file if it is not an uncut mkv video
            if not filename.lower().endswith(".mkv") or filename.lower().endswith("-cut.mkv"):
                continue
            # get a list of files in the current dir to check against
            files_in_dir = os.listdir(dirpath)
            filename_base = filename[:-4]
            skip = False
            for f in files_in_dir:
                if f == f"{filename_base}-proj.llc" or f ==f"{filename_base}-cut.mkv":
                    skip = True
                    break
            if skip is False:
                pairs.append(dirpath / filename)
    return sorted(pairs)

def get_target_dir():
    """Setting the cwd. Can be set automatically or by the user."""
    target_dir = ""
    if len(sys.argv) == 1: #no args
        target_dir = os.getcwd()
    elif len(sys.argv) == 2: #one arg
        target_dir = os.path.abspath(sys.argv[1])
    else:
        print("Usage: py main.py [DIRECTORY]")
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory")
        sys.exit(1)
    else:
        return target_dir

def get_video_length(filename):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True)
    return float(result.stdout)

def generate_proj(filepath, vid_len):
    """generates a LosslessCut project file, scaling the template to
    fit the video. This does NOT create a perfect cut, it only places
    all segments in the correct order at an approximate size"""
    proj_json = {}
    proj_json["version"] = 2
    proj_json["mediaFileName"] = os.path.basename(filepath)
    cut_segments = []
    template_len = TEMPLATE[-1]["end"]
    scale = vid_len / template_len
    segments_total_len = 0.0

    for s in TEMPLATE:
        temp_start = s["start"]
        temp_end = s["end"]
        segment_len = temp_end - temp_start

        segment_scaled_len = segment_len * scale
        cut_segments.append({
            "start": segments_total_len,
            "end": segments_total_len + segment_scaled_len,
            "name": s["name"],
            "selected": True
        })
        print(f"{segments_total_len} + {segment_scaled_len} = {segments_total_len + segment_scaled_len}")
        segments_total_len += segment_scaled_len
    proj_json["cutSegments"] = cut_segments

    if not math.isclose(segments_total_len, vid_len):
        print(f"WARN: {os.path.basename(filepath)} does not scale properly ({segments_total_len} != {vid_len}).")
        print(f"{os.path.basename(filepath)} project not generated.")
        return
    
    file_dir = os.path.dirname(filepath)
    file_name = os.path.basename(os.path.splitext(filepath)[0])
    new_filename = f"{file_name}-PROJGEN.llc"
    with open(os.path.join(file_dir, new_filename), "w", encoding="utf-8") as proj:
        json.dump(proj_json, proj, ensure_ascii=False, indent=4)

def main():
    """main."""
    # check for dependencies
    has_ffprobe = Utils.check_dependency("ffprobe")
    if not has_ffprobe:
        sys.exit(1)

    target_dir = get_target_dir()

    print(f"Recursively searching: {target_dir}")
    noprojfiles = find_files_for_projgen(target_dir)
    if not noprojfiles:
        print("No file found for projgen.")
        return
    else:
        print(f"Found {len(noprojfiles)} files for projgen.")
    for f in noprojfiles:
        vid_len = get_video_length(f)
        generate_proj(f, vid_len)


    print("\nDone.")

if __name__ == "__main__":
    main()