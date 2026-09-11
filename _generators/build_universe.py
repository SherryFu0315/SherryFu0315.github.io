# -*- coding: utf-8 -*-
"""
The research map. One sky, two arrangements of the same stars:

  "Two axes"     — where I put each study: what kind of AI, and whether it
                   intervenes or observes. Hand-drawn constellations, grey slots
                   for the work still to come.
  "The literature" — where the literature puts them: a force simulation over the
                   real citation graph, surrounded by every work they lean on.

Switching between the two moves the same stars, so you can see a study travel
from the box I filed it under to the company it actually keeps.
"""
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import words as T
from projects import PROJECTS, COLS, ROWS, LABEL, STAR_SIZE
from build import CSS_URL, JS_URL   # the content-hashed asset URLs
from constellations import CONSTELLATIONS, CELLBOX
import citelayout as CL
import deepsky as DS

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
NEUTRAL = '#8E7FA8'
CBY = {c['id']: c['c'] for c in COLS}

js_cols = [dict(id=c['id'], name=c['name'], sub=c['sub'], c=c['c'], x=COLX[c['id']]) for c in COLS]
js_rows = [dict(id=r['id'], name=r['name'], sub=r['sub'], y=ROWY[r['id']]) for r in ROWS]

def star(p, col_c, **kw):
    venue = p['chip'] + ((' &middot; ' + p['venue']) if p['venue'] else '')
    d = dict(id=p['id'], s=STAR_SIZE.get(p['chip'], 1), c=col_c,
             col=p['col'], row=p['row'],
             t=p['short'], lab=LABEL.get(p['id'], p['short']),
             a=[p['authors']] if p['authors'] else [], v=venue,
             f=p['finding'] or T.MAP_FINDING_COMING_SOON,
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

# Where the literature view opens: the median study, not the middle of the
# world. The layout leaves a wide margin around the studies for the outliers
# above and below, and centring on the world centres on that margin.
_cx = sorted(v[0] for v in sxy.values())
_cy = sorted(v[1] for v in sxy.values())
OPEN_AT_CITE = {'x': round(_cx[len(_cx) // 2], 1), 'y': round(_cy[len(_cy) // 2], 1)}

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

# ------------------------------------------------- one step back (deepsky.py)
# None when there is nothing honest to draw; the page is then byte-identical to
# the map without the layer.
DK = DS.build(cworks, sxy, wxy, cpairs, [p['id'] for p in cstudies])
if DK:
    for i, v in DK['dk'].items():
        js_works[i]['dk'] = v                  # js_works is in cworks order
    for st in js_stars:
        if st['id'] in DK['tr']:
            st['tr'] = DK['tr'][st['id']]
    print(DK['log'])

PAGE = u'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__MAP_PAGE_TITLE__</title>
<meta name="description" content="Xinyu Fu's research drawn among the literature it rests on. Every study is placed by the real citation graph rather than by hand, to show how small a part of a field any one body of work is. A second view arranges the same studies by what kind of AI they are about.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="__CSS_URL__">
<script src="__JS_URL__" defer></script>
<link rel="icon" href="/assets/favicon.svg">
<style>
.sky-page{ --void:#120A1F; --dim:#9A8CB4; background:var(--void); color:#EFEAF6 }
.sky-page .nav{ border-bottom-color:#3A2B52 }
.sky-page .brand{ color:#EFEAF6 }
.sky-page .navlinks a{ color:var(--dim) }
.sky-page .navlinks a:hover{ color:#fff; border-color:#6B5A8C }
.sky-page .navlinks a[aria-current="page"]{ background:#EFEAF6; color:var(--void) }

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
  background:none; border:0; padding:0; margin:0; cursor:pointer; display:block }
.star.absent{ opacity:0; pointer-events:none }
/* Stars only travel when you switch view. Without this the first paint would
   fly all fifteen in from the corner, since they start with no --x/--y. */
.sky.ready .star{ transition:transform .9s cubic-bezier(.33,.02,.16,1), opacity .5s ease }
.star-dot{
  display:block; width:var(--sz,20px); height:var(--sz,20px); overflow:visible;
  fill:var(--c,#fff);
  filter:drop-shadow(0 0 4px var(--c,#fff)) drop-shadow(0 0 13px var(--c,#fff));
  transform:scale(var(--inv,1)); transform-origin:50% 50%;
}
/* a point in the constellation with no project on it yet */
.slot{ position:absolute; transform:translate(-50%,-50%); pointer-events:none; display:block }
.slot .star-dot{ width:12px; height:12px; fill:#7E6CA0; opacity:.55; filter:none }
/* Star names live in an overlay that is never scaled. Inside the world they
   were counter-scaled by 1/s, and text drawn through a fractional transform
   renders soft — which is what made them blurry the moment you zoomed. */
.labels{ position:absolute; inset:0; pointer-events:none; z-index:4; overflow:hidden }
.star-name{ position:absolute; left:0; top:0;
  font-family:"IBM Plex Mono",monospace; font-size:12px; letter-spacing:.04em; line-height:1.3;
  color:#EFEAF6; white-space:nowrap; background:rgba(18,10,31,.9); padding:4px 8px;
  opacity:0; pointer-events:none; transition:opacity .18s ease }
.star-name.on{ opacity:1 }
.star-name.measuring{ opacity:0; left:0; top:0 }
.star:hover .star-dot{ transform:scale(calc(var(--inv,1) * 1.8)) rotate(12deg) }
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
.sky.mode-cite .star-name{ background:rgba(18,10,31,.72) }

/* Clicking a star opens this rather than jumping straight to the research page.
   Zoomed in, a name alone does not say what a study is; this does. */
.starcard{ position:absolute; z-index:9; right:16px; top:16px;
  width:min(340px,calc(100% - 32px));
  padding:18px 20px 16px; background:rgba(22,13,38,.985);
  border:1px solid #57427D; border-radius:3px;
  box-shadow:0 22px 60px rgba(0,0,0,.66); opacity:0; visibility:hidden;
  transition:opacity .14s ease }
.starcard.on{ opacity:1; visibility:visible }
.starcard .sc-eyebrow{ font-family:"IBM Plex Mono",monospace; font-size:10px;
  letter-spacing:.13em; text-transform:uppercase; margin:0 0 7px }
.starcard h3{ font-family:"Archivo",Arial,sans-serif; font-variation-settings:"wdth" 90,"wght" 700;
  font-size:19px; line-height:1.14; margin:0 0 8px; color:#fff }
.starcard .sc-auth{ font-size:12.5px; color:#A697C0; margin:0 0 10px; line-height:1.4 }
.starcard .sc-find{ font-size:13.5px; line-height:1.5; color:#D6CCE8; margin:0 0 14px }
.starcard .sc-find b{ color:#fff; font-weight:500 }
.starcard .sc-go{ font-family:"IBM Plex Mono",monospace; font-size:11px;
  letter-spacing:.1em; text-transform:uppercase; color:#DCFF96;
  text-decoration:none; border-bottom:1px solid rgba(220,255,150,.4); padding-bottom:2px }
.starcard .sc-go:hover{ border-bottom-color:#DCFF96 }
.starcard .sc-close{ position:absolute; top:9px; right:10px; width:26px; height:26px;
  background:none; border:0; color:#8E7FA8; font-size:19px; line-height:1; cursor:pointer }
.starcard .sc-close:hover{ color:#fff }

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

.blurb{ padding:0 var(--pad); margin:18px 0 34px; color:var(--dim); font-size:14px;
  line-height:1.65; max-width:78ch }
.blurb p{ margin:0 0 11px }
.blurb p:last-child{ margin-bottom:0 }
.blurb b{ color:#EFEAF6; font-weight:500 }
.blurb a{ color:#DCFF96 }
.blurb h2{ font-family:"Archivo",Arial,sans-serif; font-variation-settings:"wdth" 84,"wght" 800;
  text-transform:uppercase; font-size:14px; letter-spacing:.04em; color:#EFEAF6; margin:0 0 10px }
.blurb.is-off{ display:none }__DEEP_CSS__


@media (prefers-reduced-motion: reduce){ .star-name{ transition:none } }
</style>
</head>
<body class="sky-page">

<div class="topbar"></div>
<div class="shell">

  <nav class="nav">
    <a class="brand" href="/">__MAP_NAV_HOME__</a>
    <div class="navlinks">
      <a href="/research/">__MAP_NAV_RESEARCH__</a>
      <a href="/universe/" aria-current="page">__MAP_NAV_MAP__</a>
      <a href="/publications/">__MAP_NAV_PUBLICATIONS__</a>
      <a href="/teaching/">__MAP_NAV_TEACHING__</a>
      <a href="/join/">__MAP_NAV_MENTORING__</a>
    </div>
  </nav>

  <div class="sky-head">
    <div><h1>__MAP_H1__</h1></div>
    <p id="head-copy">__MAP_HEAD_COPY_CITE__</p>
    <div class="hint" style="border:0;padding:0">
      <div class="viewtoggle" role="group" aria-label="Choose an arrangement">
        <button type="button" id="v-axis" aria-pressed="false">__MAP_VIEW_TOGGLE_AXES__</button>
        <button type="button" id="v-cite" aria-pressed="true">__MAP_VIEW_TOGGLE_LITERATURE__</button>
      </div>
    </div>
  </div>

  <div class="sky mode-cite" id="sky">
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
    <div class="labels" id="labels"></div>
    <div class="tip" id="tip" role="status" aria-live="polite"></div>
    <div class="starcard" id="starcard" role="dialog" aria-label="About this study"></div>
    <div class="legend" id="legend"></div>
    <div class="sky-ctrl">
      <button type="button" id="btn-out">__MAP_BTN_ZOOM_OUT__</button>
      <button type="button" id="btn-reset">__MAP_BTN_WHOLE_SKY__</button>
    </div>
  </div>

  <p class="blurb is-off" id="blurb-axis">__MAP_BLURB_AXIS__</p>
  <div class="blurb" id="blurb-cite">
    <h2>__MAP_METHOD_HEADING__</h2>
    <p>__MAP_BLURB_CITE__</p>
    <p>__MAP_BLURB_CITE_2__</p>__DEEP_BLURB__
    <p>__MAP_BLURB_CITE_3__</p>
  </div>

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
  var mode='cite';

  /* The page opens on the literature, so that is what the template renders and
     what this reads back; the other copy is passed in. */
  var COPY_CITE = document.getElementById('head-copy').innerHTML;
  var COPY_AXIS = __COPY_AXIS__;
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
    a.setAttribute('aria-label', st.t.replace(/&[a-z]+;/g,' ') + ', ' + st.v.replace(/&[a-z]+;/g,' '));
    a.innerHTML = STAR_PATH;
    a.dataset.star='1';
    world.appendChild(a);
    var lb=document.createElement('span');
    lb.className='star-name'; lb.innerHTML=st.t;
    document.getElementById('labels').appendChild(lb);
    st.el=a; st.lbl=lb;
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
    if (atFit){ fitMul=openMul(); tgt=clampCam({x:openAt().x,y:openAt().y,s:fitScale()*fitMul}); go(); }
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
  var PAD=4, HALF=13, GAP=20, hoverId=null;
  function measureLabels(){
    STARS.forEach(function(st){
      st.lbl.classList.add('measuring');
      var r=st.lbl.getBoundingClientRect();
      st.lbl.classList.remove('measuring');
      if (r.width){ st.lw=r.width; st.lh=r.height; }
    });
  }
  function overlap(a,b){
    return !(a.x+a.w+PAD<b.x || b.x+b.w+PAD<a.x || a.y+a.h+PAD<b.y || b.y+b.h+PAD<a.y);
  }
  function placeLabels(){
    var r=sky.getBoundingClientRect();
    var ox=r.width/2-cam.x*cam.s, oy=r.height/2-cam.y*cam.s;
    var cite=(mode==='cite');
    // In the literature view the names are the point, so they stay up. On the
    // two axes they would bury the constellations, so they wait for a zoom or
    // for the pointer, as they always have.
    var showAll = cite || sky.classList.contains('zoomed');
    var live=STARS.filter(function(st){
      var x = cite ? st.cx : st.ax;
      return x!=null && st.lw;
    });
    var taken=live.map(function(st){
      var x = cite ? st.cx : st.ax, y = cite ? st.cy : st.ay;
      return { x:ox+x*cam.s-HALF, y:oy+y*cam.s-HALF, w:HALF*2, h:HALF*2, own:st.id };
    });
    STARS.forEach(function(st){ st.lbl.classList.remove('on'); });
    live.forEach(function(st){
      var wx = cite ? st.cx : st.ax, wy = cite ? st.cy : st.ay;
      var sx=ox+wx*cam.s, sy=oy+wy*cam.s, w=st.lw, h=st.lh;
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
          // whole pixels: a label on a half pixel is a soft label
          st.lbl.style.left=Math.round(box.x)+'px';
          st.lbl.style.top =Math.round(box.y)+'px';
          if (showAll || st.id===hoverId) st.lbl.classList.add('on');
          taken.push(box); return;
        }
      }
      // nowhere to put it — but if the pointer is on that star, show it anyway
      if (st.id===hoverId){
        st.lbl.style.left=Math.round(sx-w/2)+'px';
        st.lbl.style.top =Math.round(sy+GAP)+'px';
        st.lbl.classList.add('on');
      }
    });
  }

  // the label is no longer inside the star, so :hover cannot reach it
  sky.addEventListener('mouseover', function(e){
    var el=e.target.closest ? e.target.closest('.star') : null;
    var st=el && STARS.filter(function(x){ return x.el===el; })[0];
    var id=st?st.id:null;
    if (id!==hoverId){ hoverId=id; placeLabels(); }
  });
  sky.addEventListener('mouseleave', function(){
    if (hoverId){ hoverId=null; placeLabels(); }
  });

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
      +'<div class="tb">Cited in '+w.by.map(esc).join(' &middot; ')+'</div>'__DEEP_TIPLINE__;
    tip.classList.add('on'); tipOn=true;
    var r=sky.getBoundingClientRect(), t=tip.getBoundingClientRect();
    var x=e.clientX-r.left+14, y=e.clientY-r.top+14;
    if (x+t.width  > r.width -8) x=e.clientX-r.left-t.width -14;
    if (y+t.height > r.height-8) y=e.clientY-r.top -t.height-14;
    tip.style.left=Math.max(8,x)+'px'; tip.style.top=Math.max(8,y)+'px';
  });
  sky.addEventListener('mouseleave', hideTip);__DEEP_JS__

  /* ---- clicking one of my own stars opens a card about the study ---- */
  var card = document.getElementById('starcard');
  var cardOpen = false;
  function closeCard(){
    if (!cardOpen) return;
    card.classList.remove('on'); cardOpen = false;
    document.querySelectorAll('.star.is-open').forEach(function(e){ e.classList.remove('is-open'); });
  }
  function openCard(st, el){
    var authors = (st.a && st.a.length) ? st.a.join(', ') : '';
    card.innerHTML =
      '<button type="button" class="sc-close" aria-label="Close">&times;</button>'
      + '<p class="sc-eyebrow" style="color:' + st.c + '">' + st.v + '</p>'   // already entity-encoded
      + '<h3>' + st.t + '</h3>'
      + (authors ? '<p class="sc-auth">' + authors + '</p>' : '')__DEEP_CARD__
      + '<p class="sc-find">' + st.f + '</p>'
      + '<a class="sc-go" href="' + st.href + '">Read the full entry &rarr;</a>';
    card.classList.add('on'); cardOpen = true;
    document.querySelectorAll('.star.is-open').forEach(function(e){ e.classList.remove('is-open'); });
    el.classList.add('is-open');

    card.querySelector('.sc-close').addEventListener('click', closeCard);
  }
  /* Hovering opens the panel. Clicking a 34px star is a poor target, and the
     pan gesture takes pointer capture, which retargets the click away from the
     star anyway — hover has neither problem. A click still follows the link. */
  var closeTimer=null;
  function wantClose(){
    clearTimeout(closeTimer);
    closeTimer=setTimeout(closeCard, 160);      // room to travel from star to panel
  }
  function keepOpen(){ clearTimeout(closeTimer); }

  sky.addEventListener('mouseover', function(e){
    if (!e.target.closest) return;
    if (e.target.closest('.starcard')){ keepOpen(); return; }
    var el = e.target.closest('.star');
    if (!el){ wantClose(); return; }
    var st = STARS.filter(function(x){ return x.el === el; })[0];
    if (!st) return;
    keepOpen();
    openCard(st, el);
  });
  sky.addEventListener('mouseleave', wantClose);

  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeCard(); });

  document.getElementById('legend').innerHTML = COLS.map(function(c){
    return '<span><b style="background:'+c.c+'"></b>'+c.name+'</span>';
  }).join('');


  /* ---- camera ---- */
  var cam={x:W/2,y:H/2,s:1}, tgt={x:W/2,y:H/2,s:1}, raf=null, atFit=true;
  /* The map opens a little inside the whole sky rather than exactly at it.
     Fitted precisely, the frame is wider than the map's 1600x1024 and the
     constellation sits in the middle of two empty margins. WHOLE SKY still
     goes to the true fit, and once it has, a resize keeps it there. */
  /* The literature view opens well inside the whole sky, on the band where the
     studies actually are: fitted whole, most of the frame is the empty margin
     the layout leaves around them, and the labels are too small to read. It
     centres on the studies' median rather than the middle of the world, since
     the outliers above and below are what the margin is made of.

     The two-axis view opens at the true fit and cannot do otherwise — its row
     labels live at the very left edge of the world, and any crop cuts them in
     half. WHOLE SKY goes to the true fit in either view. */
  var OPEN_CITE=2.6, OPEN_AXIS=1.0;
  var OPEN_AT_CITE=__OPEN_AT_CITE__;
  function openMul(){ return mode==='cite' ? OPEN_CITE : OPEN_AXIS; }
  function openAt(){ return mode==='cite' ? OPEN_AT_CITE : {x:W/2,y:H/2}; }
  var fitMul=OPEN_CITE;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fitScale(){
    var r=sky.getBoundingClientRect();
    var s=Math.min(r.width/W, r.height/H);
    // A container measured at zero — hidden parent, prerender, first layout —
    // would otherwise set the camera scale to 0 and the map would draw nothing,
    // with no way back once the pending frame is dropped.
    return (s>0 && isFinite(s)) ? s : 0.5;
  }
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
    __DEEP_APPLY__placeLabels();
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
  function reset(){ fitMul=1; tgt=clampCam({x:W/2,y:H/2,s:fitScale()}); go(); atFit=true; }

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

  var drag=null, lastWasDrag=false, downStar=null;
  sky.addEventListener('pointerdown', function(e){
    // the card is a panel, not part of the sky: let its own links and button work
    if (e.target.closest('.sky-ctrl') || e.target.closest('.starcard')) return;
    downStar = e.target.closest ? e.target.closest('.star') : null;
    drag={x:e.clientX,y:e.clientY,cx:cam.x,cy:cam.y,moved:false};
    sky.setPointerCapture(e.pointerId); sky.classList.add('is-drag');
  });
  sky.addEventListener('pointermove', function(e){
    if(!drag) return;
    var dx=e.clientX-drag.x, dy=e.clientY-drag.y;
    if (Math.abs(dx)+Math.abs(dy)>8) drag.moved=true;   // a click wobbles; a drag does not
    var c=clampCam({x:drag.cx-dx/cam.s, y:drag.cy-dy/cam.s, s:cam.s});
    cam={x:c.x,y:c.y,s:c.s}; tgt={x:c.x,y:c.y,s:c.s}; apply();
  });
  sky.addEventListener('pointerup', function(e){
    // a drag that happens to end over a star must not follow its link
    lastWasDrag = !!(drag && drag.moved);
    if (lastWasDrag && e.target.closest('.star')) e.preventDefault();
    drag=null; sky.classList.remove('is-drag');
  });
  sky.addEventListener('pointercancel', function(){ drag=null; sky.classList.remove('is-drag'); });

  function refit(){
    if (atFit) tgt=clampCam(fitMul===1 ? {x:W/2,y:H/2,s:fitScale()}
                                       : {x:openAt().x,y:openAt().y,s:fitScale()*fitMul});
    else tgt=clampCam({x:tgt.x,y:tgt.y,s:tgt.s});
    if (!(cam.s>0)) { snap(); return; }   // recover from a zero-size first layout
    go();
  }
  window.addEventListener('resize', refit);
  if (window.ResizeObserver) new ResizeObserver(refit).observe(sky);

  position();
  (function openCamera(){
    var c=clampCam({x:openAt().x, y:openAt().y, s:Math.min(4.2, fitScale()*openMul())});
    cam.x=tgt.x=c.x; cam.y=tgt.y=c.y; cam.s=tgt.s=c.s; apply();
  })();
  measureLabels();
  requestAnimationFrame(function(){ requestAnimationFrame(function(){
    sky.classList.add('ready'); placeLabels();
  }); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){
    measureLabels(); placeLabels();
  });
})();
</script>
</body>
</html>
'''
# Label priority when the sky is too tight for every name: published and
# forthcoming work first, then whichever study carries the most literature.
# Sorting by reference count alone let the forthcoming JMIS paper lose its
# label to a working paper that happens to cite more.
js_stars.sort(key=lambda s: (-(s.get('s') or 0), -(s.get('nref') or 0)))

DEEP_CSS_SRC = u'''
.w.via{ filter:brightness(1.9) }
.tip .tb2{ color:#C9B6FF }
.tip .tb + .tb2{ border-top:0; margin-top:3px; padding-top:0 }
.starcard .sc-deep{ font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.05em;
  line-height:1.5; color:#A697C0; margin:-4px 0 12px }'''

DEEP_JS_SRC = u'''
  /* ---- one step back: works that several of my studies reach through the papers they cite.
     Painted once. One path and one fill, so where points crowd they merge instead of
     adding up: crowding here mostly means a list is better traced, not that anything
     is closer. Every point is the same size for the same reason.                      */
  var DEEP=__DEEP__, NAMED=__NAMED__, DW=__DEEP_WORDS__;
  var deepCv=null, deepOp=-1, lit=null, workEls=citeLayer.getElementsByClassName('w');
  // world px. The blur is what makes it read as further back: soft behind crisp.
  var HAZE_R=2.0, HAZE_A=0.50, HAZE_BLUR=2.2;
  (function paintDeep(){
    var b=DEEP.b, p=DEEP.p, box=document.createElement('div'), ctx, i, r;
    box.id='deep'; box.setAttribute('aria-hidden','true');
    box.style.cssText='position:absolute;pointer-events:none;left:'+b[0]+'px;top:'+b[1]+'px;width:'+b[2]+'px;height:'+b[3]+'px';
    function layer(blur){   // an inline box beats '.sky-world canvas', which would stretch it over the world
      var cv=document.createElement('canvas');
      cv.width=Math.ceil(b[2]*DPR); cv.height=Math.ceil(b[3]*DPR);
      cv.style.cssText='left:0;top:0;width:100%;height:100%'+(blur ? ';filter:blur('+blur+'px)' : '');
      box.appendChild(cv);
      var c=cv.getContext('2d'); c.setTransform(DPR,0,0,DPR,0,0); c.fillStyle='#C9B6FF'; return c;
    }
    ctx=layer(HAZE_BLUR); r=HAZE_R; ctx.globalAlpha=HAZE_A; ctx.beginPath();
    for (i=0;i<p.length;i+=2){ ctx.moveTo(p[i]+r,p[i+1]); ctx.arc(p[i],p[i+1],r,0,6.2832); }
    ctx.fill();
    ctx=layer(0); r=1.15; ctx.globalAlpha=0.75; ctx.beginPath();   // the ones you can hover stay sharp
    NAMED.forEach(function(n){ var x=n.x-b[0], y=n.y-b[1]; ctx.moveTo(x+r,y); ctx.arc(x,y,r,0,6.2832); });
    ctx.fill();
    citeLayer.insertBefore(box, document.getElementById('clinks'));  // over the dust, under lines and works
    deepCv=box;
  })();
  function deepFade(){      // fainter as its points grow on screen; stepped, so it rarely repaints
    var o=Math.round(Math.max(0.45, Math.min(1, 1.9/cam.s))*20)/20;
    if (o!==deepOp){ deepOp=o; deepCv.style.opacity=o; }
  }
  function deepLine(k){ return '<div class="tb tb2">'+DW.tip.replace('__K__', k)+'</div>'; }
  function deepCard(st){
    return (mode==='cite' && st.tr)
      ? '<p class="sc-deep">'+DW.card.replace('__DONE__', st.tr[0]).replace('__ALL__', st.tr[1])+'</p>' : '';
  }
  function light(list){     // the papers of mine that lead to it, in the existing hover look
    if (lit===list) return;
    if (lit) lit.forEach(function(j){ workEls[j].classList.remove('via'); });
    lit=list;
    if (lit) lit.forEach(function(j){ workEls[j].classList.add('via'); });
  }
  function onLabel(e){
    return STARS.some(function(st){
      if (!st.lbl.classList.contains('on')) return false;
      var b=st.lbl.getBoundingClientRect();
      return e.clientX>=b.left && e.clientX<=b.right && e.clientY>=b.top && e.clientY<=b.bottom;
    });
  }
  function namedAt(e){
    var r=sky.getBoundingClientRect(), best=null, bd=7/cam.s;            // 7 screen px
    var x=(e.clientX-r.left-r.width/2)/cam.s+cam.x, y=(e.clientY-r.top-r.height/2)/cam.s+cam.y;
    NAMED.forEach(function(n){ var d=Math.hypot(n.x-x, n.y-y); if (d<bd){ bd=d; best=n; } });
    return best;
  }
  sky.addEventListener('mousemove', function(e){
    if (mode!=='cite' || drag || !e.target.closest){ light(null); return; }
    var el=e.target.closest('.w');
    if (el){ var w=WORKS[+el.dataset.i]; light(w && w.dk ? w.dk.w : null); return; }  // its tooltip is already up
    if (e.target.closest('.star,.starcard,.sky-ctrl,.legend') || onLabel(e)){ light(null); return; }
    var n=namedAt(e);
    if (!n){ light(null); return; }                                     // the works handler already hid the tip
    tip.innerHTML='<div class="tt">'+esc(n.t)+'</div>'
      +'<div class="ta">'+n.a+' &middot; '+n.yr+(n.v?' &middot; '+esc(n.v):'')+'</div>'+deepLine(n.k);
    tip.classList.add('on'); tipOn=true; light(n.w);
    var r=sky.getBoundingClientRect(), t=tip.getBoundingClientRect();   // the existing placement rule
    var x=e.clientX-r.left+14, y=e.clientY-r.top+14;
    if (x+t.width  > r.width -8) x=e.clientX-r.left-t.width -14;
    if (y+t.height > r.height-8) y=e.clientY-r.top -t.height-14;
    tip.style.left=Math.max(8,x)+'px'; tip.style.top=Math.max(8,y)+'px';
  });
  sky.addEventListener('mouseleave', function(){ light(null); });
  // switching view from the keyboard never moves the pointer, so clear the lit papers here too
  ['v-axis','v-cite'].forEach(function(id){
    document.getElementById(id).addEventListener('click', function(){ light(null); });
  });'''

DEEP_CSS = DEEP_BLURB = DEEP_TIPLINE = DEEP_CARD = DEEP_APPLY = DEEP_JS = ''
if DK:
    _named = T.MAP_BLURB_DEEP_NAMED_ONE if len(DK['note']) == 1 else T.MAP_BLURB_DEEP_NAMED
    _p2 = ([_named] if DK['note'] else []) + ([T.MAP_BLURB_DEEP_HOVER] if DK['named'] else []) + \
          [T.MAP_BLURB_DEEP_3 if DK['ongoing'] else T.MAP_BLURB_DEEP_3_DONE]
    DEEP_BLURB = '\n    <p>%s</p>\n    <p>%s</p>' % (T.MAP_BLURB_DEEP, ' '.join(_p2))

    def _js(o):     # '</' could close the script tag from inside a title
        return json.dumps(o, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    DEEP_JS = (DEEP_JS_SRC.replace('__DEEP_WORDS__', _js({'tip': T.MAP_TIP_DEEP, 'card': T.MAP_CARD_TRACED}))
                          .replace('__DEEP__', _js(DK['js'])).replace('__NAMED__', _js(DK['named'])))
    DEEP_CSS, DEEP_TIPLINE, DEEP_CARD = DEEP_CSS_SRC, "+(w.dk?deepLine(w.dk.k):'')", '+ deepCard(st)'
    DEEP_APPLY = 'if(deepCv)deepFade();'

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
            # the wording, from words.py. These go in before the counts below,
            # so a count sitting inside a sentence is still filled in.
            .replace('__MAP_PAGE_TITLE__', T.MAP_PAGE_TITLE)
            .replace('__MAP_NAV_HOME__', T.MAP_NAV_HOME)
            .replace('__MAP_NAV_RESEARCH__', T.MAP_NAV_RESEARCH)
            .replace('__CSS_URL__', CSS_URL).replace('__JS_URL__', JS_URL)
            .replace('__MAP_NAV_MAP__', T.MAP_NAV_MAP)
            .replace('__MAP_NAV_PUBLICATIONS__', T.MAP_NAV_PUBLICATIONS)
            .replace('__MAP_NAV_TEACHING__', T.MAP_NAV_TEACHING)
            .replace('__MAP_NAV_MENTORING__', T.MAP_NAV_MENTORING)
            .replace('__MAP_H1__', T.MAP_H1)
            .replace('__MAP_HEAD_COPY_CITE__', T.MAP_HEAD_COPY_CITE)
            .replace('__COPY_AXIS__', json.dumps(T.MAP_HEAD_COPY_AXIS))
            .replace('__OPEN_AT_CITE__', json.dumps(OPEN_AT_CITE))
            .replace('__MAP_VIEW_TOGGLE_AXES__', T.MAP_VIEW_TOGGLE_AXES)
            .replace('__MAP_VIEW_TOGGLE_LITERATURE__', T.MAP_VIEW_TOGGLE_LITERATURE)
            .replace('__MAP_BTN_ZOOM_OUT__', T.MAP_BTN_ZOOM_OUT)
            .replace('__MAP_BTN_WHOLE_SKY__', T.MAP_BTN_WHOLE_SKY)
            .replace('__MAP_BLURB_AXIS__', T.MAP_BLURB_AXIS)
            .replace('__MAP_METHOD_HEADING__', T.MAP_METHOD_HEADING)
            .replace('__MAP_BLURB_CITE_2__', T.MAP_BLURB_CITE_2)
            .replace('__MAP_BLURB_CITE_3__', T.MAP_BLURB_CITE_3)
            .replace('__MAP_BLURB_CITE__', T.MAP_BLURB_CITE)
            .replace('__DEEP_CSS__', DEEP_CSS).replace('__DEEP_BLURB__', DEEP_BLURB)
            .replace('__DEEP_TIPLINE__', DEEP_TIPLINE).replace('__DEEP_CARD__', DEEP_CARD)
            .replace('__DEEP_APPLY__', DEEP_APPLY).replace('__DEEP_JS__', DEEP_JS)
            .replace('__N_CSTUDIES__', str(N_CSTUDIES))
            .replace('__N_CITED__',  str(N_CITED))
            .replace('__N_SHARED__', str(N_SHARED)))

for _k, _v in sorted((DK['tok'] if DK else {}).items(), key=lambda kv: -len(kv[0])):
    PAGE = PAGE.replace(_k, _v)

io.open(os.path.join(R, 'universe/index.html'), 'w', encoding='utf-8').write(PAGE)
print('universe/index.html %d bytes | %d stars (%d in the citation sky), %dx%d cells, '
      '%d works cited, %d shared, %d coupling links'
      % (len(PAGE), len(js_stars), N_CSTUDIES, len(COLS), len(ROWS),
         N_CITED, N_SHARED, len(js_clinks)))
