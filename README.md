# An AI-Assisted Pipeline for an Unofficial Series Finale: Screenplay, Trailer, and Illustrated Storybook

## Abstract

This repository documents a reproducible pipeline for producing an unofficial Season 1 finale
for *Julie and the Phantoms*, a Netflix series cancelled after one season on an unresolved
cliffhanger. Three artifacts are generated from a single source corpus: a complete
**screenplay**, a ~2-minute **photorealistic trailer**, and an illustrated **storybook**
(web and PDF). The work combines frame extraction (ffmpeg), image synthesis (Gemini 3 Pro
Image, "Nano Banana Pro"), image-to-video synthesis (Veo 3, Vertex AI), and deterministic
layout/assembly (ImageMagick, ffmpeg). The sections below describe the method, report several
practical constraints encountered with current generative-video safety systems, and catalog
the resulting artifacts.

> **Status:** fan work; personal, non-commercial, fair-use. *Julie and the Phantoms* and its
> characters remain the property of their respective owners. No copyrighted source video or
> subtitles are redistributed here (`.mkv` / `.srt` are excluded via `.gitignore`).

---

## 1. Background and problem statement

The source series concludes with several unresolved narrative threads: the protagonists (three
ghost musicians) remain bound by an antagonist's curse; the antagonist has possessed a living
character; an established rule (ghosts cannot touch the living) is unexpectedly broken; and two
relationships and a plagiarism subplot are left open. A story bible was first compiled from the
season to fix the canonical constraints that any continuation must respect:

- The curse ("the stamp") escalates from intermittent pain to permanent non-existence; the only
  established escape is completing "unfinished business" and crossing over, which also nullifies
  the curse. The characters had assumed their unfinished business was a specific performance;
  having achieved it without crossing over, its true nature is unresolved.
- The ghosts are visible to the living only while performing; their instruments are bound to
  them; the touch exception is treated as the central mystery.
- Tonal constraint: a PG family-musical register — earnest and comedic, with sincere treatment
  of grief and mortality.

These constraints function as the specification against which all generated content is evaluated.

---

## 2. Method

### 2.1 Character references and portrait synthesis

Reference frames were extracted from the available episode video using
[`extract_char.sh`](extract_char.sh), which samples short frame bursts around curated
timestamps; the clearest frame per character was retained. (Only the first episode was
available as video, so most secondary characters are represented by a single reference.)

Each reference was passed to **Gemini 3 Pro Image** under a single fixed style prompt to
produce a consistent portrait set. These portraits serve as **identity anchors** for all
downstream synthesis, mitigating character drift across independently generated images.

![Character portraits](refs/storybook/_contact_sheet.png)

### 2.2 Screenplay

The finale was written as a full episode in Fountain format:
[`screenplay/The_Crossing.fountain`](screenplay/The_Crossing.fountain).

The resolution unifies the open threads through a single device: the characters' "unfinished
business" is reframed as a chain of transmission across twenty-five years (their early
recording reached the protagonist's late mother, whose songwriting the protagonist now
performs). Completing that chain, rather than achieving a performance, satisfies the condition.
A final reversal — the touch exception — anchors the characters to the living world instead of
removing them, neutralizing the antagonist's fear-based power and resolving the remaining
relationship and plagiarism threads. The episode is structured around an original song,
"Don't Let Go."

### 2.3 Trailer shot list

Because generative video is currently limited to short clips, the finale was decomposed into a
**20-shot, 5-act trailer** (*Joy → Threat → Choice → Performance → Reversal*). Each shot was
specified with a duration (≤8 s), the character references required for likeness, a
first-frame still concept, and an audio cue. A first-frame establishing still was synthesized
per shot (Gemini 3 Pro Image), conditioned on the relevant portraits.

![Trailer storyboard](refs/frames/_storyboard.png)

<details>
<summary><b>Full shot list (expand)</b></summary>

| # | Beat | Shot |
|---|------|------|
| S01 | Joy | The band, whole, in the studio |
| S02 | Joy | The touch — a hand rests solid (thematic seed) |
| S03 | Joy | An unresolved almost-moment |
| S04 | Threat | The antagonist's club; the curse-mark glows |
| S05 | Threat | The jolt — electrical flare, blown bulbs |
| S06 | Threat | The warning at the skate park |
| S07 | Threat | Possession on the street |
| S08 | Threat | The possessed character approaches |
| S09 | Threat | The protagonist senses something wrong |
| S10 | Choice | The verdict — crossing over means leaving |
| S11 | Choice | Heartbreak |
| S12 | Choice | Stakes in the living world |
| S13 | Choice | The stolen-legacy subplot |
| S14 | Performance | Stage reveal — the band materializes |
| S15 | Performance | Lead vocal at the piano |
| S16 | Performance | The duet |
| S17 | Performance | The rhythm section |
| S18 | Performance | The crossing-over light begins |
| S19 | Reversal | The embrace — the arms close around something solid |
| S20 | Reversal | Closing button: the antagonist behind a character's eyes |

Five trailer **text cards** were added as ffmpeg overlays, allowing dialogue/teaser copy
without dependence on lip-sync.
</details>

### 2.4 Video synthesis

Each first-frame still was animated with **Veo 3** (image-to-video) on Vertex AI via the
asynchronous `:predictLongRunning` endpoint with operation polling. See §3 for constraints.

### 2.5 Assembly

