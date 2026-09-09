# -*- coding: utf-8 -*-
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from projects import PROJECTS, COLS, ROWS
from constellations import CONSTELLATIONS, CELLBOX

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root

COLX = {'llm': 342, 'agentic': 578, 'embodied': 814}
ROWY = {'intervention': 196, 'observational': 452}
SIZE = {'Forthcoming': 3, 'Published': 3, 'Deployed': 3, 'Under review': 2}

js_cols = [dict(id=c['id'], name=c['name'], sub=c['sub'], c=c['c'], x=COLX[c['id']]) for c in COLS]
js_rows = [dict(id=r['id'], name=r['name'], sub=r['sub'], y=ROWY[r['id']]) for r in ROWS]

js_stars, js_slots, js_links = [], [], []
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
            venue = p['chip'] + ((' &middot; ' + p['venue']) if p['venue'] else '')
            js_stars.append(dict(
                x=x, y=y, s=SIZE.get(p['chip'], 1), c=c['c'], col=c['id'], row=r['id'],
                t=p['short'], a=[p['authors']] if p['authors'] else [], v=venue,
                f=p['finding'] or 'A short description of this project is coming.',
                n=p['metrics'], href='/research/#' + p['id']))
        for i, (x, y) in enumerate(pos):
            if i not in filled:
                js_slots.append(dict(x=x, y=y, c=c['c']))
        for i, j in con['links']:
            xi, yi = pos[i]; xj, yj = pos[j]
            js_links.append(dict(x1=xi, y1=yi, x2=xj, y2=yj,
                                 lit=1 if (i in filled and j in filled) else 0, c=c['c']))

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
.sky-world{ position:absolute; top:0; left:0; width:1000px; height:640px;
  transform-origin:0 0; will-change:transform }
.sky-world canvas, .sky-world svg.links{ position:absolute; top:0; left:0;
  width:1000px; height:640px; pointer-events:none }

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

