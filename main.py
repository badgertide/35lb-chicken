import sys
import os
from pathlib import Path
import tempfile
import json5 # use instead of 'json' because LosslessCut does not use standard JSON

import utils as Utils
import cli as CLI
import constants as c
import video

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

# -----------------------------
# File discovery
# -----------------------------
def get_projects_for_cutting(root: Path):
    """
    walks the target directory for pairs of matching video and losslesscut files.
    (0001.mkv, 0001-proj.llc) qualifies as a pair
    TODO handle this more dynamically in the future, allow for remote projects
    """
    pairs = []
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)
        projs = []
        for f in filenames:
            if not f.endswith(c.LOSSLESSCUT_SUFFIX):
                continue
            projs.append(f)

        for p in projs:
            with open(dirpath / p, newline="", encoding="utf-8") as f:
                fdata = json5.parse(f.read())[0]
                if fdata["version"] != 2:
                    Utils.print_to_log(f"Skipping project file '{p}', version={fdata["version"]}, but only version 2 is supported")
                    continue
                target_mediafile = os.path.join(dirpath, fdata["mediaFileName"])
                if not os.path.isfile(target_mediafile):
                    Utils.print_to_log(f"WARN: Project file '{p}' claims file {fdata["mediaFileName"]}, which was not found")
                    continue
                target_mediafile_rendered = os.path.join(dirpath, c.CUT_FILE_PREFIX + fdata["mediaFileName"])
                if os.path.isfile(target_mediafile_rendered):
                    Utils.print_to_log(f"Rendered video '{c.CUT_FILE_PREFIX + fdata["mediaFileName"]}' already exists. Skipping")
                    continue
                pairs.append((Path(target_mediafile), Path(dirpath / p)))
    return pairs

#################################

def main():
    """main."""
    # check for dependencies
    has_ffmpeg = Utils.check_dependency("ffmpeg")
    has_ffprobe = Utils.check_dependency("ffprobe")
    if not (has_ffmpeg and has_ffprobe):
        sys.exit(1)

    target_dir = get_target_dir()

    print(f"Recursively searching: {target_dir}")
    pairs = get_projects_for_cutting(target_dir)
    if not pairs:
        print("No matching video/project pairs found.")
        return
    else:
        print(f"Found {len(pairs)} pairs.")

    options = CLI.get_cutmap_options()
    if not options:
        return

    with tempfile.TemporaryDirectory(prefix="35pcut_") as temp_dir:
        temp_dir = Path(temp_dir)
        for i, (video_file, proj_file) in enumerate(pairs):
            try:
                video.process_file(i+1, video_file, proj_file, temp_dir)
            except Exception as e:
                print(f"ERROR processing {video_file.name}: {e}")

    print("\nDone. Happy viewing!")

if __name__ == "__main__":
    main()