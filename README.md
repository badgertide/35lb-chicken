# 35lb-chicken

## What is this?
35-Pound Chicken is a tool that I built to trim the filler from your One Piece videos. The aim is to allow the user to select which types of video they would like to keep and re-cut the existing video in a controlled manner. So if they would like to keep the theme songs, but not the recaps, that should be allowed.

## The Goal
35PC attempts to re-pace One Piece, cutting out filler, plus most recaps and theme songs. The goal is not to FIX the pacing, but to alleviate it by skipping the most egregious filler. Additionally, while skipping filler *scenes* is a priority, skipping filler *episodes* is not. There are a good number of enjoyable filler episodes that add elements to the story. If you wish to skip those, you may do so at your own better judgement.

## Will this tool give me a professional, seamless recut?
No. That's the ideal that I strive for, but it is not possible in all cases. 35PC attempts to cut fat out of the video and paste it back together with no further editing, essentially fast-forwarding through the show as directed. This means that sometimes the best skip will happen in the middle of a musical piece or a scene. I try to avoid this as much as possible, but occasionally it is unavoidable.

## Why not just watch One Pace?
Yeah, you can do that. One Pace is great and I deeply respect all of the quality work that team has managed to do. However, while I feel that attempting to speed up the pacing is a noble goal, One Pace is more of a video version of the manga.

## Is this piracy?
No, everything in this project is my own making, minus the titles on the templates. You supply the video and I will cut the videos down to size.

---
---

# Setup

**Step 1**: In order for all of this to work, `ffmpeg` and `ffprobe` need to be found on the system PATH. If you can run both programs from the command line, then you are good to go.

<details><summary>Windows</summary>

* Check if ffmpeg and ffprobe are installed
  > _ ffmpeg ffprobe
* If either program is not installed, you will need to install them
* TODO - Instructions on how to install FFMPEG and FFProbe for Windows
</details>

<details><summary>Linux/MacOS</summary>

* Check if ffmpeg and ffprobe are installed
  > where ffmpeg ffprobe
* If neither shows up, use your preferred package manager to install `ffmpeg`, which will also install ffprobe
  > brew install ffmpeg
</details>

**Step 2**: 35PC should work on any copy of One Piece, but it is specifically geared to work on one specific cut