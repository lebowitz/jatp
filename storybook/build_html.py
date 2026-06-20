#!/usr/bin/env python3
"""Build a beautiful single-file HTML storybook from story_data.json + art/."""
import json, html, os

HERE=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(os.path.join(HERE,"story_data.json")))

# act dividers keyed by the page id they precede
ACTS={
 "p02":"Prologue",
 "p06":"Act One · The Clock",
 "p10":"Act Two · The Line",
 "p14":"Act Three · The Choice",
 "p17":"Act Four · The Crossing",
 "p24":"Tag · Don't Let Go",
}

def paras(prose):
    out=[]
    for i,blk in enumerate(prose.split("\n\n")):
        t=html.escape(blk.strip())
        if not t: continue
        cls=' class="lead"' if i==0 else ""
        out.append(f"<p{cls}>{t}</p>")
    return "\n".join(out)

cover=next(d for d in data if d["layout"]=="cover")
beats=[d for d in data if d["layout"]!="cover"]

sections=[]
n=0
for d in beats:
    if d["id"] in ACTS:
        sections.append(f'<div class="act"><span>{html.escape(ACTS[d["id"]])}</span></div>')
    flip=" flip" if n%2 else ""
    n+=1
    sections.append(f'''<section class="beat{flip}">
  <figure class="art"><img loading="lazy" src="art/{d['art']}" alt=""></figure>
  <div class="copy">{paras(d['prose'])}</div>
</section>''')

HTML=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Julie and the Phantoms — The Crossing</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Anton&family=Spectral:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
:root{{
  --void:#070612; --void2:#0d0a22; --violet:#7c4dff; --violet-soft:#b69dff;
  --magenta:#d65ad0; --ink:#ece9ff; --muted:#9c93c8; --line:rgba(124,77,255,.35);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{
  margin:0; background:var(--void); color:var(--ink);
  font-family:'Spectral',Georgia,serif; line-height:1.75; font-size:19px;
  background-image:
    radial-gradient(1200px 700px at 50% -10%, rgba(124,77,255,.18), transparent 60%),
    radial-gradient(900px 600px at 90% 30%, rgba(214,90,208,.10), transparent 55%),
    radial-gradient(900px 600px at 5% 70%, rgba(124,77,255,.10), transparent 55%);
  background-attachment:fixed;
}}
img{{display:block;max-width:100%}}

/* ---------- cover ---------- */
.cover{{position:relative;min-height:100vh;display:grid;place-items:center;text-align:center;overflow:hidden}}
.cover .bg{{position:absolute;inset:0;background:url("art/{cover['art']}") center/cover no-repeat;
  filter:saturate(1.05) brightness(.8) hue-rotate(-6deg)}}
.cover .scrim{{position:absolute;inset:0;
  background:linear-gradient(180deg, rgba(7,6,18,.45) 0%, rgba(7,6,18,.15) 35%, rgba(7,6,18,.85) 100%)}}
.cover .lockup{{position:relative;z-index:2;padding:6vh 5vw}}
.tagline{{font-family:'Permanent Marker',cursive;color:var(--violet-soft);
  letter-spacing:.04em;font-size:clamp(15px,2.4vw,24px);margin:0 0 4vh;text-shadow:0 2px 18px rgba(124,77,255,.6)}}
.t-julie{{font-family:'Permanent Marker',cursive;color:#fff;line-height:.9;
  font-size:clamp(46px,9vw,118px);text-shadow:0 4px 30px rgba(124,77,255,.7),0 0 60px rgba(214,90,208,.35)}}
.t-phantoms{{font-family:'Anton',sans-serif;letter-spacing:.16em;color:#fff;
  font-size:clamp(34px,7vw,86px);margin:.1em 0 0;text-shadow:0 4px 24px rgba(0,0,0,.6)}}
.t-cross{{font-family:'Permanent Marker',cursive;color:var(--magenta);
  font-size:clamp(30px,6vw,76px);margin:.25em 0 0;text-shadow:0 0 36px rgba(214,90,208,.6)}}
