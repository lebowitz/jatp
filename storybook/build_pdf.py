#!/usr/bin/env python3
"""Build an image-based PDF (universally renderable) from story_data.json + art/.
Landscape pages, art beside text (alternating sides), styled to STYLE_GUIDE."""
import json,os,subprocess
HERE=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(os.path.join(HERE,"story_data.json")))
OUT=os.path.join(HERE,"pdfpages"); os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith(".png"): os.remove(os.path.join(OUT,f))

W,H="2000","1414"
GRAD=f"radial-gradient:#241a4d-#060610"
TXT="#ece9ff"; MAG="#d65ad0"; BORDER="#4a3a85"; PG="#9a8fce"
ACTS={"p02":"Prologue","p06":"Act One · The Clock","p10":"Act Two · The Line",
      "p14":"Act Three · The Choice","p17":"Act Four · The Crossing","p24":"Tag · Don't Let Go"}
def sh(*a): subprocess.run(list(a),check=True)
def bg(dst): sh("magick","-size",f"{W}x{H}",GRAD,dst)
def artimg(src,dst,h=1180):
    sh("magick",src,"-resize",f"x{h}","-bordercolor",BORDER,"-border","4",dst)

pages=[]; idx=[0]
def nextpage():
    p=os.path.join(OUT,f"{idx[0]:03d}.png"); idx[0]+=1; pages.append(p); return p

cover=next(d for d in data if d["layout"]=="cover")
beats=[d for d in data if d["layout"]!="cover"]

# ---- cover (art left, title lockup right) ----
p=nextpage(); bg("/tmp/_cbg.png")
artimg(os.path.join(HERE,"art",cover["art"]),"/tmp/_cart.png",h=1230)
sh("magick","/tmp/_cbg.png","/tmp/_cart.png","-gravity","west","-geometry","+150+0","-composite",
   "-gravity","east","-font","SignPainter-HouseScript","-fill",TXT,"-pointsize","34","-annotate","+150-320","You only live once, but you can rock forever",
   "-gravity","east","-font","SignPainter-HouseScriptSemibold","-fill","#f6f2ff","-pointsize","120","-annotate","+150-170","Julie and the",
   "-gravity","east","-font","Helvetica-Bold","-fill","#ffffff","-pointsize","78","-annotate","+170-10","P H A N T O M S",
   "-gravity","east","-font","SignPainter-HouseScript","-fill",MAG,"-pointsize","104","-annotate","+150+160","The Crossing",
   p)

n=0
for d in beats:
    if d["id"] in ACTS:
        p=nextpage(); bg("/tmp/_abg.png")
        sh("magick","/tmp/_abg.png",
           "(","-size","520x3","xc:"+MAG,")","-gravity","center","-geometry","+0-90","-composite",
           "-gravity","center","-font","SignPainter-HouseScript","-fill",MAG,"-pointsize","96","-annotate","+0+0",ACTS[d["id"]],
           p)
    flip=(n%2==1); n+=1
    p=nextpage(); bg("/tmp/_bbg.png")
    artimg(os.path.join(HERE,"art",d["art"]),"/tmp/_bart.png",h=1180)
    open("/tmp/_pr.txt","w").write(d["prose"])
    sh("magick","-background","none","-fill",TXT,"-font","Georgia","-interline-spacing","14",
       "-size","780x1080","caption:@/tmp/_pr.txt","/tmp/_bcap.png")
    if not flip:  # art left, text right
        sh("magick","/tmp/_bbg.png",
           "/tmp/_bart.png","-gravity","west","-geometry","+110+0","-composite",
           "/tmp/_bcap.png","-gravity","east","-geometry","+150+0","-composite",
           "-gravity","south","-font","Georgia","-fill",PG,"-pointsize","30","-annotate","+0+40",str(n),p)
    else:         # text left, art right
        sh("magick","/tmp/_bbg.png",
           "/tmp/_bart.png","-gravity","east","-geometry","+110+0","-composite",
           "/tmp/_bcap.png","-gravity","west","-geometry","+150+0","-composite",
           "-gravity","south","-font","Georgia","-fill",PG,"-pointsize","30","-annotate","+0+40",str(n),p)

# ---- closing page ----
p=nextpage(); bg("/tmp/_fbg.png")
sh("magick","/tmp/_fbg.png",
   "-gravity","center","-font","SignPainter-HouseScript","-fill","#b69dff","-pointsize","80","-annotate","+0-40","Tonight, the band is whole.",
   "-gravity","center","-font","Georgia","-fill",PG,"-pointsize","26","-annotate","+0+90","An unofficial, non-commercial fan continuation of Julie and the Phantoms.",
   p)

print("composed",len(pages),"pages -> building PDF")
sh("magick",*pages,"-quality","90","-density","150","-units","PixelsPerInch",os.path.join(HERE,"..","build","storybook.pdf"))
print("done: build/storybook.pdf")
