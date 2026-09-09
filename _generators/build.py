# -*- coding: utf-8 -*-
import io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import words as T
from projects import PROJECTS, COLS, ROWS

# The map card quotes these, and draws a miniature of the real map. Both come
# from the same file and the same layout the map itself uses, so neither the
# figures nor the picture can drift away from it. The layout is deterministic,
# so computing it here gives the identical arrangement.
import citelayout as _CL
_HERE = os.path.dirname(os.path.abspath(__file__))
_works = json.load(io.open(os.path.join(_HERE, 'works.json'), encoding='utf-8'))
N_CITED = len(_works)
N_STUDIES = len(set(c for w in _works for c in w['cited_by']))

_ids = set(c for w in _works for c in w['cited_by'])
_studies = [p for p in PROJECTS if p['id'] in _ids]
_byid = {p['id']: p for p in _studies}
_CBY = {c['id']: c['c'] for c in COLS}
_MW, _MH = 1600, 1024
_sxy, _wxy, _kept, _ = _CL.layout(_studies, _works, box=(_MW, _MH))
_pairs = _CL.coupling(_studies, _kept)

def _n(p):
    return [round(p[0] / _MW, 4), round(p[1] / _MH, 4)]

MINI = {
    'w': [_n(_wxy[w['key']]) + [len([c for c in w['cited_by'] if c in _byid])]
          for w in _kept],
    's': [_n(_sxy[p['id']]) + [_CBY.get(p['col']) or '#8E7FA8'] for p in _studies],
    'l': [_n(_sxy[a]) + _n(_sxy[b]) + [n] for (a, b), n in _pairs.items()],
}

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
 '<link rel="stylesheet" href="/assets/site.css">\n'
 '<script src="/assets/site.js" defer></script>\n'
 '<link rel="icon" href="/profile.png">')

