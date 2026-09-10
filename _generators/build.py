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
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&family=Playfair+Display:ital,wght@0,600;1,600;1,700&display=swap">\n'
 '<link rel="stylesheet" href="%s">\n'
 '<script src="%s" defer></script>\n'
 '<link rel="icon" href="/assets/favicon.svg">') % (CSS_URL, JS_URL)

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


_by_id = {x['id']: x for x in PROJECTS}
featured = [_by_id[i] for i in FEATURED]
_missing = [p['id'] for p in featured if not (p.get('photo') and p['finding'])]
assert not _missing, 'featured on the front page but has no photo or finding: %s' % _missing

CARD_TPL = """  <a class="card" href="/research/#%(id)s">
    <img src="/assets/img/%(img)s" alt="%(alt)s"%(lazy)s>
    <span class="card-wash" aria-hidden="true"></span>
    <span class="card-chip">%(chip)s</span>
    <span class="card-arrow" aria-hidden="true">&#8599;</span>
    <span class="card-in">
      <span class="card-t"><span class="plus">AI+</span><span class="dom">%(title)s</span></span>
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
    <div class="hero-me">
      <img class="hero-photo" src="/profile.png" alt="Xinyu Fu" fetchpriority="high">
      <p class="hero-mail"><a class="mail" data-u="xinyufu" data-d="gsu.edu" href="#">%(EMAIL)s</a></p>
    </div>

    <div class="hero-say">
      <h1 class="hello">%(HELLO)s</h1>
      <p class="intro">%(INTRO_1)s</p>
      <p class="intro">%(INTRO_2)s</p>
    </div>
  </header>

  <div class="sec-head sec-head--bare">
    <h2>%(SR_TITLE)s</h2>
    <span class="count">%(SR_COUNT)s</span>
  </div>

  <div class="cards">
%(ENTRIES)s
  </div>

  <section class="news">
    <div class="news-cell news-cell--list">
      <p class="eyebrow">%(NEWS_TITLE)s</p>
      <ul class="newslist" role="list">
        <li><span class="yr">2026</span><span>%(NEWS_1)s</span></li>
        <li><span class="yr">2026</span><span>%(NEWS_2)s</span></li>
        <li><span class="yr">2026</span><span>%(NEWS_3)s</span></li>
        <li><span class="yr">2026</span><span>%(NEWS_4)s</span></li>
      </ul>
      <p class="news-more"><a href="/publications/">%(NEWS_MORE)s</a></p>
    </div>

    <div class="news-side">
      <div class="news-cell">
        <p class="eyebrow">%(PRESS_TITLE)s</p>
        <ul class="newslist" role="list">
          <li><span class="yr">%(PRESS_1_OUTLET)s</span><span>%(PRESS_1)s</span></li>
          <li><span class="yr">%(PRESS_2_OUTLET)s</span><span>%(PRESS_2)s</span></li>
        </ul>
      </div>
      <div class="news-cell news-cell--teaching">
        <p class="eyebrow">%(COURSE_TITLE)s</p>
        <p class="course-name">%(COURSE_NAME)s<span class="course-term">%(COURSE_TERM)s</span></p>
        <p class="news-also">%(COURSE_PATH)s</p>
        <p class="news-more"><a href="https://sherryfu0315.github.io/cis4394-agentic-ai/index.html">%(COURSE_LINK)s</a> &nbsp;<a href="/teaching/">%(COURSE_ALL)s</a></p>
      </div>
    </div>
  </section>

%(FOOT)s

</div>

</body>
</html>
''' % {
    # Named rather than positional: the front page has 37 substitutions and
    # its blocks get reordered. Positionally, moving one block silently
    # shifts every value after it, and the page still builds.
    'PAGE_TITLE': T.HOME_PAGE_TITLE,
    'HELLO': T.HOME_HELLO,
    'INTRO_1': T.HOME_INTRO_1,
    'INTRO_2': T.HOME_INTRO_2,
    'EMAIL': T.HOME_EMAIL,
    'FONTS': FONTS,
    'NAV': nav('/'),
    'SR_TITLE': T.HOME_SELECTED_RESEARCH_TITLE,
    'SR_COUNT': T.HOME_SELECTED_RESEARCH_COUNT,
    'ENTRIES': home_cards,
    'NEWS_TITLE': T.HOME_NEWS_TITLE,
    'NEWS_1': T.HOME_NEWS_1,
    'NEWS_2': T.HOME_NEWS_2,
    'NEWS_3': T.HOME_NEWS_3,
    'NEWS_4': T.HOME_NEWS_4,
    'NEWS_MORE': T.HOME_NEWS_MORE,
    'PRESS_TITLE': T.HOME_PRESS_TITLE,
    'PRESS_1_OUTLET': T.HOME_PRESS_1_OUTLET,
    'PRESS_1': T.HOME_PRESS_1,
    'PRESS_2_OUTLET': T.HOME_PRESS_2_OUTLET,
    'PRESS_2': T.HOME_PRESS_2,
    'COURSE_TITLE': T.HOME_COURSE_TITLE,
    'COURSE_NAME': T.HOME_COURSE_NAME,
    'COURSE_TERM': T.HOME_COURSE_TERM,
    'COURSE_PATH': T.HOME_COURSE_PATH,
    'COURSE_LINK': T.HOME_COURSE_LINK,
    'COURSE_ALL': T.HOME_COURSE_ALL,
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
            .replace('__N_PROJECTS__', _num(len(PROJECTS)).lower()))
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
