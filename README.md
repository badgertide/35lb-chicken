# 35lb-chicken

## What is this?
35-Pound Chicken is a tool that I built to trim the filler from  One Piece. The aim is to allow the user to select which types of filler they are okay with and re-cut the existing video in a controlled manner.

## Why not just watch One Pace?
One Pace is great and I deeply respect all of the quality work that team has managed to do. However, while I feel that attempting to speed up the pacing of One Piece is a noble goal, that is not what One Pace does (at time of writing in 2026). It fixes pacing, but it also rewrites the anime to be more of a video version of the manga.

I believe that the anime and the manga are two different things and there are things to love about both. Therefore, I aim to re-cut the anime as it is, trimming out as much dead weight as possible while retaining the anime as it was released. No reconstructions, no upscaling, no remakes of scenes spliced in from movies.

## Is this piracy?
No, everything in this project is my own making, minus the titles on the templates. You supply the video and I will cut the videos down to size.

---

### Segment Types
* **production** 
    * Used to denote opening logos, animation sequences.
    * Optionally played at the beginning of an episode run.
    * Not stretched.
* **themeopen**
    * Used to denote theme songs and jingles.
    * Played at the beginning of an episode run.
    * Not stretched.
* **easein**
    * Used to mark the section of recap footage before an episode starts.
    * Generally has a corresponding easeout in the previous episode.
* **segment**
    * The generic segment type. Used to denote time frames that should be kept under all circumstances.
* **eyecatcher**
    * Used to denote ease in/outs around commercial breaks.
    * Optionally keep the first or last eyecatcher.
* **easeout**
    * Used to mark the section of footage leading up to a cliffhanger or end of episode.
    * Generally has a corresponding easein in the next episode.
* **themeclose**
    * Used to denote theme songs and jingles.
    * Played at the end of an episode run.
    * Not stretched.
* **teaser**
    * Used to denote "next time on" segments.
    * Optionally played at the end of an episode run.
* **signoff**
    * Used to denote any trailing production logos or splash screens.
    * Optionally played at the beginning of an episode run.
    * Not stretched.
* **filler**
    * Does nothing, but can be useful as a marking tool.
    * Never included in the render under any circumstances.

### Rules (Provisional)
* Cut seasons into n-episode runs, spreading the distribution as needed (a 28-episode season split into 5-ep chunks could be split up like 5-5-5-5-4-4)
* Play `production` and `themeopen` on the first episode in a run
* Play only the first `eyecatcher` in any episode
* Play `themeclose` and `signoff` on the last episode in a run
* If an episode has an `easeout`, check the next episode for an `easein`. If one exists, skip this segment