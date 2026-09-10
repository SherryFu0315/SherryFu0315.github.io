# -*- coding: utf-8 -*-
import hashlib, io, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import words as T
from projects import (PROJECTS, COLS, ROWS, LABEL, STAR_SIZE, FEATURED,
                      CARD, CARD_LINE, VENUE_SHORT)

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
_NEUTRAL = '#8E7FA8'
_MW, _MH = 1600, 1024
_sxy, _wxy, _kept, _ = _CL.layout(_studies, _works, box=(_MW, _MH))
_pairs = _CL.coupling(_studies, _kept)


def _wcol(w):
    """The same colouring the map itself uses: cream if more than one study
    reaches this work, otherwise the colour of the one study that does."""
    cs = [c for c in w['cited_by'] if c in _byid]
    return '#FFF4D6' if len(cs) > 1 else (_CBY.get(_byid[cs[0]]['col']) or _NEUTRAL)


def _p(xy):
    return [round(xy[0], 1), round(xy[1], 1)]


_sx = sorted(v[0] for v in _sxy.values())
_sy = sorted(v[1] for v in _sxy.values())

MINI = {
    # every cited work: position, colour, and how many studies reach it
    'w': [_p(_wxy[w['key']]) + [_wcol(w), len([c for c in w['cited_by'] if c in _byid])]
          for w in _kept],
    # every study: position, colour, label, size
    's': [_p(_sxy[p['id']]) + [_CBY.get(p['col']) or _NEUTRAL,
                              LABEL.get(p['id'], p['short']),
                              STAR_SIZE.get(p['chip'], 1)] for p in _studies],
    # the coupling lines, with the number of references the pair shares
    'l': [_p(_sxy[a]) + _p(_sxy[b]) + [n] for (a, b), n in _pairs.items()],
    # where the studies are, so the card can frame them: bounds and the median
    # row to centre on. The studies span a narrow band; the outliers above and
    # below it fall off the edge of the card, which is the point.
    'b': [round(_sx[0], 1), round(_sy[0], 1), round(_sx[-1], 1), round(_sy[-1], 1),
          round(_sy[len(_sy) // 2], 1)],
}

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root


def asset(path):
    """A content hash on the stylesheet and script URLs.

    Without one, a browser holding an older site.css renders the new HTML
    against the old rules. That does not look like a caching problem — it looks
    like the page is broken: every element whose class the old stylesheet has
    never heard of falls back to unstyled. It happened once here, after a hero
    was rebuilt and then reverted, and it cost an afternoon working out that the
    files on disk were fine all along.

    The query changes only when the file's bytes change, so a visitor keeps the
    cached copy until there is genuinely something new to fetch.
    """
    h = hashlib.sha256(io.open(os.path.join(R, path), 'rb').read()).hexdigest()[:8]
    return '/%s?v=%s' % (path, h)


CSS_URL, JS_URL = asset('assets/site.css'), asset('assets/site.js')

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
 '<link rel="stylesheet" href="%s">\n'
 '<script src="%s" defer></script>\n'
 '<link rel="icon" href="/profile.png">') % (CSS_URL, JS_URL)

def nav(cur):
    items=[('/research/',T.HOME_NAV_RESEARCH),('/universe/',T.HOME_NAV_MAP),
           ('/publications/',T.HOME_NAV_PUBLICATIONS),('/teaching/',T.HOME_NAV_TEACHING)]
    out=['  <nav class="nav">','    <a class="brand" href="/">%s</a>' % T.HOME_NAV_HOME,'    <div class="navlinks">']
    for href,label in items:
        out.append('      <a href="%s"%s>%s</a>' % (href, ' aria-current="page"' if href==cur else '', label))
    out.append('      <a href="/join/" class="is-cta"%s>%s</a>'
               % (' aria-current="page"' if cur=='/join/' else '', T.HOME_NAV_CONTACT))
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
  '        <span class="tile-arrow" aria-hidden="true">&#8599;</span>\n'
  '        <span class="tile-label"><span class="plus">AI+</span><span class="dom">%s</span>'
  '<span class="tile-more">%s</span></span>\n'
  '      </a>')
# hovering a card names the study it opens, so the four settings are an index
# rather than four photographs with a category on them
_short = {p['id']: p['short'] for p in PROJECTS}
tiles = [TILE_TPL % (pid, img, alt, note, label, _short.get(pid, ''))
         for pid, label, img, note, alt in MOSAIC]

_by_id = {x['id']: x for x in PROJECTS}
featured = [_by_id[i] for i in FEATURED]
_missing = [p['id'] for p in featured if not (p.get('photo') and p['finding'])]
assert not _missing, 'featured on the front page but has no photo or finding: %s' % _missing
CARD_TPL = """  <a class="card" href="/research/#%(id)s">
    <img src="/assets/img/%(img)s" alt="%(alt)s"%(lazy)s>
    <span class="card-wash" aria-hidden="true"></span>
    <span class="card-in">
      <span class="card-chip">%(chip)s</span>
      <span class="card-t">%(title)s</span>
      <span class="card-x">
        <span class="card-f">%(line)s</span>
        <span class="card-go">%(go)s</span>
      </span>
    </span>
  </a>"""


def card(p, i):
    """A photograph, what the study is called, and how far along it is. The one
    line of finding waits for a hover — on a phone there is no hover and the
    card is simply a link, which is what it is on a desktop too."""
    venue = VENUE_SHORT.get(p['id'], p['venue'])
    return CARD_TPL % dict(
        id=p['id'], img=p['photo'][0], alt=p['photo'][1],
        lazy='' if i < 3 else ' loading="lazy" decoding="async"',
        chip=p['chip'] + ((' &middot; ' + venue) if venue else ''),
        title=CARD.get(p['id'], p['short']),
        line=CARD_LINE.get(p['id'], ''),
        go=T.HOME_CARD_GO)


home_cards = '\n'.join(card(x, i) for i, x in enumerate(featured))

HOME = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(PAGE_TITLE)s</title>
<meta name="description" content="Xinyu Fu is an Assistant Professor of Computer Information Systems at Georgia State University. She studies how different ways of working with AI shape human performance, the organization of work, and the consequences of AI use.">
%(FONTS)s
</head>
<body>

<div class="topbar"></div>

<div class="shell">

%(NAV)s

  <header class="hero">
    <div class="rail">
      <div class="rail-id">
        <img class="rail-photo" src="/profile.png" alt="Xinyu Fu">
        <div>
          <h1>Xinyu Fu</h1>
          <p class="role">%(ROLE)s</p>
          <ul class="rail-meta">
            <li><a href="https://scholar.google.com/citations?user=0OM4QfkAAAAJ&amp;hl=en">%(LINK_SCHOLAR)s</a></li>
            <li><a class="mail" data-u="xinyufu" data-d="gsu.edu" href="#">%(LINK_EMAIL)s</a></li>
          </ul>
        </div>
      </div>

      <p class="thesis">%(THESIS)s</p>
    </div>

%(TILES)s
  </header>

  <div class="strip">
    <div class="strip-cell">
      <h3>%(RECENT_TITLE)s</h3>
      <ul>
        <li><span class="yr">2026</span>%(RECENT_JMIS)s</li>
        <li><span class="yr">2026</span>%(RECENT_CIST)s</li>
        <li><a href="/publications/">%(RECENT_MORE)s</a></li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>%(PRESS_TITLE)s</h3>
      <ul>
        <li><span class="yr">2026</span>%(PRESS_PATH)s</li>
        <li><span class="yr">2025</span>%(PRESS_EDUBOT)s</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>%(TEACH_TITLE)s</h3>
      <ul>
        <li><span class="yr">F26</span>%(TEACH_F26)s</li>
        <li><span class="yr">S26</span>%(TEACH_S26)s</li>
        <li><a href="/teaching/">%(TEACH_ALL)s</a></li>
      </ul>
    </div>
  </div>

  <a class="skylink" href="/universe/">
    <canvas class="skylink-stars" id="skystars" aria-hidden="true"></canvas>
    <span class="skylink-scrim" aria-hidden="true"></span>
    <span class="skylink-in">
      <span class="eyebrow" style="color:#9A8CB4">%(MAP_EYEBROW)s</span>
      <span class="skylink-h">%(MAP_HEADLINE)s</span>
      <span class="skylink-p">%(MAP_BLURB)s</span>
      <span class="skylink-btn">%(MAP_BUTTON)s</span>
    </span>
  </a>

  <div class="sec-head">
    <h2>%(SR_TITLE)s</h2>
    <span class="count">%(SR_COUNT)s</span>
  </div>

  <div class="cards">
%(ENTRIES)s
  </div>

%(FOOT)s

</div>

<script>
(function(){
  var cv = document.getElementById('skystars');
  if (!cv) return;
  /* Not a decorative starfield: this is the real map, zoomed to its core. The
     same studies at the positions the citation layout gives them, the works
     they cite in the same colours, and the lines where two studies share a
     reference. It is deliberately cropped &mdash; what runs off the edge is the
     rest of the map, which is the thing the card is inviting you into. */
  var MINI = __MINI__;
  var SPARK = new Path2D('M50 2 C54 31 69 46 98 50 C69 54 54 69 50 98 '
                       + 'C46 69 31 54 2 50 C31 46 46 31 50 2 Z');

  function paint(){
    var r = cv.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = Math.round(r.width*dpr); cv.height = Math.round(r.height*dpr);
    var g = cv.getContext('2d'); g.setTransform(dpr,0,0,dpr,0,0);
    g.clearRect(0,0,r.width,r.height);

    /* faint dust, so the frame does not go empty where the literature thins */
    var seed=4242; function rnd(){ seed=(seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; }
    for (var i=0;i<190;i++){
      g.globalAlpha=0.07+rnd()*0.22; g.fillStyle='#CFC2E8';
      g.beginPath(); g.arc(rnd()*r.width, rnd()*r.height, rnd()*0.9+0.3, 0, Math.PI*2); g.fill();
    }

    /* Zoom to the studies rather than fitting the whole map in. Fitted whole it
       read as a stamp in the corner; at roughly the scale the map itself opens
       at, the constellation is legible and the labels can be read. On a wide
       card the text keeps the left, so the core is pushed right of centre. */
    var b = MINI.b, pad = 78;
    var narrow = r.width < 860;   // must match the scrim's breakpoint in site.css
    var s = (narrow ? r.width*1.75 : r.width*0.78) / ((b[2]-b[0]) + pad*2);
    var ox = (narrow ? r.width*0.72 : r.width*0.66) - (b[0]+b[2])/2 * s;
    var oy = (narrow ? r.height*0.74 : r.height*0.50) - b[4] * s;
    function X(u){ return ox + u*s; }
    function Y(v){ return oy + v*s; }

    MINI.l.forEach(function(l){
      g.strokeStyle='#C9B6FF';
      g.globalAlpha=Math.min(0.10+l[4]*0.05, 0.38);
      g.lineWidth=Math.min(0.5+l[4]*0.28, 1.9);
      g.beginPath(); g.moveTo(X(l[0]),Y(l[1])); g.lineTo(X(l[2]),Y(l[3])); g.stroke();
    });
    MINI.w.forEach(function(w){
      var shared = w[3] > 1;
      g.globalAlpha = shared ? 0.92 : 0.44;
      g.fillStyle = w[2];
      g.beginPath(); g.arc(X(w[0]), Y(w[1]), shared ? 2.1 : 1.2, 0, Math.PI*2); g.fill();
    });
    MINI.s.forEach(function(st){
      var x=X(st[0]), y=Y(st[1]);
      if (x < -60 || x > r.width+60 || y < -60 || y > r.height+60) return;
      var R = 8 + st[4]*3.2;
      var grd=g.createRadialGradient(x,y,0,x,y,R*2.6);
      grd.addColorStop(0,st[2]); grd.addColorStop(1,'rgba(0,0,0,0)');
      g.globalAlpha=0.4; g.fillStyle=grd;
      g.beginPath(); g.arc(x,y,R*2.6,0,Math.PI*2); g.fill();
      g.globalAlpha=1; g.fillStyle=st[2];
      g.save(); g.translate(x-R, y-R); g.scale(R/50, R/50); g.fill(SPARK); g.restore();
    });

    /* Labels, kept off the words and off each other. The text column is
       measured rather than guessed at, so this holds at every width. A label
       that cannot be placed is dropped rather than nudged: the star still
       shows, and the whole map is one click away. */
    var txt = cv.parentNode.querySelector('.skylink-in');
    var tr = txt && txt.getBoundingClientRect();
    var ex = tr && {l:tr.left-r.left-14, t:tr.top-r.top-12,
                    rt:tr.right-r.left+14, b:tr.bottom-r.top+12};
    g.font='500 12px "IBM Plex Mono", ui-monospace, monospace';
    g.textBaseline='top';
    var taken=[];
    MINI.s.forEach(function(st){
      var x=X(st[0]), y=Y(st[1]);
      if (x < 8 || x > r.width-14) return;
      var R = 8 + st[4]*3.2;
      var bw = g.measureText(st[3]).width + 14, bh = 20;
      var bx = Math.min(Math.max(x-bw/2, 8), r.width-bw-8), by = y + R + 7;
      if (by < 8 || by+bh > r.height-8) return;
      if (ex && bx < ex.rt && bx+bw > ex.l && by < ex.b && by+bh > ex.t) return;
      for (var k=0;k<taken.length;k++){
        var t=taken[k];
        if (bx < t[0]+t[2]+7 && bx+bw+7 > t[0] && by < t[1]+t[3]+5 && by+bh+5 > t[1]) return;
      }
      taken.push([bx,by,bw,bh]);
      g.globalAlpha=0.76; g.fillStyle='#120A1F';
      g.fillRect(bx, by, bw, bh);
      g.globalAlpha=1; g.fillStyle='#E9E1F6';
      g.fillText(st[3], bx+7, by+4);
    });
    g.globalAlpha=1;
  }
  paint();
  // the labels are set in a web font; measured before it lands they come out wrong
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(paint);
  var t; window.addEventListener('resize', function(){ clearTimeout(t); t=setTimeout(paint,160); });
})();
</script>
</body>
</html>
''' % {
    # Named rather than positional: the front page has 37 substitutions and
    # its blocks get reordered. Positionally, moving one block silently
    # shifts every value after it, and the page still builds.
    'PAGE_TITLE': T.HOME_PAGE_TITLE,
    'FONTS': FONTS,
    'NAV': nav('/'),
    'ROLE': T.HOME_ROLE,
    'LINK_SCHOLAR': T.HOME_LINK_SCHOLAR,
    'LINK_EMAIL': T.HOME_LINK_EMAIL,
    'THESIS': T.HOME_THESIS,
    'TILES': '\n\n'.join(tiles),
    'MAP_EYEBROW': T.HOME_MAP_EYEBROW,
    'MAP_HEADLINE': T.HOME_MAP_HEADLINE,
    'MAP_BLURB': T.HOME_MAP_BLURB,
    'MAP_BUTTON': T.HOME_MAP_BUTTON,
    'SR_TITLE': T.HOME_SELECTED_RESEARCH_TITLE,
    'SR_COUNT': T.HOME_SELECTED_RESEARCH_COUNT,
    'ENTRIES': home_cards,
    'RECENT_TITLE': T.HOME_RECENT_TITLE,
    'RECENT_JMIS': T.HOME_RECENT_JMIS,
    'RECENT_CIST': T.HOME_RECENT_CIST,
    'RECENT_MORE': T.HOME_RECENT_MORE,
    'PRESS_TITLE': T.HOME_PRESS_TITLE,
    'PRESS_PATH': T.HOME_PRESS_PATH,
    'PRESS_EDUBOT': T.HOME_PRESS_EDUBOT,
    'TEACH_TITLE': T.HOME_TEACHING_TITLE,
    'TEACH_F26': T.HOME_TEACHING_F26,
    'TEACH_S26': T.HOME_TEACHING_S26,
    'TEACH_ALL': T.HOME_TEACHING_ALL_COURSES,
    'FOOT': FOOT,
}
_NUM = {1:'One',2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',
        9:'Nine',10:'Ten',11:'Eleven',12:'Twelve',13:'Thirteen',14:'Fourteen',
        15:'Fifteen',16:'Sixteen',17:'Seventeen',18:'Eighteen'}


def _num(n):
    """Spelled out, because these counts sit in sentences. Derived rather than
    written down: the front page said 'Six of thirteen' for some time after
    there were fifteen."""
    return _NUM.get(n, str(n))


HOME = (HOME.replace('__N_FEATURED__', _num(len(featured)))
            .replace('__N_PROJECTS__', _num(len(PROJECTS)).lower())
            .replace('__N_CITED__', str(N_CITED)).replace('__N_STUDIES__', str(N_STUDIES))
            .replace('__MINI__', json.dumps(MINI, separators=(',', ':'))))
io.open(os.path.join(R, 'index.html'), 'w', encoding='utf-8').write(HOME)
print('index.html', len(HOME), 'bytes,', len(featured), 'featured')

# publications/ and credits/ are hand-written rather than generated, but their
# stylesheet link has to carry the same hash as everyone else's or they are the
# two pages that break after a CSS change. Only the query string is touched.
import re as _re
for _p in ('publications/index.html', 'credits/index.html'):
    _f = os.path.join(R, _p)
    _s = io.open(_f, encoding='utf-8').read()
    _n = _re.sub(r'/assets/site\.css(\?v=[0-9a-f]+)?', CSS_URL, _s)
    _n = _re.sub(r'/assets/site\.js(\?v=[0-9a-f]+)?', JS_URL, _n)
    if _n != _s:
        io.open(_f, 'w', encoding='utf-8').write(_n)
        print('stamped', _p)
