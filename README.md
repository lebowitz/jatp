# JATP — "The Crossing" (unofficial finale trailer)

A personal, non-commercial fan project: an unofficial Season 1 finale **trailer** for
*Julie and the Phantoms*, resolving the show's cliffhanger ("Option D — The Crossing").

The end product is `build/trailer_v1.mp4` — a ~2:02 photorealistic trailer scored with
the project's centerpiece song, **"Don't Let Go."**

## The two index sheets

**Character portraits** — one photorealistic, style-consistent portrait per main character
(`refs/storybook/_contact_sheet.png`):

![Character portraits](refs/storybook/_contact_sheet.png)

**Trailer storyboard** — the first-frame still for each of the 20 shots
(`refs/frames/_storyboard.png`):

![Trailer storyboard](refs/frames/_storyboard.png)

## The process

1. **Reference frames.** `extract_char.sh` pulls bursts of candidate frames from the
   episode video around curated timestamps; the best, clearest frame per character is kept
   as a reference. *(Only E1 had video on hand, so most secondary characters were sourced
   from a single labeled reference each.)*
2. **Character portraits.** Each reference is fed to **Gemini 3 Pro Image ("Nano Banana
   Pro")** with one fixed style prompt, producing the style-consistent photorealistic
   portrait set above. These portraits are the *consistency anchors* for everything after.
3. **Story + shot list.** The cliffhanger is resolved as "Option D — The Crossing"
   (`PLAN.md`), broken into a 20-shot, 5-act trailer (`SHOTLIST.md`): Joy → Threat →
   Choice → Farewell Performance → Reversal.
4. **First-frame stills.** For every shot, a establishing still is generated (Nano Banana
   Pro again), passing the relevant character portraits so faces/wardrobe stay consistent.
   These become the storyboard above and the seed frames for video.
5. **Video.** Each still is animated with **Veo 3** (image-to-video, on Vertex AI) into an
   8s clip (`renders/S01`–`S20`). Several shots had to be recomposed to clear Veo's safety
   filters (faceless/atmosphere framing for the menace beats); details in `PLAN.md`.
6. **Assembly.** ffmpeg trims and orders the clips, inserts 5 trailer text cards, lays the
   edited song so its chorus drops on the Act 4 stage reveal, applies a cinemascope
   letterbox and warm grade, and muxes the final cut → `build/trailer_v1.mp4`.

## Contents
- `CLAUDE.md` — story bible (characters, magic rules, season arc, cliffhanger).
- `PLAN.md` — project plan, decisions, model IDs, and pipeline notes.
- `SHOTLIST.md` — the trailer shot list (20 shots + 5 text cards).
- `screenplay/The_Crossing.fountain` — the full episode screenplay (Fountain format).
- `extract_char.sh` — reference-frame extractor (ffmpeg).
- `refs/storybook/` — photorealistic character portraits (+ contact sheet).
- `refs/frames/` — per-shot first-frame stills (+ storyboard; `*_orig.png` = pre-recompose).
- `renders/` — the 20 generated Veo clips (`S01`–`S20`).
- `build/trailer_v1.mp4` — the assembled trailer.
- `Don't Let Go.mp3` — the centerpiece song (AI-generated for this project).

## Not included (excluded via .gitignore)
Raw episode video (`*.mkv`) and ripped subtitles (`*.srt`) — third-party copyrighted
source material, not redistributed here.

---
*Fan work for personal use. Julie and the Phantoms and its characters are © their respective owners.*
