import sys
import json5 # use instead of 'json' for LosslessCut's nonstandard .llc files

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

def parse_segment_cuts(base_segments, options):
    """To cut out segments from the video, first sort every segment by its start time.
    Then check every `generic` for an overlapping `filler` and cut along those lines"""
    # Sort by start time. If any segments start at the same time, make sure the generic is first
    # "label != generic" treats "generic" as 0, everything else as 1
    base_segments = sorted(base_segments, key=lambda d:(d["start"], d["label"]!="generic"))
    parsed_segments = []
    for i, s in enumerate(base_segments):
        if not s["label"] in ["generic"] + c.FILLER_TYPES:
            # TODO we should check for overlaps that will break things
            # honestly that should be checked by now
            parsed_segments.append(s)
            continue # only generics have filler unless I can think of a reason otherwise
        # check each generic against each subsequent segment. Proceed if it is a filler AND it is contained by the generic
        generic = s
        fillers = []
        for s2 in base_segments[i+1:]:
            if not s2["label"] in c.FILLER_TYPES:
                continue
            if s2["start"] >= generic["end"]:
                # if this segment starts after the target ends, we're done
                break
            #if s2["start"] >= generic["start"] and s2["end"] <= generic["end"]: # I don't think this is needed
            fillers.append(s2)
        # BUG 'generic' can be filler. Investigate this
        parsed_segments += slice_generic_by_fillers(generic, fillers)
    for i, j in enumerate(parsed_segments):
        # TODO Finish this
        print(f"segment {i:<3}: {round(j["start"], 2)} -> {round(j["end"], 2)}")
    return parsed_segments

def slice_generic_by_fillers(generic, fillers):
    """generic i = [ [ a ]  [   b   ]   [c]     ]
    - is 'i' free of overlaps? No, split by first overlap
    - now we have [i1], i2 = [  [   b   ]   [c]     ]
    - is i1 free of overlap? Yes, Add it to the list
    - is i2 free of overlap? No, split by first overlap
    - now we have [i3], i4 = [   [c]     ]
    - is i3 free of overlap? Yes, Add it to the list
    - is i4 free of overlap? No, split by first overlap
    - now we have [i5 ], [  i6 ]
    - is i5 free of overlap? Yes, Add it to the list
    - is i6 free of overlap? Yes, Add it to the list
    - No more segments to check
    """
    def get_segment_overlaps(s, fillers):
        return [i for i in fillers
            if i["start"] < i["end"] and
            i["start"] < s["end"] and
            i["end"] > s["start"]]
    
    def slice_filler_from_segment(s, f):
        """this function requires [   segment   [filler] ]
        where [filler] is contained within [segment]. [filler] may touch either boundary
        returns: [[segment_1],[segment_2]], discarding any zero-length segments"""
        segment_is_normal = s["start"] < s["end"]
        filler_is_normal = f["start"] < f["end"]
        filler_start_is_contained = f["start"] >= s["start"]
        filler_end_is_contained = f["end"] <= s["end"]
        if not segment_is_normal and filler_is_normal and filler_start_is_contained and filler_end_is_contained:
            Utils.print_to_log("ERROR: Malformed segments in slice_filler_from_segment()", {"s": s, "f": f})
            return []
        slices = [dict(s), dict(s)]
        # split this segment into [ s1 [f] s2 ]
        # s1 spans from start:s.start, end:f.start
        slices[0] = {
            **slices[0],
            "end": f["start"],
            "duration": f["start"] - s["start"],
            "filename": f"{s["filename"]}_0"
        }
        # s2 spans from start:f.end, end:s.end
        slices[1] = {
            **slices[1],
            "start": f["end"],
            "duration": s["end"] - f["end"],
            "filename": f"{s["filename"]}_1"
        }
        nonzero_length = [x for x in slices if x["end"] - x["start"] > 0.0]
        return nonzero_length

    candidates = [generic]
    overlaps = get_segment_overlaps(generic, fillers)
    cleared_segments = []
    # keep looping if any candidate has overlaps
    loops = 0
    while (len(overlaps)):
        if loops > c.MAX_LOOPS:
            Utils.print_to_log("ERROR: Maximum loops reached in get_segment_overlaps()", {"generic": generic, "fillers": fillers})
            cleared_segments = []
            break
        for i, j in enumerate(candidates):
            overlaps = get_segment_overlaps(j, fillers)
            if len(overlaps) == 0:
                cleared_segments.append(j)
            else:
                # remove cleared segments from overlap list
                candidates = candidates[i:]
                break
        # candidates[0] is the next target to slice
        if candidates and overlaps:
            candidates = slice_filler_from_segment(candidates[0], overlaps[0])
        else:
            if not overlaps:
                # success
                Utils.print_to_log(f"[{len(fillers)}] overlaps removed from segment [{generic["filename"]}] resulting in [{len(cleared_segments)}] new segments")
            if not candidates:
                # ???
                Utils.print_to_log(f"WARN: Segment [{generic["filename"]}] resulted in [{len(candidates)}] candidate segments in get_segment_overlaps()", {"generic": generic, "fillers": fillers})
        loops += 1
    return cleared_segments

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
    user_cuts = parse_segment_cuts(proj_cuts, options)
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