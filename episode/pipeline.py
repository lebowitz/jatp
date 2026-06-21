#!/usr/bin/env python3
"""Episode render pipeline (scene-by-scene).

Phases:
  stills    - generate first-frame stills (Gemini 3 Pro Image), parallel
  video     - image-to-video per shot via Veo (with native dialogue audio), in waves
  assemble  - concatenate each scene's clips -> episode/scenes/scene_0N.mp4

DEBUG (default ON now): burns "S<scene> · <shot id>" into every clip during assemble,
for reference while building. Set EPISODE_DEBUG=0 to disable for a clean render.

Usage:
  GTOKEN=$(gcloud auth print-access-token) python3 episode/pipeline.py all --tier fast
  ... or run a single phase: stills | video | assemble
"""
import base64, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS

P="hickory-ai-analytics-prod"; LOC="us-central1"
IMG_MODEL="gemini-3-pro-image-preview"
TOKEN=os.environ.get("GTOKEN","")
HERE=os.path.dirname(os.path.abspath(__file__))
SB=os.path.join(HERE,"..","refs","storybook")
STILLS=os.path.join(HERE,"stills"); CLIPS=os.path.join(HERE,"clips"); SCENES=os.path.join(HERE,"scenes")
for d in (STILLS,CLIPS,SCENES): os.makedirs(d,exist_ok=True)

DEBUG = os.environ.get("EPISODE_DEBUG","1") == "1"
# a font that ffmpeg drawtext can load on macOS
FONT = next((f for f in [
  "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
  "/System/Library/Fonts/Supplemental/Arial.ttf",
  "/System/Library/Fonts/Helvetica.ttc",
] if os.path.exists(f)), None)

IMG_STYLE=(" Photorealistic cinematic film still, 16:9, naturalistic lighting appropriate to the scene, "
 "shallow depth of field, faces large and clearly rendered. No text, no lettering. "
 "Each character must match the face, hair, and wardrobe of the corresponding reference image.")

curl_hdr=["-H",f"Authorization: Bearer {TOKEN}","-H","Content-Type: application/json"]

# ---------------- stills ----------------
def gen_still(shot, tries=2):
    out=os.path.join(STILLS,f"{shot['id']}.png")
    if os.path.exists(out): return f"  · {shot['id']} still (exists)"
    parts=[{"inlineData":{"mimeType":"image/png","data":base64.b64encode(open(os.path.join(SB,f"{s}.png"),'rb').read()).decode()}} for s in shot["refs"]]
    parts.append({"text":shot["still"]+IMG_STYLE})
    body={"contents":[{"role":"user","parts":parts}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"imageConfig":{"aspectRatio":"16:9"}}}
    rf=f"/tmp/est_{shot['id']}.json"; json.dump(body,open(rf,"w"))
    url=f"https://aiplatform.googleapis.com/v1/projects/{P}/locations/global/publishers/google/models/{IMG_MODEL}:generateContent"
    for _ in range(tries):
        d=json.loads(subprocess.run(["curl","-s",url,*curl_hdr,"--data-binary",f"@{rf}"],capture_output=True,text=True).stdout)
        for c in d.get("candidates",[]):
            for p in c.get("content",{}).get("parts",[]):
                if "inlineData" in p:
                    open(out,"wb").write(base64.b64decode(p["inlineData"]["data"])); return f"  ✓ {shot['id']} still"
    return f"  ✗ {shot['id']} still FAILED"

