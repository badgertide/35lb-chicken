import sys
import json5 # use instead of 'json' because LosslessCut does not use standard JSON

import utils as Utils
import constants as c

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

# -----------------------------
# LLC/time-frame parsing
# -----------------------------
def load_segments_from_map(cut_filepath):
    """
    reads the -proj.llc file and extracts user-defined chunks
    TODO treat chunks differently by category
    """
    cuts = []
    with open(cut_filepath, newline="", encoding="utf-8") as f:
        data = json5.parse(f.read())[0]
        for i, row in enumerate(data["cutSegments"]):
            start = (row.get("start", None))
            end = (row.get("end", None))
            label = row.get("name", None)

            if None in [start, end, label]:
                Utils.print_to_log(f"[{cut_filepath.name}] Skipping segment {i+1}: missing Start/End/Name")
                continue

            duration = end - start
            if duration <= 0:
                error = f"[{cut_filepath.name}] Segment {i} has non-positive duration: {start} -> {end}"
                Utils.print_to_log(error)
                raise ValueError(error)

            out_name = f"segment_{i:02d}"
            cuts.append({
                "start": start,
                "end": end,
                "duration": duration,
                "filename": out_name,
                "label": label,
            })
    if not cuts:
        error = f"No valid cuts found in project: {cut_filepath}"
        Utils.print_to_log(error)
        raise RuntimeError(error)
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
    data = json5.parse(data)[0]
    return data.get("streams", [])

def build_ffmpeg_streammaps(streams):
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

# -----------------------------
# Segment cutting
# -----------------------------
def make_reencode_segment(input_file, output_file, start, end, maps):
    """runs a segment of the file through ffmpeg, re-encoding the chunk."""
    args = ["ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
    "-i", input_file, "-ss", start, "-to", end,
    *maps, *VIDEO_ENCODE_ARGS, *AUDIO_ENCODE_ARGS, *SUBTITLE_ARGS,
    str(output_file)]
    Utils.print_to_log(f"Running FFMPEG command '{" ".join(args)}'")
    Utils.run(args)
    print("Done.")

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
# Main per-file processing
# -----------------------------

# TODO clean up other functionality
def process_file(video_file, proj_file, options, temp_dir):
    """handles the processing of one file from beginning to end."""
    output_filename = video_file.with_stem(f"{c.CUT_FILE_PREFIX}{video_file.stem}")

    print(f"\n=== Processing: {video_file.name} ===")
    proj_cuts = load_segments_from_map(proj_file)
    user_cuts = parse_base_segments(proj_cuts, options)
    return

    streams = ffprobe_streams(video_file)
    stream_maps = build_ffmpeg_streammaps(streams)
    segment_files = []

    for i, cut in enumerate(user_cuts):
        start = cut['start']
        end = cut['end']
        duration = cut['duration']
        filename = cut['filename']
        label = cut['label']

        # TEMPORARY - in the future, intelligently select which video get skipped
        if not label == "generic":
            continue

        seg_file = temp_dir / f"ep{video_file.stem}_seg_{i:03d}_chunk.mkv"
        print(f"\n=== Encoding segment: '{temp_dir}/ep{video_file.stem}_seg_{i:03d}_chunk.mkv' ===")
        make_reencode_segment(str(video_file), seg_file, str(start), str(end), stream_maps)
        segment_files.append(seg_file)

    concat_file = temp_dir / f"ep{video_file.stem}_concat.txt"
    concat_segments(concat_file, segment_files, output_filename)

    print("Deleting temp segment files...")
    for seg_file in segment_files:
        if seg_file.exists():
            seg_file.unlink()
    if concat_file.exists():
        concat_file.unlink()

    print(f"Done: {output_filename}")