# -*- coding: utf-8 -*-
"""
The research map. One sky, two arrangements of the same stars:

  "Two axes"     — where I put each study: what kind of AI, and whether it
                   intervenes or observes. Hand-drawn constellations, grey slots
                   for the work still to come.
  "Citation sky" — where the literature puts them: a force simulation over the
                   real citation graph, surrounded by every work they cite.

Switching between the two moves the same stars, so you can see a study travel
from the box I filed it under to the company it actually keeps.
"""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projects import PROJECTS, COLS, ROWS
from constellations import CONSTELLATIONS, CELLBOX
import citelayout as CL

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(HERE)                                          # repo root

# One coordinate space for both arrangements. It is larger than the two-axis
# layout needs, because the citation sky has 600 more points to place and they
# need room to read as a field rather than a smear; the axis view is simply
# scaled up to match, which changes nothing about how it looks.
K = 1.6
W, H = int(1000 * K), int(640 * K)
CANVAS = 1.5                                                       # canvas oversample
COLX = {k: v * K for k, v in {'llm': 342, 'agentic': 578, 'embodied': 814}.items()}
ROWY = {k: v * K for k, v in {'intervention': 196, 'observational': 452}.items()}
CELLBOX = {k: tuple(v * K for v in box) for k, box in CELLBOX.items()}
SIZE = {'Forthcoming': 3, 'Published': 3, 'Deployed': 3, 'Under review': 2}
NEUTRAL = '#8E7FA8'
CBY = {c['id']: c['c'] for c in COLS}

# Short enough to sit under a star. The full title stays in the tooltip.
LABEL = {
    'retrieval': 'LLM oversight',           'errors': 'Detecting AI errors',
    'secd': 'Epistemic calibration',        'creativity': 'AI authenticity',
    'investment': 'Investment expectations','stimulus': 'Stimulus sampling',
    'sales': 'Parallel AI in sales',        'triage': 'AI triage',
    'manufacturing': 'Shop-floor embodied AI', 'service': 'Service robots',
    'misaligned': 'Cost of conformity',     'remote': 'Remote work',
    'hrm': 'AI in HR',                      'edubot': 'EduBot Naija',
    'surgery': 'Robotic surgery',
}

js_cols = [dict(id=c['id'], name=c['name'], sub=c['sub'], c=c['c'], x=COLX[c['id']]) for c in COLS]
js_rows = [dict(id=r['id'], name=r['name'], sub=r['sub'], y=ROWY[r['id']]) for r in ROWS]

def star(p, col_c, **kw):
    venue = p['chip'] + ((' &middot; ' + p['venue']) if p['venue'] else '')
    d = dict(id=p['id'], s=SIZE.get(p['chip'], 1), c=col_c,
             col=p['col'], row=p['row'],
             t=p['short'], lab=LABEL.get(p['id'], p['short']),
             a=[p['authors']] if p['authors'] else [], v=venue,
             f=p['finding'] or 'A short description of this project is coming.',
             n=p['metrics'], href='/research/#' + p['id'])
    d.update(kw)
    return d

# ---------------------------------------------------------- view A: two axes
js_stars, js_slots, js_links = [], [], []
placed = set()
for c in COLS:
    for r in ROWS:
        key = (c['id'], r['id'])
        con = CONSTELLATIONS[key]
        bx, by, bw, bh = CELLBOX[key]
        pos = [(bx + nx * bw, by + ny * bh) for nx, ny in con['pts']]
        mine = sorted([p for p in PROJECTS if p['col'] == c['id'] and p['row'] == r['id']],
                      key=lambda x: x['order'])
        filled = {}
        for i, p in enumerate(mine[:len(pos)]):
            filled[i] = p
            x, y = pos[i]
            js_stars.append(star(p, c['c'], ax=x, ay=y))
            placed.add(p['id'])
        for i, (x, y) in enumerate(pos):
            if i not in filled:
                js_slots.append(dict(x=x, y=y, c=c['c']))
        for i, j in con['links']:
            xi, yi = pos[i]; xj, yj = pos[j]
            js_links.append(dict(x1=xi, y1=yi, x2=xj, y2=yj,
                                 lit=1 if (i in filled and j in filled) else 0, c=c['c']))

# ------------------------------------------------------- view B: citation sky
cworks = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf8'))
cited_ids = set(c for w in cworks for c in w['cited_by'])
cstudies = [p for p in PROJECTS if p['id'] in cited_ids]
cbyid = {p['id']: p for p in cstudies}
sxy, wxy, cworks, _ = CL.layout(cstudies, cworks, box=(W, H))
cpairs = CL.coupling(cstudies, cworks)

# studies that live only in the citation sky (off the two AI axes) still need a star
byid = {s['id']: s for s in js_stars}
for p in cstudies:
    if p['id'] not in placed:
        s = star(p, CBY.get(p['col']) or NEUTRAL)
        js_stars.append(s)
        byid[p['id']] = s
for sid, (x, y) in sxy.items():
    if sid in byid:
        byid[sid]['cx'] = x
        byid[sid]['cy'] = y
        byid[sid]['nref'] = sum(1 for w in cworks if sid in w['cited_by'])

