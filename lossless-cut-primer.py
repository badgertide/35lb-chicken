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
        print(vid_len)


    print("\nDone.")

if __name__ == "__main__":
    main()