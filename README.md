# JATP — "The Crossing" (unofficial finale trailer)

A personal, non-commercial fan project: an unofficial Season 1 finale **trailer** for
*Julie and the Phantoms*, resolving the show's cliffhanger ("Option D — The Crossing").

## What's here
- `CLAUDE.md` — story bible (characters, magic rules, season arc, cliffhanger).
- `PLAN.md` — project plan, decisions, and pipeline notes.
- `SHOTLIST.md` — the ~2:30 trailer shot list (20 shots + 5 text cards).
- `extract_char.sh` — pulls character reference frames from episode video (ffmpeg).
- `refs/storybook/` — photorealistic character portraits (Gemini "Nano Banana Pro").
- `refs/frames/` — per-shot first-frame stills used to seed video generation.
- `renders/` — the 20 generated Veo clips (`S01`–`S20`).
- `build/trailer_v1.mp4` — the assembled trailer (cut + song + cards + grade).
- `Don't Let Go.mp3` — the centerpiece song (AI-generated for this project).

## Pipeline
reference frames → character portraits & first-frame stills (Gemini 3 Pro Image) →
image-to-video per shot (Veo 3 on Vertex) → assemble + score in ffmpeg.

## Not included (excluded via .gitignore)
Raw episode video (`*.mkv`) and ripped subtitles (`*.srt`) — third-party copyrighted
source material, not redistributed here.

---
*Fan work for personal use. Julie and the Phantoms and its characters are © their respective owners.*