js_works = []
for w in cworks:
    x, y = wxy[w['key']]
    cs = [c for c in w['cited_by'] if c in cbyid]
    au = w['authors'][0] if w['authors'] else ''
    if len(w['authors']) == 2:
        au += ' &amp; ' + w['authors'][1]
    elif len(w['authors']) > 2:
        au += ' et al.'
    js_works.append(dict(
        x=round(x, 1), y=round(y, 1), d=len(cs),
        c='#FFF4D6' if len(cs) > 1 else (CBY.get(cbyid[cs[0]]['col']) or NEUTRAL),
        t=w['title'], a=au, yr=w['year'], v=w['venue'],
        by=[cbyid[c]['short'] for c in cs]))

js_clinks = []
for (a, b), n in sorted(cpairs.items(), key=lambda kv: kv[1]):
    if a in sxy and b in sxy:
        js_clinks.append(dict(x1=sxy[a][0], y1=sxy[a][1],
                              x2=sxy[b][0], y2=sxy[b][1], n=n))

N_CITED = len(js_works)
N_SHARED = sum(1 for w in js_works if w['d'] > 1)
N_CSTUDIES = len(cstudies)

PAGE = u'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research Universe &mdash; Xinyu Fu</title>
<meta name="description" content="A map of Xinyu Fu's research on two axes: what kind of AI a study is about, and whether it asks how the benefit gets built, what it set off, or how to govern that.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
<link rel="icon" href="/profile.png">
<style>
.sky-page{ --void:#120A1F; --dim:#9A8CB4; background:var(--void); color:#EFEAF6 }
.sky-page .nav{ border-bottom-color:#3A2B52 }
.sky-page .brand{ color:#EFEAF6 }
.sky-page .navlinks a{ color:var(--dim) }
.sky-page .navlinks a:hover{ color:#fff; border-color:#6B5A8C }
.sky-page .navlinks a[aria-current="page"]{ background:#EFEAF6; color:var(--void) }
.sky-page .navlinks a.is-cta{ background:var(--coral); color:#1E102F; border-color:var(--coral) }

.sky-head{ padding:26px var(--pad) 20px; border-bottom:1px solid #3A2B52;
  display:flex; gap:24px; align-items:flex-end; flex-wrap:wrap }
.sky-head h1{ font-family:"Archivo",Arial,sans-serif; font-variation-settings:"wdth" 78,"wght" 800;
  text-transform:uppercase; line-height:.92; margin:0; font-size:clamp(30px,5vw,56px);
  color:#fff; letter-spacing:-.015em }
.sky-head p{ margin:0; color:var(--dim); font-size:15px; max-width:44ch; line-height:1.5 }
.sky-head p b{ color:#EFEAF6; font-weight:500 }
.sky-head .hint{ margin-left:auto; font-family:"IBM Plex Mono",monospace; font-size:11px;
  letter-spacing:.13em; text-transform:uppercase; color:var(--dim);
  border:1px solid #3A2B52; padding:8px 12px; white-space:nowrap }

.sky{ position:relative; height:min(76vh,780px); min-height:460px; overflow:hidden;
  background:radial-gradient(120% 90% at 50% 42%, #1E1030 0%, #120A1F 62%, #0C0616 100%);
  cursor:grab; touch-action:none }
.sky.is-drag{ cursor:grabbing }
.sky-world{ position:absolute; top:0; left:0; width:__W__px; height:__H__px;
  transform-origin:0 0; will-change:transform }
.sky-world canvas, .sky-world svg.links{ position:absolute; top:0; left:0;
  width:__W__px; height:__H__px; pointer-events:none }

/* axis handles */
.axis{ position:absolute; background:none; border:0; padding:8px 12px; margin:0;
  color:#EFEAF6; cursor:pointer; font-family:"IBM Plex Mono",monospace;
  font-size:11px; letter-spacing:.15em; text-transform:uppercase; line-height:1.35;
  white-space:nowrap; text-align:left }
.axis i{ display:block; font-style:normal; font-size:9px; letter-spacing:.08em;
  color:var(--dim); margin-top:3px }
.axis .axis-in{ display:inline-block; transform:scale(var(--inv,1)); transform-origin:0 50% }
.axis--col{ transform:translate(-50%,0); text-align:center }
.axis--col .axis-in{ transform-origin:50% 0 }
.axis--row{ transform:translate(0,-50%) }
.axis:hover{ color:#fff }
.axis:hover i{ color:#CFC4E2 }
.axis:focus-visible{ outline:2px solid #fff; outline-offset:4px }

/* Positioned by custom properties rather than left/top so that switching view
   animates the star from one arrangement to the other. */
.star{ position:absolute; left:0; top:0;
  transform:translate(var(--x,0),var(--y,0)) translate(-50%,-50%);
  transition:transform .9s cubic-bezier(.33,.02,.16,1), opacity .5s ease;
  background:none; border:0; padding:0; margin:0; cursor:pointer; display:block }
.star.absent{ opacity:0; pointer-events:none }
.star-dot{
  display:block; width:var(--sz,20px); height:var(--sz,20px); overflow:visible;
  fill:var(--c,#fff);
  filter:drop-shadow(0 0 4px var(--c,#fff)) drop-shadow(0 0 13px var(--c,#fff));
  transform:scale(var(--inv,1)); transform-origin:50% 50%;
}
/* a point in the constellation with no project on it yet */
.slot{ position:absolute; transform:translate(-50%,-50%); pointer-events:none; display:block }
.slot .star-dot{ width:12px; height:12px; fill:#7E6CA0; opacity:.55; filter:none }
.star-name{ position:absolute; left:50%; top:50%;
  transform:translate(-50%,0) scale(var(--inv,1)) translate(0,15px); transform-origin:50% 0;
  font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.04em; line-height:1.3;
  color:#E6DEF4; white-space:nowrap; background:rgba(18,10,31,.86); padding:3px 7px;
  opacity:0; pointer-events:none; transition:opacity .2s ease }
.sky.zoomed .star-name{ opacity:1 }
.star:hover .star-name, .star:focus-visible .star-name{ opacity:1 }
.star:hover .star-dot{ transform:scale(calc(var(--inv,1) * 1.4)) rotate(12deg) }
.star.is-open .star-dot{
  transform:scale(calc(var(--inv,1) * 1.55));
  filter:drop-shadow(0 0 3px #fff) drop-shadow(0 0 10px var(--c,#fff)) drop-shadow(0 0 26px var(--c,#fff));
}
.star:focus-visible{ outline:2px solid #fff; outline-offset:8px }

.sky-ctrl{ position:absolute; right:14px; bottom:14px; z-index:6; display:flex; gap:6px }
.sky-ctrl button{ font-family:"IBM Plex Mono",monospace; font-size:11px; letter-spacing:.1em;
  text-transform:uppercase; background:rgba(18,10,31,.85); color:#E6DEF4;
  border:1px solid #4A3A68; padding:8px 12px; cursor:pointer }
.sky-ctrl button:hover{ background:#EFEAF6; color:#120A1F }

.legend{ position:absolute; left:14px; bottom:14px; z-index:6; display:flex; flex-wrap:wrap;
  gap:4px 14px; font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.08em;
  text-transform:uppercase; color:var(--dim); background:rgba(18,10,31,.72);
  padding:8px 11px; max-width:62% }
.legend span{ display:inline-flex; align-items:center; gap:6px }
.legend b{ width:8px; height:8px; border-radius:50%; display:block }

/* ---------- the two views ---------- */
.axis-layer,.cite-layer{ position:absolute; inset:0; transition:opacity .55s ease }
.sky.mode-cite .axis-layer{ opacity:0; pointer-events:none }
.sky.mode-axis .cite-layer{ opacity:0; pointer-events:none }
.sky.mode-cite .slot{ opacity:0 }

.viewtoggle{ display:inline-flex; border:1px solid #4A3A68; border-radius:2px; overflow:hidden }
.viewtoggle button{ font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.11em;
  text-transform:uppercase; background:transparent; color:var(--dim); border:0;
  padding:9px 13px; cursor:pointer; white-space:nowrap }
.viewtoggle button+button{ border-left:1px solid #4A3A68 }
.viewtoggle button:hover{ color:#fff }
.viewtoggle button[aria-pressed="true"]{ background:#EFEAF6; color:#120A1F }

.cite-links line{ stroke:#C9B6FF; stroke-linecap:round }
.w{ position:absolute; border-radius:50%;
  transform:translate(-50%,-50%) scale(var(--inv,1)); transform-origin:50% 50%;
  cursor:crosshair }
.w:hover{ filter:brightness(1.9) }

/* In the citation sky the names stay up and the solver decides which fit.
   Origin at the star centre with the counter-scale applied LAST, so an inline
   translate is read in screen pixels: scale(1/s) then s cancel, and the offset
   the solver computed is the offset that renders. A percentage translate here
   would be resolved before the counter-scale and land short by a factor of s. */
.sky.mode-cite .star-name{ opacity:1; background:none; left:50%; top:50%;
  transform-origin:0 0; transform:scale(var(--inv,1));
  text-shadow:0 1px 10px #120A1F,0 0 20px #120A1F,0 0 30px #120A1F }
.sky.mode-cite .star-name.no-room{ opacity:0 }
.sky.mode-cite .star:hover .star-name{ opacity:1; z-index:4 }

.tip{ position:absolute; z-index:7; max-width:330px; padding:11px 13px;
  background:rgba(24,15,40,.97); border:1px solid #4A3968; border-radius:3px;
  box-shadow:0 14px 40px rgba(0,0,0,.6); pointer-events:none; opacity:0;
  transition:opacity .12s ease }
.tip.on{ opacity:1 }
.tip .tt{ font-size:13.5px; line-height:1.36; color:#F4EFFA }
.tip .ta{ margin-top:5px; font-family:"IBM Plex Mono",monospace; font-size:10.5px;
  letter-spacing:.06em; color:#A697C0 }
.tip .tb{ margin-top:7px; padding-top:7px; border-top:1px solid #3A2B55;
  font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.08em;
  text-transform:uppercase; color:#DCFF96 }

.blurb{ padding:0 var(--pad); margin:14px 0 0; color:var(--dim); font-size:14px;
  line-height:1.6; max-width:78ch }
.blurb b{ color:#EFEAF6; font-weight:500 }
.blurb.is-off{ display:none }


.index-list{ padding:var(--pad); border-top:1px solid #3A2B52 }
.index-list h2{ font-family:"Archivo",Arial,sans-serif; font-variation-settings:"wdth" 84,"wght" 800;
  text-transform:uppercase; font-size:19px; margin:0 0 6px; color:#fff }
.index-list > p{ color:var(--dim); font-size:14px; margin:0 0 20px; max-width:62ch }
.index-cols{ display:grid; grid-template-columns:1fr; gap:0 30px }
@media(min-width:760px){ .index-cols{ grid-template-columns:repeat(3,1fr) } }
.index-list .grp{ margin-bottom:22px }
.index-list h3{ font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.14em;
  text-transform:uppercase; margin:0 0 8px; font-weight:500 }
.index-list ul{ margin:0; padding:0; list-style:none }
.index-list li{ font-size:14px; line-height:1.45; padding:6px 0; border-top:1px solid #2A1C40; color:#CFC4E2 }
.index-list li em{ font-style:normal; color:var(--dim); font-size:12px; display:block }
@media (prefers-reduced-motion: reduce){ .star-name{ transition:none } }
</style>
</head>
<body class="sky-page">

<div class="topbar"></div>
<div class="shell">

  <nav class="nav">
    <a class="brand" href="/">Home</a>
    <div class="navlinks">
      <a href="/research/">Research</a>
      <a href="/universe/" aria-current="page">Universe</a>
      <a href="/publications/">Publications</a>
      <a href="/teaching/">Teaching</a>
      <a href="/join/" class="is-cta">Work with me</a>
    </div>
  </nav>

  <div class="sky-head">
    <div><h1>How the work<br>connects</h1></div>
    <p id="head-copy">Two axes. Across: <b>what kind of AI</b> the study is about. Down: whether it <b>intervenes</b> &mdash; building something that makes people better at the work &mdash; or <b>observes</b> what AI set off once it arrived. Click an axis to fall into it; click a star to go to the study.</p>
    <div class="hint" style="border:0;padding:0">
      <div class="viewtoggle" role="group" aria-label="Choose an arrangement">
        <button type="button" id="v-axis" aria-pressed="true">Two axes</button>
        <button type="button" id="v-cite" aria-pressed="false">Citation sky</button>
      </div>
    </div>
  </div>

  <div class="sky mode-axis" id="sky">
    <div class="sky-world" id="world">
      <div class="axis-layer" id="axis-layer">
        <canvas id="neb" width="__CW__" height="__CH__"></canvas>
        <svg class="links" viewBox="0 0 __W__ __H__" id="links" aria-hidden="true"></svg>
      </div>
      <div class="cite-layer" id="cite-layer">
        <canvas id="dust" width="__CW__" height="__CH__"></canvas>
        <svg class="links cite-links" viewBox="0 0 __W__ __H__" id="clinks" aria-hidden="true"></svg>
      </div>
    </div>
    <div class="tip" id="tip" role="status" aria-live="polite"></div>
    <div class="legend" id="legend"></div>
    <div class="sky-ctrl">
      <button type="button" id="btn-out">Zoom out</button>
      <button type="button" id="btn-reset">Whole sky</button>
    </div>
  </div>

  <p class="blurb" id="blurb-axis">Where I file each study. The constellations are real ones &mdash; Ursa Major, Cassiopeia, Orion, Lyra, Corvus, Crux &mdash; and the grey points are the places still open in each cell.</p>
  <p class="blurb is-off" id="blurb-cite">Where the literature files them. Every faint star is a work one of these studies cites; the bright ones are the studies. <b>No position here is chosen by hand</b> &mdash; a force simulation runs over the real citation graph, so two studies sit close together only when they draw on the same references, and a work several papers lean on is pulled into the space between them. <b>__N_CITED__</b> works cited, <b>__N_SHARED__</b> of them by two or more studies.</p>

  <section class="index-list">
    <h2>Everything on the map, in plain text</h2>
    <p>Grouped by what kind of AI each study is about. Works without JavaScript, and reads correctly to a screen reader.</p>
    <div class="index-cols" id="fallback"></div>
  </section>

</div>

<script>
(function(){
  "use strict";
  var COLS = __COLS__;
  var ROWS = __ROWS__;
  var STARS = __STARS__;
  var SLOTS = __SLOTS__;
  var LINKS = __LINKS__;
  var WORKS = __WORKS__;
  var CLINKS = __CLINKS__;

  var world=document.getElementById('world'), sky=document.getElementById('sky');
  var axisLayer=document.getElementById('axis-layer'), citeLayer=document.getElementById('cite-layer');
  var tip=document.getElementById('tip');
  var W=__W__, H=__H__, DPR=__DPR__;
  var mode='axis';

  var COPY_AXIS = document.getElementById('head-copy').innerHTML;
  var COPY_CITE = 'Where the literature puts them. Across: nothing &mdash; there are no axes here. '
    + 'Two studies are close together <b>only because they cite the same work</b>, and every faint '
    + 'star is one of those works. Hover a faint star to see what it is; click a bright one to go '
    + 'to the study.';
  var colById={}, rowById={};
  COLS.forEach(function(c){ colById[c.id]=c; });
  ROWS.forEach(function(r){ rowById[r.id]=r; });

  /* ---- sky: one soft cloud per AI kind, plus faint band separators ---- */
  (function paintSky(){
    var cv=document.getElementById('neb'), ctx=cv.getContext('2d');
    ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
    var seed=20260909;
    function rnd(){ seed=(seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; }
    for (var i=0;i<1500;i++){
      ctx.globalAlpha=0.14+rnd()*0.4;
      ctx.fillStyle= rnd()>0.86 ? '#C9B8F0' : '#FFFFFF';
      ctx.beginPath(); ctx.arc(rnd()*W, rnd()*H, rnd()*0.9+0.25, 0, Math.PI*2); ctx.fill();
    }
    ctx.globalAlpha=1;
    function hexA(hex,a){ var n=parseInt(hex.slice(1),16);
      return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')'; }
    COLS.forEach(function(c){
      ROWS.forEach(function(r){
        var g=ctx.createRadialGradient(c.x,r.y,6,c.x,r.y,192);
        g.addColorStop(0,hexA(c.c,0.15)); g.addColorStop(0.5,hexA(c.c,0.055)); g.addColorStop(1,hexA(c.c,0));
        ctx.fillStyle=g; ctx.beginPath(); ctx.arc(c.x,r.y,192,0,Math.PI*2); ctx.fill();
      });
    });
    ctx.strokeStyle='rgba(255,255,255,.07)'; ctx.lineWidth=1;
    ROWS.forEach(function(r,i){
      if(!i) return;
      var y=(ROWS[i-1].y+r.y)/2;
      ctx.beginPath(); ctx.moveTo(48,y); ctx.lineTo(W-48,y); ctx.stroke();
    });
    COLS.forEach(function(c,i){
      if(!i) return;
      var x=(COLS[i-1].x+c.x)/2;
      ctx.beginPath(); ctx.moveTo(x,83); ctx.lineTo(x,H-64); ctx.stroke();
    });
  })();

  /* ---- constellation lines: lit where two projects meet, faint elsewhere ---- */
  (function drawLinks(){
    var frag='';
    LINKS.forEach(function(l){
      frag += '<line x1="'+l.x1+'" y1="'+l.y1+'" x2="'+l.x2+'" y2="'+l.y2+
              '" stroke="'+(l.lit ? l.c : '#7E6CA0')+
              '" stroke-opacity="'+(l.lit ? '.45' : '.15')+
              '" stroke-width="1" vector-effect="non-scaling-stroke"/>';
    });
    document.getElementById('links').innerHTML = frag;
  })();

  /* ---- the citation sky: dust, the works cited, the coupling between studies ---- */
  (function paintDust(){
    var cv=document.getElementById('dust'), ctx=cv.getContext('2d');
    ctx.setTransform(DPR,0,0,DPR,0,0); ctx.clearRect(0,0,W,H);
    var s=1337;
    function rnd(){ s=(s*1664525+1013904223)%4294967296; return s/4294967296; }
    for (var i=0;i<2100;i++){
      ctx.globalAlpha=0.05+rnd()*0.26;
      ctx.fillStyle='#CFC2E8';
      ctx.beginPath(); ctx.arc(rnd()*W, rnd()*H, rnd()*0.85+0.22, 0, Math.PI*2); ctx.fill();
    }
  })();

  (function drawCoupling(){
    var frag='';
    CLINKS.forEach(function(l){
      frag += '<line x1="'+l.x1+'" y1="'+l.y1+'" x2="'+l.x2+'" y2="'+l.y2+
              '" stroke-width="'+(0.5+l.n*0.4).toFixed(2)+
              '" stroke-opacity="'+Math.min(0.10+l.n*0.075,0.46).toFixed(3)+
              '" vector-effect="non-scaling-stroke"/>';
    });
    document.getElementById('clinks').innerHTML=frag;
  })();

  var WSIZE={1:3.0,2:5.0,3:6.6,4:7.8};
  (function drawWorks(){
    var frag=document.createDocumentFragment();
    WORKS.forEach(function(w,i){
      var d=document.createElement('div'), px=WSIZE[w.d]||8;
      d.className='w';
      d.style.left=w.x+'px'; d.style.top=w.y+'px';
      d.style.width=px+'px'; d.style.height=px+'px';
      d.style.background=w.c;
      d.style.opacity = w.d>1 ? 0.95 : 0.5;
      if (w.d>1) d.style.boxShadow='0 0 '+(w.d*4)+'px '+w.c;
      d.dataset.i=i;
      frag.appendChild(d);
    });
    citeLayer.appendChild(frag);
  })();

  /* ---- axis handles ---- */
  COLS.forEach(function(c){
    var b=document.createElement('button');
    b.type='button'; b.className='axis axis--col';
    b.style.left=c.x+'px'; b.style.top='22px';
    b.innerHTML='<span class="axis-in">'+c.name+'<i>'+c.sub+'</i></span>';
    b.addEventListener('click', function(e){ e.stopPropagation(); flyTo(c.x, H/2, 1.55); });
    axisLayer.appendChild(b);
  });
  ROWS.forEach(function(r){
    var b=document.createElement('button');
    b.type='button'; b.className='axis axis--row';
    b.style.left='13px'; b.style.top=r.y+'px';
    b.innerHTML='<span class="axis-in">'+r.name+'<i>'+r.sub+'</i></span>';
    b.addEventListener('click', function(e){ e.stopPropagation(); flyTo(W/2, r.y, 1.55); });
    axisLayer.appendChild(b);
  });

  /* ---- stars ---- */
  var STAR_PATH = '<svg class="star-dot" viewBox="0 0 100 100" aria-hidden="true">'
    + '<path d="M50 2 C54 31 69 46 98 50 C69 54 54 69 50 98 C46 69 31 54 2 50 C31 46 46 31 50 2 Z"/></svg>';

  STARS.forEach(function(st){
    var size = st.s===3 ? 34 : st.s===2 ? 26 : 19;
    var a=document.createElement('a');
    a.className='star'; a.href=st.href;
    a.style.setProperty('--c', st.c); a.style.setProperty('--sz', size+'px');
    a.setAttribute('aria-label', st.t.replace(/&[a-z]+;/g,' ') + ' \u2014 ' + st.v.replace(/&[a-z]+;/g,' '));
    a.innerHTML = STAR_PATH + '<span class="star-name">'+st.t+'</span>';
    a.dataset.star='1';
    world.appendChild(a);
    st.el=a; st.lbl=a.querySelector('.star-name');
  });

  // the room the sky still has
  SLOTS.forEach(function(sl){
    var d=document.createElement('span');
    d.className='slot'; d.setAttribute('aria-hidden','true');
    d.style.left=sl.x+'px'; d.style.top=sl.y+'px';
    d.innerHTML=STAR_PATH;
    axisLayer.appendChild(d);
  });

  /* ---- switching arrangement -------------------------------------------
     Same stars, two sets of coordinates. A study with no reference list yet
     has no place in the citation sky, and a study off the two AI axes has no
     cell \u2014 either way it fades rather than jumping to the origin.          */
  function position(){
    var cite = (mode==='cite');
    STARS.forEach(function(st){
      var x = cite ? st.cx : st.ax, y = cite ? st.cy : st.ay;
      var here = (x!=null && y!=null);
      st.el.classList.toggle('absent', !here);
      if (here){
        st.el.style.setProperty('--x', x+'px');
        st.el.style.setProperty('--y', y+'px');
        st.lbl.textContent = cite ? st.lab : st.t;
      }
    });
  }

  function setMode(m){
    if (m===mode) return;
    mode=m;
    sky.classList.toggle('mode-cite', m==='cite');
    sky.classList.toggle('mode-axis', m==='axis');
    document.getElementById('v-axis').setAttribute('aria-pressed', String(m==='axis'));
    document.getElementById('v-cite').setAttribute('aria-pressed', String(m==='cite'));
    document.getElementById('blurb-axis').classList.toggle('is-off', m!=='axis');
    document.getElementById('blurb-cite').classList.toggle('is-off', m!=='cite');
    document.getElementById('head-copy').innerHTML = (m==='cite') ? COPY_CITE : COPY_AXIS;
    if (m!=='cite') STARS.forEach(function(st){ st.lbl.style.transform=''; st.lbl.className='star-name'; });
    hideTip();
    position();
    measureLabels();
    // the arrangement moves for most of a second; keep the labels honest as it does
    var t0=Date.now();
    (function follow(){ placeLabels(); if (Date.now()-t0 < 1100) requestAnimationFrame(follow); })();
  }
  document.getElementById('v-axis').addEventListener('click', function(){ setMode('axis'); });
  document.getElementById('v-cite').addEventListener('click', function(){ setMode('cite'); });

  /* ---- label placement, citation view only -----------------------------
     A label's size on screen is fixed while the gap between two stars is not,
     so where a name fits depends on the zoom. Solve it each frame instead of
     baking positions in. STARS is ordered by how much literature a study
     carries, so the big ones keep their names when the sky is tight.      */
  var PAD=4, HALF=13, GAP=20;
  function measureLabels(){
    STARS.forEach(function(st){
      st.lbl.style.transform='';                  // measure the natural box
      st.lbl.className='star-name';
      var r=st.lbl.getBoundingClientRect();
      if (r.width){ st.lw=r.width; st.lh=r.height; }
    });
  }
  function overlap(a,b){
    return !(a.x+a.w+PAD<b.x || b.x+b.w+PAD<a.x || a.y+a.h+PAD<b.y || b.y+b.h+PAD<a.y);
  }
  function placeLabels(){
    if (mode!=='cite') return;
    var r=sky.getBoundingClientRect();
    var ox=r.width/2-cam.x*cam.s, oy=r.height/2-cam.y*cam.s;
    var live=STARS.filter(function(st){ return st.cx!=null && st.lw; });
    var taken=live.map(function(st){
      return { x:ox+st.cx*cam.s-HALF, y:oy+st.cy*cam.s-HALF, w:HALF*2, h:HALF*2, own:st.id };
    });
    live.forEach(function(st){
      var sx=ox+st.cx*cam.s, sy=oy+st.cy*cam.s, w=st.lw, h=st.lh;
      var D=GAP*0.72;
      var cands=[[sx-w/2,sy+GAP],[sx-w/2,sy-GAP-h],[sx+GAP,sy-h/2],[sx-GAP-w,sy-h/2],
                 [sx+D,sy+D],[sx-D-w,sy+D],[sx+D,sy-D-h],[sx-D-w,sy-D-h]];
      for (var i=0;i<cands.length;i++){
        var box={x:cands[i][0],y:cands[i][1],w:w,h:h}, ok=true;
        for (var j=0;j<taken.length;j++){
          if (taken[j].own===st.id) continue;
          if (overlap(box,taken[j])){ ok=false; break; }
        }
        if (ok){
          st.lbl.className='star-name';
          st.lbl.style.transform='scale(var(--inv,1)) translate('+(box.x-sx).toFixed(1)+'px,'
                                +(box.y-sy).toFixed(1)+'px)';
          taken.push(box); return;
        }
      }
      st.lbl.className='star-name no-room';
    });
  }

  /* ---- tooltip for the works cited ---- */
  function esc(s){ return String(s==null?'':s).replace(/[&<>]/g,function(m){
    return {'&':'&amp;','<':'&lt;','>':'&gt;'}[m]; }); }
  var tipOn=false;
  function hideTip(){ if(tipOn){ tip.classList.remove('on'); tipOn=false; } }
  sky.addEventListener('mousemove', function(e){
    if (mode!=='cite'){ hideTip(); return; }
    var el = e.target.closest ? e.target.closest('.w') : null;
    if (!el){ hideTip(); return; }
    var w=WORKS[+el.dataset.i];
    if (!w) return;
    tip.innerHTML='<div class="tt">'+esc(w.t)+'</div>'
      +'<div class="ta">'+w.a+(w.yr?' &middot; '+w.yr:'')+(w.v?' &middot; '+esc(w.v):'')+'</div>'
      +'<div class="tb">Cited in '+w.by.map(esc).join(' &middot; ')+'</div>';
    tip.classList.add('on'); tipOn=true;
    var r=sky.getBoundingClientRect(), t=tip.getBoundingClientRect();
    var x=e.clientX-r.left+14, y=e.clientY-r.top+14;
    if (x+t.width  > r.width -8) x=e.clientX-r.left-t.width -14;
    if (y+t.height > r.height-8) y=e.clientY-r.top -t.height-14;
    tip.style.left=Math.max(8,x)+'px'; tip.style.top=Math.max(8,y)+'px';
  });
  sky.addEventListener('mouseleave', hideTip);

  document.getElementById('legend').innerHTML = COLS.map(function(c){
    return '<span><b style="background:'+c.c+'"></b>'+c.name+'</span>';
  }).join('');

  /* ---- plain-text index ---- */
  (function(){
    var html='';
    COLS.forEach(function(c){
      var mine=STARS.filter(function(s){ return s.col===c.id; });
      if(!mine.length) return;
      html+='<div class="grp"><h3>'+c.name+'</h3><ul>';
      ROWS.forEach(function(r){
        mine.filter(function(s){ return s.row===r.id; }).forEach(function(s){
          html+='<li>'+s.t+'<em>'+r.name+' &middot; '+s.v+'</em></li>';
        });
      });
      html+='</ul></div>';
    });
    document.getElementById('fallback').innerHTML=html;
  })();

  /* ---- camera ---- */
  var cam={x:W/2,y:H/2,s:1}, tgt={x:W/2,y:H/2,s:1}, raf=null, atFit=true;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fitScale(){ var r=sky.getBoundingClientRect(); return Math.min(r.width/W, r.height/H); }
  function clampCam(c){
    c.s=Math.max(fitScale()*0.92, Math.min(4.2, c.s));
    var r=sky.getBoundingClientRect();
    var hw=r.width/(2*c.s), hh=r.height/(2*c.s);
    c.x = (W*c.s<=r.width)  ? W/2 : Math.max(hw, Math.min(W-hw, c.x));
    c.y = (H*c.s<=r.height) ? H/2 : Math.max(hh, Math.min(H-hh, c.y));
    return c;
  }
  function apply(){
    var r=sky.getBoundingClientRect();
    world.style.transform='translate('+(r.width/2-cam.x*cam.s)+'px,'+(r.height/2-cam.y*cam.s)+'px) scale('+cam.s+')';
    world.style.setProperty('--inv',(1/cam.s).toFixed(4));
    sky.classList.toggle('zoomed', cam.s > fitScale()*1.35);
    placeLabels();
  }
  function snap(){ cam.x=tgt.x; cam.y=tgt.y; cam.s=tgt.s; apply(); }
  function tick(){
    var e=(reduce||document.hidden)?1:0.16, done=true;
    ['x','y','s'].forEach(function(k){
      var d=tgt[k]-cam[k];
      if (Math.abs(d) > (k==='s'?0.0012:0.35)) { cam[k]+=d*e; done=false; } else cam[k]=tgt[k];
    });
    apply(); raf = done ? null : requestAnimationFrame(tick);
  }
  function go(){ if (reduce||document.hidden){ snap(); return; } if(!raf) raf=requestAnimationFrame(tick); }
  function flyTo(x,y,s){ atFit=false; tgt=clampCam({x:x,y:y,s:s}); go(); }
  function reset(){ tgt=clampCam({x:W/2,y:H/2,s:fitScale()}); go(); atFit=true; }

  document.getElementById('btn-reset').addEventListener('click', reset);
  document.getElementById('btn-out').addEventListener('click', function(){
    flyTo(cam.x, cam.y, Math.max(fitScale(), cam.s/1.75));
  });

  sky.addEventListener('wheel', function(e){
    e.preventDefault(); atFit=false;
    var r=sky.getBoundingClientRect();
    var px=(e.clientX-r.left-r.width/2)/cam.s+cam.x, py=(e.clientY-r.top-r.height/2)/cam.s+cam.y;
    var ns=Math.max(fitScale()*0.92, Math.min(4.2, cam.s*(e.deltaY<0?1.14:1/1.14)));
    var k=1-cam.s/ns;
    tgt=clampCam({x:cam.x+(px-cam.x)*k, y:cam.y+(py-cam.y)*k, s:ns}); go();
  }, {passive:false});

  var drag=null;
  sky.addEventListener('pointerdown', function(e){
    if (e.target.closest('.sky-ctrl')) return;
    drag={x:e.clientX,y:e.clientY,cx:cam.x,cy:cam.y,moved:false};
    sky.setPointerCapture(e.pointerId); sky.classList.add('is-drag');
  });
  sky.addEventListener('pointermove', function(e){
    if(!drag) return;
    var dx=e.clientX-drag.x, dy=e.clientY-drag.y;
    if (Math.abs(dx)+Math.abs(dy)>4) drag.moved=true;
    var c=clampCam({x:drag.cx-dx/cam.s, y:drag.cy-dy/cam.s, s:cam.s});
    cam={x:c.x,y:c.y,s:c.s}; tgt={x:c.x,y:c.y,s:c.s}; apply();
  });
  sky.addEventListener('pointerup', function(e){
    // a drag that happens to end over a star must not follow its link
    if (drag && drag.moved && e.target.closest('.star')) e.preventDefault();
    drag=null; sky.classList.remove('is-drag');
  });
  sky.addEventListener('pointercancel', function(){ drag=null; sky.classList.remove('is-drag'); });

  function refit(){
    if (atFit) tgt=clampCam({x:W/2,y:H/2,s:fitScale()});
    else tgt=clampCam({x:tgt.x,y:tgt.y,s:tgt.s});
    go();
  }
  window.addEventListener('resize', refit);
  if (window.ResizeObserver) new ResizeObserver(refit).observe(sky);

  position();
  cam.s=tgt.s=fitScale(); apply();
  measureLabels();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){
    measureLabels(); placeLabels();
  });
})();
</script>
</body>
</html>
'''
# biggest literature first, so those names win when the citation sky gets tight
js_stars.sort(key=lambda s: -(s.get('nref') or 0))

PAGE = (PAGE.replace('__COLS__',   json.dumps(js_cols,   ensure_ascii=False))
            .replace('__ROWS__',   json.dumps(js_rows,   ensure_ascii=False))
            .replace('__STARS__',  json.dumps(js_stars,  ensure_ascii=False))
            .replace('__SLOTS__',  json.dumps(js_slots,  ensure_ascii=False))
            .replace('__LINKS__',  json.dumps(js_links,  ensure_ascii=False))
            .replace('__WORKS__',  json.dumps(js_works,  ensure_ascii=False))
            .replace('__CLINKS__', json.dumps(js_clinks, ensure_ascii=False))
            .replace('__W__', str(W)).replace('__H__', str(H))
            .replace('__CW__', str(int(W * CANVAS))).replace('__CH__', str(int(H * CANVAS)))
            .replace('__DPR__', str(CANVAS))
            .replace('__N_CITED__',  str(N_CITED))
            .replace('__N_SHARED__', str(N_SHARED)))

io.open(os.path.join(R, 'universe/index.html'), 'w', encoding='utf-8').write(PAGE)
print('universe/index.html %d bytes | %d stars (%d in the citation sky), %dx%d cells, '
      '%d works cited, %d shared, %d coupling links'
      % (len(PAGE), len(js_stars), N_CSTUDIES, len(COLS), len(ROWS),
         N_CITED, N_SHARED, len(js_clinks)))
