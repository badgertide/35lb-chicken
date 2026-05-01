# Style Guide
Things you should know if you intend on writing your own cut for a show

## Segment Types
Any segment may be written like `name|note` to indicate descriptions or general notes on why a cut was made

### Beginning Segments
<details><summary> production - the opening logo or splash screen for the production company </summary>

* Used to denote opening logos, animation sequences
* Optionally played at the beginning of an episode run
</details>

<details><summary> themeopen </summary>

* Used to denote theme songs and jingles
* Played at the beginning of an episode run
</details>

<details><summary> recap - the compressed version of the previous episode </summary>

* Used to denote a segment at the beginning of an episode where clips from the previous episode(s) are played in sqeuence
* Not played unless it's at the beginning of an episode run
</details>

### Middle Segments
<details><summary> titlecard </summary>

* Used to denote the segment where the episode title is shown
* This can be left in or out depending on if you feel that episode titles are spoilers
</details>

<details><summary> generic </summary>

* The generic segment type. Played under all circumstances
* Can contain `filler` segments
</details>

<details><summary> eyecatcher - the commercial bumpers </summary>

* Used to denote the bumpers around commercial breaks
* Optionally keep the first or last eyecatcher
</details>

### Ending Segments
<details><summary> easeout - the bit leading up to a cliffhanger </summary>

* Used to mark the section of footage leading up to a cliffhanger or end of episode. There is generally a corresponding bit at the beginning of the next episode that re-states this without the drama.
* Not played unless this is the last episode in a run
</details>

<details><summary> tbc - To Be Continued </summary>

* Marks the "To Be Continued" panel
* Not played unless this is the last episode in a run
</details>

<details><summary> themeclose </summary>

* Used to denote theme songs and jingles
* Not played unless this is the last episode in a run
</details>

<details><summary> teaser - the bit where it tells you what's in the next episode </summary>

* Used to denote "next time on" segments
* Optionally played at the end of an episode run
</details>

<details><summary> signoff - splash panel at the end of the episode </summary>

* Used to denote any trailing production logos or splash screens
* Optionally played at the end of an episode run
</details>

<details><summary> filler - unnecessarily long or useless scenes </summary>

* Used to mark segments that should never be included in the render under any circumstances
* Optionally the tag is written as `filler|description` to describe the scene or the reason it was selected for pruning. If you want to search through these and remove segments that you want to keep, that's perfectly fine
* **IMPORTANT** - `filler` tags can be placed within larger `generic` tags, but they must be entirely contained within one tag without extending beyond either border or overlapping another `filler`. Placing a `filler` tag within any other tag will have no effect
</details>

<details><summary> noncanon - cut all noncanon scenes (except G-8) </summary>

* Not currently used. Allows for the option of a more aggressive cut with even more scenes removed
* The same as `filler`. Cuts out all scenes from the anime that are non-canon
</details>

### Rules (Provisional)
* Cut seasons into n-episode runs, spreading the distribution as needed (a 28-episode season split into 5-ep chunks could be split up like 5-5-5-5-4-4)
* Play `production`, `themeopen`, and `recap` on the first episode in a run
* Optionally skip the `titlecard`, though this will often lead to jump-cuts when music is playing
* Play only the first `eyecatcher` in any episode
* Play `easeout`, `tbc`, `themeclose` and `signoff` on the last episode in a run