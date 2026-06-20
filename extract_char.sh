#!/usr/bin/env bash
#
# JATP character reference-frame extractor
# ------------------------------------------------------------
# Pulls a small BURST of frames around each curated timestamp so you can
# pick the cleanest face shot (no blinks, no motion blur, front-facing).
#
# REQUIREMENTS: ffmpeg installed and on your PATH.
#   macOS:    brew install ffmpeg
#   Windows:  winget install ffmpeg   (or download from ffmpeg.org)
#   Linux:    sudo apt install ffmpeg
#
# SETUP:
#   1. Put your episode video files in the same folder as this script,
#      OR edit the EPxx paths below to point at them.
#   2. Make executable:   chmod +x extract_frames.sh
#   3. Run:               ./extract_frames.sh
#
# OUTPUT: ./refs/<Character>/E<ep>_<timestamp>_<n>.png
#         A handful of stills per character. Keep the best, delete the rest.
# ------------------------------------------------------------

set -euo pipefail

# ---- EDIT THESE to match YOUR filenames ----
EP01="Julie.And.The.Phantoms.S01E01.1080p.NF.WEB-DL.DDP5.1.Atmos.H.264-NTb.mkv"
EP02="S01E02.mkv"
EP03="S01E03.mkv"
EP04="S01E04.mkv"
EP05="S01E05.mkv"
# (only the episodes we actually pull from are needed)
# --------------------------------------------

# How many frames per burst, and the gap between them (seconds).
BURST=10
GAP=1.5

# grab <file> <start_timestamp HH:MM:SS> <character> <episode_tag>
grab () {
  local file="$1" start="$2" char="$3" eptag="$4"
  if [[ ! -f "$file" ]]; then
    echo "  ! missing $file — skipping $char ($eptag)"; return
  fi
  local outdir="refs/${char}"
  mkdir -p "$outdir"
  echo "  • $char  $eptag @ $start"
  # Seek a touch before the cue so the burst straddles the moment.
  ffmpeg -nostdin -loglevel error -ss "$start" -i "$file" \
    -frames:v "$BURST" -vf "fps=1/${GAP},scale=-1:1080" \
    "${outdir}/${eptag}_$(echo "$start" | tr ':,' '__')_%02d.png"
}

echo "Extracting reference bursts..."

# ---- JULIE ----
grab "$EP01" 00:18:28 Julie E01     # "It's Julie." — direct intro, faces camera
grab "$EP01" 00:08:09 Julie E01     # featured close moment
grab "$EP01" 00:06:11 Julie E01     # kitchen scene with brother

# ---- LUKE ----
grab "$EP01" 00:03:07 Luke E01      # "I'm Luke, by the way" — intro
grab "$EP01" 00:18:30 Luke E01      # second clear intro beat
grab "$EP02" 00:06:25 Luke E02      # studio, well-lit

# ---- ALEX ----
grab "$EP01" 00:02:35 Alex E01      # "Alex, you were smoking" — featured
grab "$EP01" 00:18:37 Alex E01      # "Alex. How's it going?"

# ---- REGGIE ----
grab "$EP01" 00:03:09 Reggie E01    # "I'm Reggie" — intro
grab "$EP01" 00:18:34 Reggie E01    # second intro beat

# ---- WILLIE ----
grab "$EP03" 00:09:43 Willie E03    # "I'm Willie" — intro
grab "$EP04" 00:24:12 Willie E04    # "Cool. I'm Willie." — clean

# ---- CALEB ----
grab "$EP05" 00:06:50 Caleb E05     # "Hello, boys. Caleb Covington." — featured
grab "$EP05" 00:02:11 Caleb E05     # stage intro / spotlight

# ---- NICK ----
grab "$EP01" 00:07:35 Nick E01      # "Nice job, Nick"
grab "$EP01" 00:06:49 Nick E01      # featured

# ---- CARRIE ----
grab "$EP01" 00:06:34 Carrie E01    # featured
grab "$EP02" 00:23:18 Carrie E02    # performance-adjacent, well-lit

# ---- FLYNN ----
grab "$EP01" 00:06:44 Flynn E01     # featured
grab "$EP02" 00:01:57 Flynn E02

# ---- TREVOR / BOBBY (present-day) ----
grab "$EP04" 00:14:31 Trevor E04    # name-drop scene context

# ---- CARLOS ----
grab "$EP01" 00:06:02 Carlos E01    # kitchen sibling banter ("Hey, underachiever")
grab "$EP01" 00:19:10 Carlos E01    # family dinner — "Your turn, Carlos"
grab "$EP01" 00:19:22 Carlos E01    # dinner, later beat ("Carlos tells me he...")
grab "$EP01" 00:22:04 Carlos E01    # family scene ("you and Carlos, I see Mom")

# ---- RAY (dad) ----
grab "$EP01" 00:12:48 Ray E01

echo
echo "Done. Look in ./refs/<Character>/ and keep the best frame from each burst."
echo "Tip: open a folder in your image viewer and arrow through — the sharpest,"
echo "     eyes-open, front-facing frame is your reference."