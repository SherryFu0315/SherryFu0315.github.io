# -*- coding: utf-8 -*-
"""
Builds /sky/ — the citation sky.

Every faint star is a work one of Xinyu Fu's studies cites. Every bright star is a
study. Nothing is hand-placed: positions come from a force simulation over the real
citation graph, so two studies sit close together because they actually draw on the
same literature, and a cited work sits between the studies that cite it.

    python3 build_citesky.py
"""
import io, os, sys, json, math, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projects import PROJECTS, COLS
import citelayout as CL

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(HERE)

NEUTRAL = '#8E7FA8'
CBY = {c['id']: c['c'] for c in COLS}

works = json.load(open(os.path.join(HERE, 'works.json'), encoding='utf8'))
have = set(c for w in works for c in w['cited_by'])
studies = [p for p in PROJECTS if p['id'] in have]
byid = {p['id']: p for p in studies}

sxy, wxy, works, (WBOX, HBOX) = CL.layout(studies, works)
pairs = CL.coupling(studies, works)

# Short enough to sit under a star without colliding with its neighbours. The full
# title still shows in the tooltip and in the aria-label.
LABEL = {
    'retrieval':     'LLM oversight',
    'errors':        'Detecting AI errors',
    'secd':          'Epistemic calibration',
    'creativity':    'AI authenticity',
    'investment':    'Investment expectations',
    'stimulus':      'Stimulus sampling',
    'sales':         'Parallel AI in sales',
    'triage':        'AI triage',
    'manufacturing': 'Shop-floor embodied AI',
    'service':       'Service robots',
    'misaligned':    'Social signals',
    'remote':        'Remote work',
}

# ---------------------------------------------------------------- stars
js_stars = []
for p in studies:
    x, y = sxy[p['id']]
    c = CBY.get(p['col']) or NEUTRAL
    deg = sum(1 for w in works if p['id'] in w['cited_by'])
    js_stars.append(dict(
        id=p['id'], x=x, y=y, c=c,
        t=LABEL.get(p['id'], p['short']), full=p['title'],
        v=p['chip'] + ((' · ' + p['venue']) if p['venue'] else ''),
        n=deg, href='/research/#' + p['id']))
js_stars.sort(key=lambda s: -s['n'])          # label priority: most-cited first

# ---------------------------------------------------------------- cited works
js_works = []
for w in works:
    x, y = wxy[w['key']]
    cs = [c for c in w['cited_by'] if c in byid]
    if len(cs) == 1:
        col = CBY.get(byid[cs[0]]['col']) or NEUTRAL
    else:
        col = '#FFF4D6'                       # shared works burn white-gold
    au = w['authors'][0] if w['authors'] else ''
    if len(w['authors']) == 2:
        au += ' & ' + w['authors'][1]
    elif len(w['authors']) > 2:
        au += ' et al.'
    js_works.append(dict(
        x=x, y=y, d=len(cs), c=col,
        t=w['title'], a=au, y2=w['year'], v=w['venue'],
        by=[byid[c]['short'] for c in cs]))

# ---------------------------------------------------------------- coupling links
js_links = []
for (a, b), n in sorted(pairs.items(), key=lambda kv: kv[1]):
    if a not in sxy or b not in sxy:
        continue
    x1, y1 = sxy[a]; x2, y2 = sxy[b]
    js_links.append(dict(x1=x1, y1=y1, x2=x2, y2=y2, n=n,
                         a=byid[a]['short'], b=byid[b]['short']))

N_WORKS = len(js_works)
N_SHARED = sum(1 for w in js_works if w['d'] > 1)
N_STUDIES = len(js_stars)

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500'
         '&display=swap">')