def nav(cur):
    items=[('/research/',T.HOME_NAV_RESEARCH),('/universe/',T.HOME_NAV_UNIVERSE),
           ('/publications/',T.HOME_NAV_PUBLICATIONS),('/teaching/',T.HOME_NAV_TEACHING)]
    out=['  <nav class="nav">','    <a class="brand" href="/">%s</a>' % T.HOME_NAV_HOME,'    <div class="navlinks">']
    for href,label in items:
        out.append('      <a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href==cur else '', label))
    out.append('      <a href="/join/" class="is-cta"%s>%s</a>'
               % (' aria-current="page"' if cur=='/join/' else '', T.HOME_NAV_WORK_WITH_ME))
    out+=['    </div>','  </nav>']
    return '\n'.join(out)

FOOT = '''  <footer class="foot">
    <div>
      <h3>Xinyu Fu</h3>
      <p>%s</p>
      <p><a class="mail" data-u="xinyufu" data-d="gsu.edu" href="#">xinyufu [at] gsu.edu</a></p>
    </div>
    <div>
      <h3>%s</h3>
      <ul>
        <li><a href="https://scholar.google.com/citations?user=0OM4QfkAAAAJ&amp;hl=en">%s</a></li>
        <li><a href="https://www.linkedin.com/in/xinyu-fu-pitt">%s</a></li>
      </ul>
    </div>
    <div>
      <h3>%s</h3>
      <p class="credit">%s</p>
    </div>
  </footer>''' % (T.HOME_FOOT_ADDRESS,
                  T.HOME_FOOT_ELSEWHERE_TITLE,
                  T.HOME_FOOT_GOOGLE_SCHOLAR,
                  T.HOME_FOOT_LINKEDIN,
                  T.HOME_FOOT_CREDITS_TITLE,
                  T.HOME_FOOT_CREDIT_LINE)

colById = {c['id']: c for c in COLS}
NEUTRAL = {'c': '#6B5F7D', 'name': 'Adjacent work'}
def colof(p): return colById.get(p['col'], NEUTRAL)
byCell = {}
for p in PROJECTS:
    byCell.setdefault((p['col'], p['row']), []).append(p)

# ------------------------------------------------------------------ matrix --
def matrix_html():
    out = ['  <div class="matrix">']
    out.append('    <div class="mx-corner"><span>%s</span></div>' % T.RESEARCH_MATRIX_CORNER)
    for c in COLS:
        out.append('    <div class="mx-col" style="--c:%s"><b>%s</b><i>%s</i></div>' % (c['c'], c['name'], c['sub']))
    for r in ROWS:
        out.append('    <div class="mx-row"><b>%s</b><i>%s</i></div>' % (r['name'], r['sub']))
        for c in COLS:
            items = sorted(byCell.get((c['id'], r['id']), []), key=lambda x: x['order'])
            cell = ['    <div class="mx-cell" style="--c:%s">' % c['c']]
            if not items:
                cell.append('      <span class="mx-empty">&mdash;</span>')
            for p in items:
                cell.append('      <a class="mx-item" href="/research/#%s"><span class="mx-t">%s</span>'
                            '<span class="mx-s">%s</span></a>' % (p['id'], p['short'], p['chip']))
            cell.append('    </div>')
            out.append('\n'.join(cell))
    out.append('  </div>')
    return '\n'.join(out)

# ----------------------------------------------------------------- entries --
def entry(p, i=0):
    chips = ['<span class="chip chip--%s">%s</span>' % (
        'live' if p['chip'] in ('Forthcoming', 'Published', 'Deployed') else 'venue', p['chip'])]
    if p['venue']: chips.append('<span class="chip">%s</span>' % p['venue'])
    if p['method']: chips.append('<span class="chip">%s</span>' % p['method'])
    chips.append('<span class="chip chip--kind" style="--c:%s">%s</span>' % (colof(p)['c'], colof(p)['name']))
    m = ''
    if p['metrics']:
        m = '\n      <div class="metrics">%s</div>' % ''.join(
            '<div class="metric"><span class="metric-value">%s</span><span class="metric-label">%s</span></div>'
            % (v, l) for v, l in p['metrics'])
    links = ''
    if p['links']:
        links = '\n      <p class="proj-links">%s</p>' % ' '.join(
            '<a href="%s">%s &rarr;</a>' % (u, t) for t, u in p['links'])
    auth = ('\n      <p class="authors">%s</p>' % p['authors']) if p['authors'] else ''
    ph = ''
    if p.get('photo'):
        ph = ('\n    <div class="entry-art%s"><img src="/assets/img/%s" alt="%s"></div>'
              % (' is-contain' if p.get('fit') == 'contain' else '', p['photo'][0], p['photo'][1]))
    elif p.get('emoji'):
        ph = ('\n    <div class="entry-art is-emoji" aria-hidden="true"><span>%s</span></div>' % p['emoji'])
    find = ('\n      <p class="finding">%s</p>' % p['finding']) if p['finding'] else (
        '\n      <p class="finding is-tbc">%s</p>' % T.RESEARCH_FINDING_COMING_SOON)
    cls = ''
    if p.get('photo') or p.get('emoji'):
        cls = ' has-art' + (' art-left' if i % 2 else '')
    return ('  <article class="entry%s" id="%s" style="--c:%s">\n'
            '    <div class="entry-body">\n'
            '      <div class="chip-row">%s</div>\n'
            '      <h3>%s</h3>%s%s%s%s\n'
            '    </div>%s\n'
            '  </article>' % (cls, p['id'], colof(p)['c'], ''.join(chips), p['title'], auth, find, links, m, ph))

def research_page():
    return '\n\n'.join(entry(x, i) for i, x in enumerate(sorted(PROJECTS, key=lambda y: y['order'])))

RESEARCH = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="Xinyu Fu's research on the design of human-AI collaboration, arranged on two axes: the kind of AI, and whether the study intervenes or observes.">
%s
</head>
<body>

<div class="topbar"></div>
<div class="shell">

%s

  <div class="sec-head">
    <h2>%s</h2>
    <span class="count">%s</span>
  </div>

%s

  <div class="prose" style="border-top:2px solid var(--rule)">
    <p style="font-size:15px;color:var(--muted);max-width:70ch">%s</p>
    <p style="margin-top:22px"><a class="btn" href="/join/">%s</a></p>
  </div>

%s

</div>
</body>
</html>
''' % (T.RESEARCH_PAGE_TITLE,
       FONTS,
       nav('/research/'),
       T.RESEARCH_HEADING,
       T.RESEARCH_COUNT,
       research_page(),
       T.RESEARCH_UNDER_REVIEW_NOTE,
       T.RESEARCH_JOIN_BUTTON,
       FOOT)
io.open(os.path.join(R, 'research/index.html'), 'w', encoding='utf-8').write(RESEARCH)
print('research/index.html', len(RESEARCH), 'bytes')

MOSAIC = [
  ('manufacturing','Manufacturing','manufacturing.jpg','Embodied AI',
   'A robotic arm moving a large sheet of flat glass along a conveyor in a bright glass plant.'),
  ('service','Service','service.jpg','Embodied AI',
   'A hotel guest in a white robe reaching into the open lid of a delivery robot in a carpeted corridor.'),
  ('sales','Sales','sales.jpg','Agentic AI',
   'A humanoid AI head in profile beside a woman wearing a call-centre headset.'),
  ('edubot','Education','edubot.jpg','Agentic AI',
   'Secondary-school students in uniform seated together at the EduBot Naija launch.'),
]
TILE_TPL = (
  '      <a class="tile" href="/research/#%s">\n'
  '        <img src="/assets/img/%s" alt="%s">\n'

  '        <span class="tile-note">%s</span>\n'
  '        <span class="tile-label"><span class="plus">AI+</span><span class="dom">%s</span></span>\n'
  '      </a>')
tiles = [TILE_TPL % (pid, img, alt, note, label) for pid, label, img, note, alt in MOSAIC]

featured = [x for x in sorted(PROJECTS, key=lambda y: y['order']) if x.get('photo') and x['finding']][:6]
home_entries = '\n\n'.join(entry(x, i) for i, x in enumerate(featured))

HOME = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="Xinyu Fu is an Assistant Professor of Computer Information Systems at Georgia State University. She studies how different ways of working with AI shape human performance, the organization of work, and the consequences of AI use.">
%s
</head>
<body>

<div class="topbar"></div>

<div class="shell">

%s

  <header class="hero">
    <div class="rail">
      <div class="rail-top">
        <img class="rail-photo" src="/profile.png" alt="Xinyu Fu">
        <div>
          <h1>Xinyu<br>Fu</h1>
          <p class="role">%s</p>
        </div>
      </div>

      <p class="thesis">%s</p>

    </div>

    <div class="mosaic">
%s
    </div>
  </header>

  <a class="skylink" href="/universe/">
    <canvas class="skylink-stars" id="skystars" aria-hidden="true"></canvas>
    <span class="skylink-in">
      <span class="eyebrow" style="color:#9A8CB4">%s</span>
      <span class="skylink-h">%s</span>
      <span class="skylink-p">%s</span>
      <span class="skylink-btn">%s</span>
    </span>
  </a>

  <div class="sec-head">
    <h2>%s</h2>
    <span class="count">%s</span>
  </div>

%s

  <section class="cta" id="join">
    <div>
      <p class="eyebrow eyebrow--boxed">%s</p>
      <h2>%s</h2>
      <p class="lede">%s</p>
      <p style="font-size:15.5px;color:var(--muted);max-width:52ch">%s</p>
    </div>
    <div>
      <ol class="send-list">
        <li><span class="n">01</span><span>%s</span></li>
        <li><span class="n">02</span><span>%s</span></li>
        <li><span class="n">03</span><span>%s</span></li>
      </ol>
      <p style="margin:22px 0 0"><a class="btn mail" data-u="xinyufu" data-d="gsu.edu" data-s="Research assistant volunteer" href="#">%s</a></p>
      <p style="margin:14px 0 0;font-size:13.5px"><a href="/join/">%s</a></p>
    </div>
  </section>

  <div class="strip">
    <div class="strip-cell">
      <h3>%s</h3>
      <ul>
        <li><span class="yr">2026</span>%s</li>
        <li><span class="yr">2026</span>%s</li>
        <li><span class="yr">2026</span>%s</li>
        <li><span class="yr">2026</span>%s</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>%s</h3>
      <ul>
        <li><span class="yr">2026</span>%s</li>
        <li><span class="yr">2025</span>%s</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>%s</h3>
      <ul>
        <li><span class="yr">F26</span>%s</li>
        <li><span class="yr">S26</span>%s</li>
        <li><a href="/teaching/">%s</a></li>
      </ul>
    </div>
  </div>

%s

</div>

<script>
(function(){
  var cv = document.getElementById('skystars');
  if (!cv) return;
  /* A miniature of the real map, not a decorative starfield: the same 13
     studies at the same positions the citation layout puts them, the works
     they cite, and the lines where two studies share a reference. It sits to
     the right so the text keeps the left. */
  var MINI = __MINI__;
  function paint(){
    var r = cv.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width*dpr); cv.height = Math.round(r.height*dpr);
    var g = cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
    g.clearRect(0,0,r.width,r.height);

    /* faint dust everywhere, so the card is not empty on the left */
    var seed=4242; function rnd(){ seed=(seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; }
    for (var i=0;i<180;i++){
      g.globalAlpha=0.10+rnd()*0.28; g.fillStyle='#CFC2E8';
      g.beginPath(); g.arc(rnd()*r.width, rnd()*r.height, rnd()*0.9+0.3, 0, Math.PI*2); g.fill();
    }

    /* Drawn larger than the card and allowed to crop. Fitted whole it read as
       a stamp in the corner; running off the edge it reads as a window onto
       something bigger, which is what it is. The text column runs to 56ch, so
       side by side only works on a wide card; below that it sits underneath. */
    var narrow = r.width < 1080;
    var mh = narrow ? r.height*1.15 : r.height*1.55;
    var mw = mh*1.5625;                            // the map is 1600x1024
    if (narrow){ mw = r.width*1.5; mh = mw/1.5625; }
    var ox = narrow ? (r.width-mw)/2 : r.width*0.42;
    var oy = narrow ? r.height - mh*0.62 : (r.height-mh)/2;
    function X(v){ return ox + v*mw; }
    function Y(v){ return oy + v*mh; }

    MINI.l.forEach(function(l){
      g.strokeStyle='#C9B6FF';
      g.globalAlpha=Math.min(0.08+l[4]*0.05, 0.34);
      g.lineWidth=Math.min(0.4+l[4]*0.22, 1.4);
      g.beginPath(); g.moveTo(X(l[0]),Y(l[1])); g.lineTo(X(l[2]),Y(l[3])); g.stroke();
    });
    MINI.w.forEach(function(w){
      var shared = w[2] > 1;
      g.globalAlpha = shared ? 0.9 : 0.34;
      g.fillStyle = shared ? '#FFF4D6' : '#B9A9DA';
      g.beginPath(); g.arc(X(w[0]), Y(w[1]), shared ? 1.9 : 1.05, 0, Math.PI*2); g.fill();
    });
    MINI.s.forEach(function(st){
      var x=X(st[0]), y=Y(st[1]);
      var grd=g.createRadialGradient(x,y,0,x,y,10);
      grd.addColorStop(0,st[2]); grd.addColorStop(1,'rgba(0,0,0,0)');
      g.globalAlpha=0.55; g.fillStyle=grd;
      g.beginPath(); g.arc(x,y,10,0,Math.PI*2); g.fill();
      g.globalAlpha=1; g.fillStyle=st[2];
      g.beginPath(); g.arc(x,y,2.8,0,Math.PI*2); g.fill();
    });
    g.globalAlpha=1;
  }
  paint();
  var t; window.addEventListener('resize', function(){ clearTimeout(t); t=setTimeout(paint,160); });
})();
</script>
</body>
</html>
''' % (T.HOME_PAGE_TITLE,
       FONTS,
       nav('/'),
       T.HOME_ROLE,
       T.HOME_THESIS,

       '\n\n'.join(tiles),
       T.HOME_MAP_EYEBROW,
       T.HOME_MAP_HEADLINE,
       T.HOME_MAP_BLURB,
       T.HOME_MAP_BUTTON,
       T.HOME_SELECTED_RESEARCH_TITLE,
       T.HOME_SELECTED_RESEARCH_COUNT,
       home_entries,
       T.HOME_JOIN_EYEBROW,
       T.HOME_JOIN_HEADLINE,
       T.HOME_JOIN_LEDE,
       T.HOME_JOIN_RECENT_STUDENTS,
       T.HOME_JOIN_SEND_CV,
       T.HOME_JOIN_SEND_WRITING_SAMPLE,
       T.HOME_JOIN_SEND_WHICH_PROJECT,
       T.HOME_JOIN_EMAIL_BUTTON,
       T.HOME_JOIN_MORE_LINK,
       T.HOME_RECENT_TITLE,
       T.HOME_RECENT_JMIS,
       T.HOME_RECENT_CIST,
       T.HOME_RECENT_ICIS,
       T.HOME_RECENT_CHAPTER,
       T.HOME_PRESS_TITLE,
       T.HOME_PRESS_PATH,
       T.HOME_PRESS_EDUBOT,
       T.HOME_TEACHING_TITLE,
       T.HOME_TEACHING_F26,
       T.HOME_TEACHING_S26,
       T.HOME_TEACHING_ALL_COURSES,
       FOOT)
HOME = (HOME.replace('__N_CITED__', str(N_CITED)).replace('__N_STUDIES__', str(N_STUDIES))
            .replace('__MINI__', json.dumps(MINI, separators=(',', ':'))))
io.open(os.path.join(R, 'index.html'), 'w', encoding='utf-8').write(HOME)
print('index.html', len(HOME), 'bytes,', len(featured), 'featured')