Clips were trimmed, ordered, and combined with ffmpeg; text cards were inserted; a 2.39:1
cinemascope letterbox and a warm grade were applied. The score was integrated by analyzing the
loudness envelope of "Don't Let Go" to locate its quiet introduction, chorus onset, and
fade-out, then constructing a three-segment edit such that the chorus onset coincides with the
Act-4 stage reveal (verified against the assembled timeline).

🎬 **Trailer:** [`build/trailer_v1.mp4`](build/trailer_v1.mp4) — ~2:02, 1280×720.

### 2.6 Storybook

The episode was additionally rendered as an illustrated storybook in two formats: a single-file
web document, [`storybook/story.html`](storybook/story.html), and a print-ready
[`build/storybook.pdf`](build/storybook.pdf). Each beat pairs a synthesized illustration with
prose adapted from the screenplay, in alternating image/text columns so that text never
overlays artwork. The document chrome adopts the palette and typography of the series' key art
(midnight-to-violet palette, brush-script display type); see §3.3 on scoping that adoption. The
PDF is composed as a flat image-per-page document (`storybook/build_pdf.py`) rather than via
browser print-to-PDF, for cross-viewer compatibility (§3.2).

![Storybook cover](storybook/art/cover.png)

---

## 3. Findings: practical constraints

### 3.1 Generative-video safety filtering

The Veo 3 content filter rejected a substantial fraction of shots. The behavior was **not** a
simple prohibition on depicting minors (many shots featuring youthful subjects passed). Rejections
correlated with the **combination of youthful subjects and sensitive themes** (emotional
distress in close-up, menace, possession) and with certain prompt vocabulary. Setting
`personGeneration: "allow_all"` did not resolve it, and filtering was non-deterministic.

The effective mitigation was **compositional rather than parametric** — re-framing affected
beats to convey the same narrative content without a youthful face in distress or menace:

| Shot | Rejection mode | Mitigation |
|------|----------------|------------|
| S07 (possession) | output filtered | Figure shot from behind; menace conveyed by light/atmosphere |
| S08 (uncanny approach) | output filtered | A shadow across a floor; no figure in frame |
| S09 (distress close-up) | output filtered | Over-the-shoulder framing |
| S13 (legacy subplot) | input image rejected (apparent real-person likeness) | Regenerated as objects + silhouette |
| S20 (closing button) | output filtered | Extreme close-up of an eye |

Additional operational notes: preview model identifiers returned `404` on the project
(allowlisting required); the generally-available `veo-3.0-generate-001` was used. A concurrency
quota required submission in waves of ≤5 with operation polling. An empty-payload probe returns
`400` regardless of access and is therefore not a valid access check.

### 3.2 PDF rendering portability

PDFs produced via headless-browser print-to-PDF rendered correctly in Ghostscript but appeared
blank in macOS PDFKit/Preview (attributable to CSS blend-modes and embedded web fonts). Replacing
this with a **flat image-per-page PDF** composed in ImageMagick produced output that renders
identically across viewers; this was verified against PDFKit directly (`qlmanage`).

### 3.3 Style-guide scope

An initial adoption of the series style guide incorporated its *compositional* motifs (ghostly
translucency, smoke/haze) into every image prompt, which introduced those elements into scenes
where they were inappropriate. Restricting the adopted attributes to **palette and typography
only** — and removing compositional language from prompts — yielded grounded, scene-appropriate
illustrations while preserving visual cohesion.

---

## 4. Artifacts

- [`screenplay/The_Crossing.fountain`](screenplay/The_Crossing.fountain) — full episode script
- [`build/trailer_v1.mp4`](build/trailer_v1.mp4) — assembled trailer
- [`storybook/story.html`](storybook/story.html) — web storybook *(rebuild: `storybook/build_html.py`)*
- [`build/storybook.pdf`](build/storybook.pdf) — print storybook *(rebuild: `storybook/build_pdf.py`)*
- `refs/storybook/` — character portrait set (+ contact sheet)
- `refs/frames/` — per-shot first-frame stills (+ storyboard)
- `renders/` — the 20 synthesized video clips
- `storybook/` — illustration set, prose data, and document builders
- [`STYLE_GUIDE.md`](STYLE_GUIDE.md) — derived visual style guide
- [`extract_char.sh`](extract_char.sh) — reference-frame extractor
- `Don't Let Go.mp3` — score

### Pipeline overview

```
episode frames ──► character portraits ──► first-frame stills ──► Veo 3 clips ──► ffmpeg ──► TRAILER
 (ffmpeg)          (Gemini 3 Pro Image)    (Gemini 3 Pro Image)   (Vertex)       (cut + score)
        │                                        │
        └────────► story bible ─► screenplay ────┴──► storybook prose + art ─► HTML / PDF STORYBOOK
```

**Toolchain:** ffmpeg · Gemini 3 Pro Image ("Nano Banana Pro") · Veo 3 (Vertex AI) ·
ImageMagick · Python.

---

## 5. Limitations and future work

- The trailer uses fast-tier video synthesis and start-trimmed clips; planned refinements
  include per-clip in/out selection, smoother audio splicing, an underscore for the middle acts,
  and re-rendering hero shots at a higher-quality tier.
- Only one source episode was available as video, constraining secondary-character references.
- Character consistency across independently generated images is approximate, not guaranteed.
- The continuation deliberately leaves the antagonist available for a subsequent season.