.star{ position:absolute; transform:translate(-50%,-50%); background:none; border:0;
  padding:0; margin:0; cursor:pointer; display:block }
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
    <p>Two axes. Across: <b>what kind of AI</b> the study is about. Down: whether it <b>intervenes</b> &mdash; building something that makes people better at the work &mdash; or <b>observes</b> what AI set off once it arrived. Click an axis to fall into it; click a star to go to the study.</p>
    <p class="hint">Scroll to zoom &middot; drag to pan</p>
  </div>

  <div class="sky" id="sky">
    <div class="sky-world" id="world">
      <canvas id="neb" width="2000" height="1280"></canvas>
      <svg class="links" viewBox="0 0 1000 640" id="links" aria-hidden="true"></svg>
    </div>
    <div class="legend" id="legend"></div>
    <div class="sky-ctrl">
      <button type="button" id="btn-out">Zoom out</button>
      <button type="button" id="btn-reset">Whole sky</button>
    </div>
  </div>

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

  var world=document.getElementById('world'), sky=document.getElementById('sky');
  var W=1000, H=640;
  var colById={}, rowById={};
  COLS.forEach(function(c){ colById[c.id]=c; });
  ROWS.forEach(function(r){ rowById[r.id]=r; });

  /* ---- sky: one soft cloud per AI kind, plus faint band separators ---- */
  (function paintSky(){
    var cv=document.getElementById('neb'), ctx=cv.getContext('2d');
    ctx.setTransform(2,0,0,2,0,0); ctx.clearRect(0,0,W,H);
    var seed=20260909;
    function rnd(){ seed=(seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; }
    for (var i=0;i<640;i++){
      ctx.globalAlpha=0.14+rnd()*0.4;
      ctx.fillStyle= rnd()>0.86 ? '#C9B8F0' : '#FFFFFF';
      ctx.beginPath(); ctx.arc(rnd()*W, rnd()*H, rnd()*0.9+0.25, 0, Math.PI*2); ctx.fill();
    }
    ctx.globalAlpha=1;
    function hexA(hex,a){ var n=parseInt(hex.slice(1),16);
      return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')'; }
    COLS.forEach(function(c){
      ROWS.forEach(function(r){
        var g=ctx.createRadialGradient(c.x,r.y,4,c.x,r.y,120);
        g.addColorStop(0,hexA(c.c,0.15)); g.addColorStop(0.5,hexA(c.c,0.055)); g.addColorStop(1,hexA(c.c,0));
        ctx.fillStyle=g; ctx.beginPath(); ctx.arc(c.x,r.y,120,0,Math.PI*2); ctx.fill();
      });
    });
    ctx.strokeStyle='rgba(255,255,255,.07)'; ctx.lineWidth=1;
    ROWS.forEach(function(r,i){
      if(!i) return;
      var y=(ROWS[i-1].y+r.y)/2;
      ctx.beginPath(); ctx.moveTo(30,y); ctx.lineTo(W-30,y); ctx.stroke();
    });
    COLS.forEach(function(c,i){
      if(!i) return;
      var x=(COLS[i-1].x+c.x)/2;
      ctx.beginPath(); ctx.moveTo(x,52); ctx.lineTo(x,H-40); ctx.stroke();
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

  /* ---- axis handles ---- */
  COLS.forEach(function(c){
    var b=document.createElement('button');
    b.type='button'; b.className='axis axis--col';
    b.style.left=c.x+'px'; b.style.top='14px';
    b.innerHTML='<span class="axis-in">'+c.name+'<i>'+c.sub+'</i></span>';
    b.addEventListener('click', function(e){ e.stopPropagation(); flyTo(c.x, H/2, 1.55); });
    world.appendChild(b);
  });
  ROWS.forEach(function(r){
    var b=document.createElement('button');
    b.type='button'; b.className='axis axis--row';
    b.style.left='8px'; b.style.top=r.y+'px';
    b.innerHTML='<span class="axis-in">'+r.name+'<i>'+r.sub+'</i></span>';
    b.addEventListener('click', function(e){ e.stopPropagation(); flyTo(W/2, r.y, 1.55); });
    world.appendChild(b);
  });

  /* ---- stars ---- */
  var STAR_PATH = '<svg class="star-dot" viewBox="0 0 100 100" aria-hidden="true">'
    + '<path d="M50 2 C54 31 69 46 98 50 C69 54 54 69 50 98 C46 69 31 54 2 50 C31 46 46 31 50 2 Z"/></svg>';

  STARS.forEach(function(st){
    var size = st.s===3 ? 34 : st.s===2 ? 26 : 19;
    var a=document.createElement('a');
    a.className='star'; a.href=st.href;
    a.style.left=st.x+'px'; a.style.top=st.y+'px';
    a.style.setProperty('--c', st.c); a.style.setProperty('--sz', size+'px');
    a.setAttribute('aria-label', st.t.replace(/&[a-z]+;/g,' ') + ' \u2014 ' + st.v.replace(/&[a-z]+;/g,' '));
    a.innerHTML = STAR_PATH + '<span class="star-name">'+st.t+'</span>';
    world.appendChild(a);
  });

  // the room the sky still has
  SLOTS.forEach(function(sl){
    var d=document.createElement('span');
    d.className='slot'; d.setAttribute('aria-hidden','true');
    d.style.left=sl.x+'px'; d.style.top=sl.y+'px';
    d.innerHTML=STAR_PATH;
    world.appendChild(d);
  });

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

  cam.s=tgt.s=fitScale(); apply();
})();
</script>
</body>
</html>
'''
PAGE = (PAGE.replace('__COLS__',  json.dumps(js_cols,  ensure_ascii=False))
            .replace('__ROWS__',  json.dumps(js_rows,  ensure_ascii=False))
            .replace('__STARS__', json.dumps(js_stars, ensure_ascii=False))
            .replace('__SLOTS__', json.dumps(js_slots, ensure_ascii=False))
            .replace('__LINKS__', json.dumps(js_links, ensure_ascii=False)))

io.open(os.path.join(R, 'universe/index.html'), 'w', encoding='utf-8').write(PAGE)
print('universe/index.html', len(PAGE), 'bytes,', len(js_stars), 'stars,', len(COLS), 'x', len(ROWS), 'cells')
