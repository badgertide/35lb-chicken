# 35lb-chicken
A tool to facilitate trimming the filler from cartoons, specifically One Piece. The aim is to allow the user to select which types of filler they are okay with and re-cut the existing video in the prescribed manner.

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