.scroll{{position:absolute;bottom:26px;left:0;right:0;z-index:2;color:var(--muted);
  font-family:'Anton',sans-serif;letter-spacing:.3em;font-size:13px;animation:bob 2s ease-in-out infinite}}
@keyframes bob{{50%{{transform:translateY(8px)}}}}

/* ---------- story flow ---------- */
.wrap{{max-width:1180px;margin:0 auto;padding:2vh 24px 10vh}}
.act{{text-align:center;margin:13vh 0 9vh}}
.act span{{font-family:'Permanent Marker',cursive;color:var(--magenta);
  font-size:clamp(22px,3.6vw,38px);position:relative;padding:0 28px}}
.act span::before,.act span::after{{content:"";position:absolute;top:50%;width:18vw;max-width:230px;height:1px;
  background:linear-gradient(90deg,transparent,var(--line),transparent)}}
.act span::before{{right:100%}} .act span::after{{left:100%}}

.beat{{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(28px,5vw,72px);align-items:center;
  margin:9vh 0;opacity:0;transform:translateY(28px);transition:opacity .9s ease,transform .9s ease}}
.beat.in{{opacity:1;transform:none}}
.beat.flip .art{{order:2}}
.art{{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);
  box-shadow:0 26px 70px rgba(0,0,0,.6), 0 0 0 1px rgba(255,255,255,.03), 0 0 60px rgba(124,77,255,.12)}}
.art img{{width:100%;filter:saturate(1.06) contrast(1.02)}}
.art::after{{content:"";position:absolute;inset:0;mix-blend-mode:soft-light;pointer-events:none;
  background:linear-gradient(150deg, rgba(124,77,255,.45), rgba(214,90,208,.25) 55%, rgba(7,6,18,.5))}}
.copy p{{margin:0 0 1.1em;color:#dfdbf5}}
.copy .lead{{font-size:1.06em}}
.copy .lead::first-letter{{font-family:'Anton',sans-serif;float:left;line-height:.8;
  font-size:3.1em;padding:6px 12px 0 0;color:var(--magenta)}}

footer{{text-align:center;padding:8vh 24px 12vh;color:var(--muted);border-top:1px solid var(--line);margin-top:6vh}}
footer .end{{font-family:'Permanent Marker',cursive;color:var(--violet-soft);font-size:clamp(20px,3vw,30px);margin-bottom:1.2em}}
footer small{{display:block;max-width:640px;margin:0 auto;font-size:13px;line-height:1.6;opacity:.8}}

@media(max-width:760px){{
  .beat,.beat.flip{{grid-template-columns:1fr;gap:22px}}
  .beat.flip .art{{order:0}}
  body{{font-size:18px}}
}}
</style></head>
<body>

<header class="cover">
  <div class="bg"></div><div class="scrim"></div>
  <div class="lockup">
    <p class="tagline">You only live once, but you can rock forever</p>
    <div class="t-julie">Julie and the</div>
    <div class="t-phantoms">PHANTOMS</div>
    <div class="t-cross">The Crossing</div>
  </div>
  <div class="scroll">SCROLL</div>
</header>

<main class="wrap">
{chr(10).join(sections)}
</main>

<footer>
  <div class="end">Tonight, the band is whole.</div>
  <small>An unofficial, non-commercial fan continuation of <em>Julie and the Phantoms</em>.
  Story &amp; art generated for personal use. Julie and the Phantoms and its characters are &copy; their respective owners.</small>
</footer>

<script>
const io=new IntersectionObserver((es)=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}}),{{threshold:.15}});
document.querySelectorAll('.beat').forEach(b=>io.observe(b));
</script>
</body></html>'''

open(os.path.join(HERE,"story.html"),"w").write(HTML)
print("wrote storybook/story.html —", len(beats), "beats,", HTML.count("<section"), "sections")