def phase_stills():
    print("PHASE stills (parallel)...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        for line in ex.map(lambda s: gen_still(s), SHOTS): print(line,flush=True)

# ---------------- video ----------------
def _fb(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in("bytesBase64Encoded","videoBytes") and isinstance(v,str): return v
            x=_fb(v)
            if x: return x
    if isinstance(o,list):
        for v in o:
            x=_fb(v)
            if x: return x

def phase_video(tier="fast", wave=4):
    model = "veo-3.0-fast-generate-001" if tier=="fast" else "veo-3.0-generate-001"
    base=f"https://{LOC}-aiplatform.googleapis.com/v1/projects/{P}/locations/{LOC}/publishers/google/models/{model}"
    todo=[s for s in SHOTS if not os.path.exists(os.path.join(CLIPS,f"{s['id']}.mp4"))]
    print(f"PHASE video ({model}); {len(todo)} shots, waves of {wave}")
    import time
    def submit(s):
        img=os.path.join(STILLS,f"{s['id']}.png")
        body={"instances":[{"prompt":s["motion"],"image":{"bytesBase64Encoded":base64.b64encode(open(img,'rb').read()).decode(),"mimeType":"image/png"}}],
              "parameters":{"aspectRatio":"16:9","durationSeconds":8,"sampleCount":1,"generateAudio":True,"resolution":"720p","personGeneration":"allow_all"}}
        rf=f"/tmp/ev_{s['id']}.json"; json.dump(body,open(rf,"w"))
        d=json.loads(subprocess.run(["curl","-s",f"{base}:predictLongRunning",*curl_hdr,"--data-binary",f"@{rf}"],capture_output=True,text=True).stdout)
        return d.get("name"), d.get("error",{}).get("message","")
    results={}
    for i in range(0,len(todo),wave):
        chunk=todo[i:i+wave]; ops={}
        for s in chunk:
            name,err=submit(s)
            if name: ops[s["id"]]=name
            else: results[s["id"]]=f"submit-err: {err[:70]}"; print(f"  ✗ {s['id']} {err[:70]}")
        t0=time.time()
        while ops:
            time.sleep(20)
            for sid in list(ops):
                pf=f"/tmp/evp_{sid}.json"; json.dump({"operationName":ops[sid]},open(pf,"w"))
                d=json.loads(subprocess.run(["curl","-s",f"{base}:fetchPredictOperation",*curl_hdr,"--data-binary",f"@{pf}"],capture_output=True,text=True).stdout)
                if not d.get("done"): continue
                r=d.get("response",{})
                if "error" in d: results[sid]="error"; print(f"  ✗ {sid} error")
                elif r.get("raiMediaFilteredCount"): results[sid]="FILTERED"; print(f"  ⚠ {sid} RAI-filtered")
                else:
                    b=_fb(r)
                    if b: open(os.path.join(CLIPS,f"{sid}.mp4"),"wb").write(base64.b64decode(b)); results[sid]="OK"; print(f"  ✓ {sid}")
                    else: results[sid]="no-video"; print(f"  ✗ {sid} no-video")
                ops.pop(sid)
            if time.time()-t0>600:
                for sid in ops: results[sid]="timeout"
                break
    ok=sum(1 for v in results.values() if v=="OK")
    print(f"video done: {ok}/{len(todo)} ok; issues: "+", ".join(f"{k}={v}" for k,v in results.items() if v!='OK') or "video done: all ok")

# ---------------- assemble ----------------
def label_filter(shot):
    if not (DEBUG and FONT): return "null"
    txt=f"S{shot['scene']} · {shot['id']}"
    return (f"drawtext=fontfile='{FONT}':text='{txt}':x=24:y=20:fontsize=34:fontcolor=yellow:"
            f"box=1:boxcolor=black@0.55:boxborderw=12")

def phase_assemble():
    print(f"PHASE assemble (DEBUG overlay {'ON' if DEBUG else 'off'})")
    scenes={}
    for s in SHOTS: scenes.setdefault(s["scene"],[]).append(s)
    for scene, shots in sorted(scenes.items()):
        listf=f"/tmp/eas_{scene}.txt"; open(listf,"w").write("")
        segs=[]
        for s in shots:
            clip=os.path.join(CLIPS,f"{s['id']}.mp4")
            if not os.path.exists(clip):
                print(f"  (skip {s['id']} — no clip)"); continue
            seg=f"/tmp/easeg_{s['id']}.mp4"
            vf=f"scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,fps=24,{label_filter(s)},format=yuv420p"
            subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-i",clip,"-vf",vf,
                            "-c:v","libx264","-crf","19","-c:a","aac","-b:a","160k",seg],check=True)
            segs.append(seg)
        if not segs: print(f"  scene {scene}: no clips yet"); continue
        with open(listf,"w") as f:
            for seg in segs: f.write(f"file '{seg}'\n")
        out=os.path.join(SCENES,f"scene_{scene:02d}.mp4")
        subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-f","concat","-safe","0","-i",listf,
                        "-c","copy",out],check=True)
        print(f"  ✓ scene {scene} -> {out} ({len(segs)} shots)")

def phase_full():
    """Append all rendered scene files (in scene order) into one episode cut."""
    import glob, re
    files=sorted(glob.glob(os.path.join(SCENES,"scene_*.mp4")),
                 key=lambda p:int(re.search(r"scene_(\d+)",p).group(1)))
    if not files: print("no scene files yet"); return
    listf="/tmp/efull.txt"
    with open(listf,"w") as f:
        for p in files: f.write(f"file '{p}'\n")
    out=os.path.join(HERE,"the_crossing.mp4")
    # scenes share codec/params (uniform re-encode in assemble) -> stream copy
    r=subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-f","concat","-safe","0","-i",listf,"-c","copy",out])
    if r.returncode!=0:  # fallback: re-encode if copy fails
        subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-f","concat","-safe","0","-i",listf,
                        "-c:v","libx264","-crf","19","-c:a","aac","-b:a","160k",out],check=True)
    dur=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],
                       capture_output=True,text=True).stdout.strip()
    print(f"  ✓ full episode -> {out}  ({len(files)} scenes, {dur}s)")

if __name__=="__main__":
    phase=sys.argv[1] if len(sys.argv)>1 else "all"
    tier="fast"
    if "--tier" in sys.argv: tier=sys.argv[sys.argv.index("--tier")+1]
    if phase in ("stills","all"): phase_stills()
    if phase in ("video","all"): phase_video(tier=tier)
    if phase in ("assemble","all"): phase_assemble()
    if phase in ("full","all"): phase_full()