PAGE = u'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Citation Sky &mdash; Xinyu Fu</title>
<meta name="description" content="Every study Xinyu Fu cites, drawn as a star. Her own work sits where the literature actually puts it: two studies are close together because they draw on the same references.">
__FONTS__
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/site.js" defer></script>
<link rel="icon" href="/profile.png">
<style>
.sky-page{ --void:#100A1C; --dim:#9A8CB4; background:var(--void); color:#EFEAF6 }
.sky-page .topbar{ background:var(--void) }
.sky-page .nav{ border-bottom-color:#33254A }
.sky-page .brand{ color:#EFEAF6 }
.sky-page .navlinks a{ color:var(--dim) }
.sky-page .navlinks a:hover,.sky-page .navlinks a[aria-current]{ color:#fff }
.sky-page .navlinks a.is-cta{ background:#DCFF96; color:#1E102F }

.sky-head{ display:grid; grid-template-columns:minmax(220px,1fr) minmax(0,2fr) auto;
  gap:26px; align-items:start; padding:26px var(--pad) 20px; border-bottom:1px solid #33254A }
.sky-head h1{ font-family:Archivo,system-ui,sans-serif; font-variation-settings:'wdth' 78,'wght' 900;
  font-size:clamp(26px,3.4vw,44px); line-height:.92; margin:0; text-transform:uppercase; letter-spacing:-.01em }
.sky-lede{ margin:0; font-size:15px; line-height:1.5; color:#C9BEDD; max-width:62ch }
.sky-lede b{ color:#fff; font-weight:600 }
.sky-meta{ font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.07em;
  text-transform:uppercase; color:var(--dim); text-align:right; line-height:1.85; margin:0;
  min-width:15ch }
.sky-meta b{ color:#DCFF96; font-weight:500 }

.sky{ position:relative; height:min(74vh,780px); min-height:440px; overflow:hidden;
  border-bottom:1px solid #33254A;
  background:
    radial-gradient(1100px 620px at 46% 40%, rgba(96,68,150,.30), transparent 66%),
    radial-gradient(760px 520px at 78% 72%, rgba(150,64,110,.16), transparent 70%),
    var(--void);
  cursor:grab; touch-action:none }
.sky.is-drag{ cursor:grabbing }
.sky-world{ position:absolute; left:0; top:0; width:__W__px; height:__H__px;
  transform-origin:0 0; will-change:transform }

.dust{ position:absolute; inset:0; pointer-events:none }
.links{ position:absolute; left:0; top:0; width:100%; height:100%; overflow:visible; pointer-events:none }
.links line{ stroke:#C9B6FF; stroke-linecap:round }

.w{ position:absolute; border-radius:50%; transform:translate(-50%,-50%) scale(var(--inv,1));
  transform-origin:50% 50%; cursor:crosshair }
.w:hover{ filter:brightness(1.9) }

.star{ position:absolute; transform:translate(-50%,-50%); text-decoration:none; color:inherit }
.star-dot{ display:block; width:38px; height:38px; margin:-19px 0 0 -19px;
  transform:scale(var(--inv,1)); transform-origin:50% 50%; transition:transform .18s ease }
/* Four candidate placements; JS picks the first that does not collide on screen. */
.star-name{ position:absolute; left:50%; top:0; white-space:nowrap;
  transform:translate(-50%,0) scale(var(--inv,1)) translate(0,20px); transform-origin:50% 0;
  font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.10em;
  text-transform:uppercase; color:#EFEAF6; text-shadow:0 1px 10px #100A1C,0 0 22px #100A1C }
.star-name.at-top{ transform:translate(-50%,-100%) scale(var(--inv,1)) translate(0,-20px);
  transform-origin:50% 100% }
.star-name.at-right{ transform:translate(0,-50%) scale(var(--inv,1)) translate(20px,0);
  transform-origin:0 50% }
.star-name.at-left{ transform:translate(-100%,-50%) scale(var(--inv,1)) translate(-20px,0);
  transform-origin:100% 50% }
.star-name.hidden{ opacity:0 }
.star:hover .star-name{ opacity:1; z-index:3 }
.star:hover .star-dot{ transform:scale(calc(var(--inv,1) * 1.35)) rotate(12deg) }
.star:focus-visible{ outline:2px solid #DCFF96; outline-offset:6px; border-radius:4px }

.tip{ position:absolute; z-index:5; max-width:330px; padding:11px 13px;
  background:rgba(24,15,40,.97); border:1px solid #4A3968; border-radius:3px;
  box-shadow:0 14px 40px rgba(0,0,0,.6); pointer-events:none; opacity:0;
  transition:opacity .12s ease }
.tip.on{ opacity:1 }
.tip .tt{ font-size:13.5px; line-height:1.36; color:#F4EFFA }
.tip .ta{ margin-top:5px; font-family:'IBM Plex Mono',monospace; font-size:10.5px;
  letter-spacing:.06em; color:#A697C0 }
.tip .tb{ margin-top:7px; padding-top:7px; border-top:1px solid #3A2B55;
  font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:.08em;
  text-transform:uppercase; color:#DCFF96 }

.sky-ctl{ position:absolute; right:16px; bottom:16px; display:flex; gap:8px; z-index:4 }
.sky-ctl button{ font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.09em;
  text-transform:uppercase; color:var(--dim); background:rgba(24,15,40,.86);
  border:1px solid #4A3968; border-radius:2px; padding:7px 11px; cursor:pointer }
.sky-ctl button:hover{ color:#fff; border-color:#7A63A8 }
.sky-hint{ position:absolute; left:16px; bottom:16px; z-index:4;
  font-family:'IBM Plex Mono',monospace; font-size:10.5px; letter-spacing:.09em;
  text-transform:uppercase; color:#7A6C94; pointer-events:none }

.legend{ display:flex; flex-wrap:wrap; gap:22px 26px; padding:16px var(--pad) 6px;
  font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.07em;
  text-transform:uppercase; color:var(--dim); align-items:center }
.legend span{ display:flex; align-items:center; gap:8px }
.legend i{ display:inline-block; border-radius:50% }

.sky-note{ padding:20px var(--pad) 44px; font-size:14.5px; line-height:1.6; color:#B7AACD; max-width:74ch }
.sky-note a{ color:#DCFF96 }
.sky-note h2{ font-family:Archivo,system-ui,sans-serif; font-variation-settings:'wdth' 82,'wght' 800;
  font-size:15px; letter-spacing:.02em; text-transform:uppercase; color:#EFEAF6; margin:0 0 8px }

@media(max-width:860px){
  .sky-head{ grid-template-columns:1fr; gap:12px }
  .sky-meta{ text-align:left }
  .sky{ height:64vh }
}
@media(prefers-reduced-motion:reduce){ .star-dot{ transition:none } }
</style>
</head>
<body class="sky-page">

<div class="topbar"></div>
<div class="shell">

  <nav class="nav">
    <a class="brand" href="/">Home</a>
    <div class="navlinks">
      <a href="/research/">Research</a>
      <a href="/universe/">Universe</a>
      <a href="/sky/" aria-current="page">Citation sky</a>
      <a href="/publications/">Publications</a>
      <a href="/teaching/">Teaching</a>
      <a href="/join/" class="is-cta">Work with me</a>
    </div>
  </nav>

  <div class="sky-head">
    <h1>Where the<br>work sits</h1>
    <p class="sky-lede">Every faint star is a paper one of my studies cites. Every bright star is
    one of my studies. <b>Nothing here is placed by hand.</b> The positions come from a force
    simulation over the real citation graph, so two of my studies are close together only because
    they draw on the same literature &mdash; and a reference that several of my papers lean on is
    pulled into the space between them.</p>
    <p class="sky-meta">
      <b>__NSTUDIES__</b> studies<br>
      <b>__NWORKS__</b> works cited<br>
      <b>__NSHARED__</b> shared by two or more
    </p>
  </div>

  <div class="sky" id="sky">
    <div class="sky-world" id="world">
      <canvas class="dust" id="dust" width="__W__" height="__H__"></canvas>
      <svg class="links" viewBox="0 0 __W__ __H__" id="links" aria-hidden="true"></svg>
    </div>
    <div class="tip" id="tip" role="status" aria-live="polite"></div>
    <p class="sky-hint">Scroll to zoom &middot; drag to pan</p>
    <div class="sky-ctl">
      <button type="button" id="reset">Reset view</button>
    </div>
  </div>

  <div class="legend">
    <span><i style="width:9px;height:9px;background:#8FA6FF"></i> LLM / MLLM</span>
    <span><i style="width:9px;height:9px;background:#FF7874"></i> Agentic AI</span>
    <span><i style="width:9px;height:9px;background:#ECB8FF"></i> Embodied AI</span>
    <span><i style="width:9px;height:9px;background:#8E7FA8"></i> Off the AI axes</span>
    <span><i style="width:9px;height:9px;background:#FFF4D6"></i> Cited by two or more</span>
  </div>

  <div class="sky-note">
    <h2>How this is built</h2>
    <p>The reference list of each manuscript was parsed into structured records &mdash; author,
    year, title, venue &mdash; and the same work cited in two papers was matched to a single star.
    An edge runs from a study to every work it cites. A spring pulls each study toward its own
    references; every star pushes every other away. Run that to equilibrium and the literature
    arranges itself: the cluster you see is bibliographic coupling, not a drawing.</p>
    <p>Some of it is legible immediately. <em>Detecting AI Errors</em> and the JMIS oversight paper
    share six references and sit closer than any other pair. The real-estate study shares none with
    anything else and drifts off alone with its own halo, which is the honest answer. Studies
    without a finished manuscript &mdash; the book chapter, EduBot, the robotic-surgery work
    &mdash; have no reference list to place them, so they are not in this sky yet.</p>
    <p><a href="/universe/">The other map &rarr;</a> arranges the same studies by what kind of AI
    they are about and whether they intervene or observe.</p>
  </div>

  <footer class="foot">
    <div>
      <h3>Xinyu Fu</h3>
      <p>Department of Computer Information Systems<br>
      J. Mack Robinson College of Business, Georgia State University<br>
      55 Park Place NE, Suite 1727, Atlanta, GA 30303</p>
      <p><a class="mail" data-u="xinyufu" data-d="gsu.edu" href="#">xinyufu [at] gsu.edu</a></p>
    </div>
    <div>
      <h3>Elsewhere</h3>
      <ul>
        <li><a href="https://scholar.google.com/citations?user=0OM4QfkAAAAJ&amp;hl=en">Google Scholar</a></li>
        <li><a href="https://www.linkedin.com/in/xinyu-fu-pitt">LinkedIn</a></li>
      </ul>
    </div>
    <div>
      <h3>Credits</h3>
      <p class="credit">Photography and figure credits: <a href="/credits/">credits</a>.</p>
    </div>
  </footer>

</div>

<script>
(function(){
  var W = __W__, H = __H__;
  var STARS = __STARS__;
  var WORKS = __WORKS__;
  var LINKS = __LINKS__;

  var sky   = document.getElementById('sky');
  var world = document.getElementById('world');
  var svg   = document.getElementById('links');
  var tip   = document.getElementById('tip');
  var reduce = window.matchMedia('(prefers-reduced-motion:reduce)').matches;

  /* ---------- background dust: pure decoration, drawn once ---------- */
  (function dust(){
    var c = document.getElementById('dust'), g = c.getContext('2d');
    var s = 1337;
    function rnd(){ s = (s * 1664525 + 1013904223) % 4294967296; return s / 4294967296; }
    for (var i = 0; i < 1400; i++){
      var x = rnd() * W, y = rnd() * H, r = rnd() * 1.0 + 0.3;
      g.globalAlpha = 0.06 + rnd() * 0.30;
      g.fillStyle = '#CFC2E8';
      g.beginPath(); g.arc(x, y, r, 0, 6.283); g.fill();
    }
  })();

  /* ---------- coupling links between studies ---------- */
  var NS = 'http://www.w3.org/2000/svg';
  LINKS.forEach(function(l){
    var e = document.createElementNS(NS, 'line');
    e.setAttribute('x1', l.x1); e.setAttribute('y1', l.y1);
    e.setAttribute('x2', l.x2); e.setAttribute('y2', l.y2);
    e.setAttribute('stroke-width', (0.55 + l.n * 0.42).toFixed(2));
    e.setAttribute('stroke-opacity', Math.min(0.10 + l.n * 0.075, 0.46).toFixed(3));
    svg.appendChild(e);
  });

  /* ---------- cited works ---------- */
  var SIZE = {1: 3.2, 2: 5.2, 3: 6.8, 4: 8.0};
  var frag = document.createDocumentFragment();
  WORKS.forEach(function(w, i){
    var d = document.createElement('div');
    d.className = 'w';
    var px = SIZE[w.d] || 8;
    d.style.left = w.x + 'px';
    d.style.top  = w.y + 'px';
    d.style.width = px + 'px';
    d.style.height = px + 'px';
    d.style.background = w.c;
    d.style.opacity = w.d > 1 ? 0.95 : 0.52;
    if (w.d > 1) d.style.boxShadow = '0 0 ' + (w.d * 5) + 'px ' + w.c;
    d.dataset.i = i;
    frag.appendChild(d);
  });
  world.appendChild(frag);

  /* ---------- my own studies ---------- */
  var STAR_PATH = '<svg class="star-dot" viewBox="0 0 100 100" aria-hidden="true">'
    + '<path d="M50 2 C54 32 68 46 98 50 C68 54 54 68 50 98 C46 68 32 54 2 50 C32 46 46 32 50 2 Z"'
    + ' fill="CC" /></svg>';
  STARS.forEach(function(st){
    var a = document.createElement('a');
    a.className = 'star';
    a.href = st.href;
    a.style.left = st.x + 'px';
    a.style.top  = st.y + 'px';
    a.style.filter = 'drop-shadow(0 0 12px ' + st.c + ')';
    a.innerHTML = STAR_PATH.replace('CC', st.c) + '<span class="star-name">' + st.t + '</span>';
    a.setAttribute('aria-label', st.full + ' — ' + st.v + ', cites ' + st.n + ' works');
    a.dataset.s = 1;
    a.dataset.t = st.full; a.dataset.v = st.v; a.dataset.n = st.n;
    world.appendChild(a);
    st.el = a; st.lab = a.querySelector('.star-name');
  });

  /* ---------- label placement -----------------------------------------
     Labels are counter-scaled, so their screen size is fixed but the gap
     between two stars is not. Placing them at build time would only be right
     at one zoom level. So: measure once, then on every camera change try four
     positions per star in priority order and drop the ones with nowhere to go.
     STARS is pre-sorted by how many works the study cites, so the biggest
     literatures keep their names when the sky gets crowded.                */
  var PAD = 4, HALF = 19, GAP = 20;             // GAP must match the CSS offsets
  STARS.forEach(function(st){
    var r = st.lab.getBoundingClientRect();     // constant in screen px
    st.lw = r.width; st.lh = r.height;
  });
  function hit(a, b){
    return !(a.x + a.w + PAD < b.x || b.x + b.w + PAD < a.x ||
             a.y + a.h + PAD < b.y || b.y + b.h + PAD < a.y);
  }
  function placeLabels(){
    var taken = [];
    STARS.forEach(function(st){                 // star glyphs are obstacles...
      taken.push({ x: cam.x + st.x * cam.s - HALF, y: cam.y + st.y * cam.s - HALF,
                   w: HALF * 2, h: HALF * 2, own: st.id });
    });
    STARS.forEach(function(st){
      var sx = cam.x + st.x * cam.s, sy = cam.y + st.y * cam.s;
      var w = st.lw, h = st.lh;
      var cands = [
        ['',          sx - w / 2,    sy + GAP],
        ['at-top',    sx - w / 2,    sy - GAP - h],
        ['at-right',  sx + GAP,      sy - h / 2],
        ['at-left',   sx - GAP - w,  sy - h / 2]
      ];
      for (var i = 0; i < cands.length; i++){
        var box = { x: cands[i][1], y: cands[i][2], w: w, h: h }, ok = true;
        for (var j = 0; j < taken.length; j++){
          if (taken[j].own === st.id) continue;  // ...but not your own glyph
          if (hit(box, taken[j])){ ok = false; break; }
        }
        if (ok){
          st.lab.className = 'star-name ' + cands[i][0];
          taken.push(box);
          return;
        }
      }
      st.lab.className = 'star-name hidden';
    });
  }

  /* ---------- tooltip ---------- */
  function esc(s){ return String(s == null ? '' : s).replace(/[&<>]/g, function(m){
    return {'&':'&amp;','<':'&lt;','>':'&gt;'}[m]; }); }
  var tipOn = false;
  function showTip(html, cx, cy){
    tip.innerHTML = html;
    tip.classList.add('on'); tipOn = true;
    var r = sky.getBoundingClientRect(), t = tip.getBoundingClientRect();
    var x = cx - r.left + 14, y = cy - r.top + 14;
    if (x + t.width  > r.width  - 8) x = cx - r.left - t.width  - 14;
    if (y + t.height > r.height - 8) y = cy - r.top  - t.height - 14;
    tip.style.left = Math.max(8, x) + 'px';
    tip.style.top  = Math.max(8, y) + 'px';
  }
  function hideTip(){ if (tipOn){ tip.classList.remove('on'); tipOn = false; } }

  sky.addEventListener('mousemove', function(e){
    var el = e.target.closest ? e.target.closest('.w, .star') : null;
    if (!el){ hideTip(); return; }
    if (el.classList.contains('star')){
      showTip('<div class="tt">' + esc(el.dataset.t) + '</div>'
            + '<div class="ta">' + esc(el.dataset.v) + '</div>'
            + '<div class="tb">Cites ' + esc(el.dataset.n) + ' works · click to open</div>',
            e.clientX, e.clientY);
      return;
    }
    var w = WORKS[+el.dataset.i];
    if (!w) return;
    showTip('<div class="tt">' + esc(w.t) + '</div>'
          + '<div class="ta">' + esc(w.a) + (w.y2 ? ' · ' + w.y2 : '')
          + (w.v ? ' · ' + esc(w.v) : '') + '</div>'
          + '<div class="tb">Cited in ' + w.by.map(esc).join(' · ') + '</div>',
          e.clientX, e.clientY);
  });
  sky.addEventListener('mouseleave', hideTip);

  /* ---------- camera ---------- */
  var cam = { x:0, y:0, s:1 }, want = { x:0, y:0, s:1 }, raf = null;

  function fitScale(){
    var r = sky.getBoundingClientRect();
    return Math.min(r.width / W, r.height / H);
  }
  function home(){
    var s = fitScale(), r = sky.getBoundingClientRect();
    return { s:s, x:(r.width - W * s) / 2, y:(r.height - H * s) / 2 };
  }
  function apply(){
    world.style.transform = 'translate(' + cam.x.toFixed(2) + 'px,' + cam.y.toFixed(2)
      + 'px) scale(' + cam.s.toFixed(4) + ')';
    world.style.setProperty('--inv', (1 / cam.s).toFixed(4));
    if (placeLabels) placeLabels();
  }
  function snap(){ cam.x = want.x; cam.y = want.y; cam.s = want.s; apply(); }
  function tick(){
    var e = (reduce || document.hidden) ? 1 : 0.18, done = true;
    ['x','y','s'].forEach(function(k){
      var d = want[k] - cam[k];
      if (Math.abs(d) > (k === 's' ? 1e-4 : 0.4)){ cam[k] += d * e; done = false; }
      else cam[k] = want[k];
    });
    apply();
    raf = done ? null : requestAnimationFrame(tick);
  }
  function go(){ if (reduce || document.hidden){ snap(); return; } if (!raf) raf = requestAnimationFrame(tick); }

  var MINS, MAXS;
  function refit(){
    var h = home();
    MINS = h.s * 0.85; MAXS = h.s * 9;
    want = h; snap();
  }
  refit();

  sky.addEventListener('wheel', function(e){
    e.preventDefault();
    var r = sky.getBoundingClientRect();
    var mx = e.clientX - r.left, my = e.clientY - r.top;
    var k = Math.exp(-e.deltaY * 0.0016);
    var ns = Math.min(MAXS, Math.max(MINS, want.s * k));
    k = ns / want.s;
    want.x = mx - (mx - want.x) * k;
    want.y = my - (my - want.y) * k;
    want.s = ns;
    go();
  }, { passive:false });

  var drag = null, moved = 0;
  sky.addEventListener('pointerdown', function(e){
    if (e.button !== 0) return;
    drag = { x:e.clientX, y:e.clientY }; moved = 0;
    sky.classList.add('is-drag'); sky.setPointerCapture(e.pointerId);
  });
  sky.addEventListener('pointermove', function(e){
    if (!drag) return;
    var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    moved += Math.abs(dx) + Math.abs(dy);
    want.x += dx; want.y += dy; drag.x = e.clientX; drag.y = e.clientY;
    go();
  });
  function endDrag(e){
    if (!drag) return;
    drag = null; sky.classList.remove('is-drag');
    if (e && e.pointerId != null && sky.hasPointerCapture(e.pointerId)) sky.releasePointerCapture(e.pointerId);
  }
  sky.addEventListener('pointerup', endDrag);
  sky.addEventListener('pointercancel', endDrag);
  sky.addEventListener('click', function(e){ if (moved > 6) e.preventDefault(); }, true);

  /* web fonts change the label widths, so measure again once they land */
  if (document.fonts && document.fonts.ready){
    document.fonts.ready.then(function(){
      STARS.forEach(function(st){
        st.lab.className = 'star-name';
        /* world scales by cam.s, the label counter-scales by 1/cam.s, so the
           rect is already in screen pixels at 1:1 — do not divide again. */
        var r = st.lab.getBoundingClientRect();
        st.lw = r.width; st.lh = r.height;
      });
      placeLabels();
    });
  }

  document.getElementById('reset').addEventListener('click', function(){ want = home(); go(); });
  if (window.ResizeObserver) new ResizeObserver(refit).observe(sky);
  document.addEventListener('visibilitychange', function(){ if (!document.hidden) snap(); });
})();
</script>
</body>
</html>
'''

PAGE = (PAGE.replace('__FONTS__', FONTS)
            .replace('__W__', str(WBOX)).replace('__H__', str(HBOX))
            .replace('__NSTUDIES__', str(N_STUDIES))
            .replace('__NWORKS__', str(N_WORKS))
            .replace('__NSHARED__', str(N_SHARED))
            .replace('__STARS__', json.dumps(js_stars, ensure_ascii=False))
            .replace('__WORKS__', json.dumps(js_works, ensure_ascii=False))
            .replace('__LINKS__', json.dumps(js_links, ensure_ascii=False)))

out = os.path.join(R, 'sky')
if not os.path.isdir(out):
    os.makedirs(out)
io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(PAGE)
print('sky/index.html %d bytes  |  %d studies, %d works (%d shared), %d links, world %dx%d'
      % (len(PAGE), N_STUDIES, N_WORKS, N_SHARED, len(js_links), WBOX, HBOX))
