import csv
import json
import os
from pathlib import Path
import sys
import tempfile

import utils as Utils

# -----------------------------
# Settings & Dependencies
# -----------------------------

# NVENC quality/speed tradeoff
# Good options: p4, p5, p6, p7 (higher = slower/better)
NVENC_PRESET = "p5"
VIDEO_ENCODE_ARGS = [
    "-c:v", "h264_nvenc", "-preset", NVENC_PRESET,
    "-pix_fmt", "yuv420p", "-movflags", "+faststart"
]
AUDIO_ENCODE_ARGS = ["-c:a", "aac", "-b:a", "192k"]
SUBTITLE_ARGS = ["-c:s", "copy"]

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
def find_matching_pairs(root: Path):
    """
    walks the target directory for pairs of matching video and cut files.
    (0001.mkv, 0001-cut.mkv) qualifies as a pair
    TODO handle this more dynamically in the future
    """
    pairs = []
    for dirpath, _, filenames in os.walk(root):
        dirpath = Path(dirpath)
        filenames_set = set(filenames)
        for filename in filenames:
            if not filename.lower().endswith(".mkv"):
                continue
            if filename.lower().endswith("-cut.mkv"):
                continue
            csv_name = filename + ".csv"
            if csv_name in filenames_set:
                pairs.append((dirpath / filename, dirpath / csv_name))
    return sorted(pairs)

# -----------------------------
# CSV parsing
# -----------------------------
def load_segments(csv_file):
    """
    reads the -cut.csv file and extracts user-defined chunks
    TODO treat chunks differently by category
    """
    cuts = []
    with open(csv_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            start = (row.get("Start") or "").strip()
            end = (row.get("End") or "").strip()
            label = row.get("Name", "").strip()
            #TODO do this better
            if not start or not end or not label:
                print(f"Skipping row {i} in {csv_file.name}: missing Start/End/Name")
                continue

            start_s = Utils.time_to_seconds(start)
            end_s = Utils.time_to_seconds(end)
            duration = end_s - start_s
            if duration <= 0:
                raise ValueError(f"Segment {i} has non-positive duration: {start} -> {end}")

            out_name = f"segment_{i:02d}"

            cuts.append({
                "start": start,
                "end": end,
                "start_s": start_s,
                "end_s": end_s,
                "duration": duration,
                "filename": out_name,
                "label": label,
            })
    if not cuts:
        raise RuntimeError(f"No valid cuts found in CSV: {csv_file}")
    return cuts

# -----------------------------
# FFprobe helpers
# -----------------------------
def ffprobe_streams(input_file):
    """read streams from a video."""
    data = Utils.run_capture([
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_streams", str(input_file)
    ])
    return json.loads(data)["streams"]

def build_maps(streams):
    """select which streams to keep. TODO Make this more configurable"""
    maps = []
    for i, s in enumerate(streams):
        codec_type = s.get("codec_type")
        lang = s.get("tags", {}).get("language", "").lower()
        keep = False
        if codec_type == "video":
            keep = True
        elif codec_type == "audio" and lang in ["eng","jap"]:
            keep = True
        elif codec_type == "subtitle" and lang == "eng":
            keep = True
        if keep:
            maps.extend(["-map", f"0:{i}"])
    if not maps:
        raise RuntimeError("No matching streams found")
    return maps

def concat_segments(concat_file, segment_files, final_output):
    """stitch encoded videos into one."""

    with open(concat_file, "w", encoding="utf-8") as f:
        for seg_file in segment_files:
            # ffmpeg concat demuxer wants forward slashes or escaped paths
            safe_path = seg_file.name.replace("'", r"'\''")
            f.write(f"file '{safe_path}'\n")

    Utils.run([
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", str(final_output)
    ])

# -----------------------------
# Segment cutting
# -----------------------------
def make_reencode_segment(input_file, output_file, start, end, maps):
    """runs a segment of the file through ffmpeg, re-encoding the chunk."""
    Utils.run([
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
        "-i", str(input_file), "-ss", start, "-to", end,
        *maps, *VIDEO_ENCODE_ARGS, *AUDIO_ENCODE_ARGS, *SUBTITLE_ARGS,
        str(output_file)
    ])
    print("Done.")

# -----------------------------
# Main per-file processing
# -----------------------------
def process_file(index, input_file, csv_file, temp_dir):
    """handles the processing of one file from beginning to end."""
    output_file = input_file.with_name(f"{input_file.stem}-cut{input_file.suffix}")
    if output_file.exists():
        print(f"=== Skipping (already exists): {output_file} ===")
        return

    print(f"\n=== Processing: {input_file.name} ===")
    cuts = load_segments(csv_file)
    streams = ffprobe_streams(input_file)
    maps = build_maps(streams)
    segment_files = []

    for i, cut in enumerate(cuts):
        start = cut['start']
        end = cut['end']
        start_s = cut['start_s']
        end_s = cut['end_s']
        duration = cut['duration']
        filename = cut['filename']
        label = cut['label']

        if end_s <= start_s:
            continue

        seg_file = temp_dir / f"ep{index}_seg_{i:03d}_chunk.mkv"
        print(f"\n=== Encoding segment: '{temp_dir}/ep{index}_seg_{i:03d}_chunk.mkv' ===")
        make_reencode_segment(input_file, seg_file, start, end, maps)
        segment_files.append(seg_file)

    concat_file = os.path.join(temp_dir, f"ep{index}_concat.txt")
    concat_segments(concat_file, segment_files, output_file)

    print("Deleting temp segment files...")
    for seg_file in segment_files:
        if seg_file.exists():
            seg_file.unlink()
    if concat_file.exists():
        concat_file.unlink()

    print(f"Done: {output_file}")

def main():
    """main."""
    # check for dependencies
    has_ffmpeg = Utils.check_dependency("ffmpeg")
    has_ffprobe = Utils.check_dependency("ffprobe")
    if not (has_ffmpeg and has_ffprobe):
        sys.exit(1)

    target_dir = get_target_dir()

    print(f"Recursively searching: {target_dir}")
    pairs = find_matching_pairs(target_dir)
    if not pairs:
        print("No matching .mkv + .csv pairs found.")
        return
    else:
        print(f"Found {len(pairs)} pairs.")

    with tempfile.TemporaryDirectory(prefix="35pcat_") as temp_dir:
        temp_dir = Path(temp_dir)
        for i, (input_file, csv_file) in enumerate(pairs):
            try:
                process_file(i+1, input_file, csv_file, temp_dir)
            except Exception as e:
                print(f"ERROR processing {input_file.name}: {e}")

    print("\nDone. Happy viewing!")

if __name__ == "__main__":
    main()