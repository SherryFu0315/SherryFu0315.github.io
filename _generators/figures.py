# -*- coding: utf-8 -*-
"""Five drawn figures. Each is a self-contained SVG on a 400x300 stage using
only the course-deck palette, and each encodes that project's real mechanism."""

INK='#1E102F'; BLUE='#274CEC'; CORAL='#FF7874'; LAV='#ECB8FF'; LIME='#DCFF96'; PAPER='#F6F4F9'
MONO='font-family="IBM Plex Mono, ui-monospace, monospace"'

def _wrap(inner, label):
    return ('<svg viewBox="0 0 400 300" role="img" aria-label="%s" preserveAspectRatio="xMidYMid meet">\n%s\n</svg>'
            % (label, inner))

def fig_retrieval():
    """Two numbers and a slope. No key needed."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text x="26" y="24" %s font-size="9.5" letter-spacing="1.3" fill="%s">SHARE OF ERRORS CAUGHT IN AN AI ANSWER</text>' % (MONO, INK))
    base=194
    for x,val,col,l1,l2 in [(58,0.68,INK,'READ THE SYSTEM&#8217;S','EXPLANATION'),
                            (168,0.78,LIME,'WRITE YOUR OWN','EXPLANATION')]:
        h=int(val*140)
        p.append('<rect x="%d" y="%d" width="72" height="%d" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, base-h, h, col, INK))
        p.append('<text x="%d" y="%d" font-family="Archivo, Arial Black, Arial, sans-serif" font-size="27" font-weight="800" fill="%s" text-anchor="middle">%s</text>' % (x+36, base-h-12, INK, ('%.2f'%val)))
        p.append('<text x="%d" y="212" %s font-size="8.5" letter-spacing=".6" fill="%s" text-anchor="middle">%s</text>' % (x+36, MONO, INK, l1))
        p.append('<text x="%d" y="223" %s font-size="8.5" letter-spacing=".6" fill="%s" text-anchor="middle">%s</text>' % (x+36, MONO, INK, l2))
    p.append('<line x1="44" y1="194" x2="256" y2="194" stroke="%s" stroke-width="2.5"/>' % INK)
    p.append('<text x="26" y="256" %s font-size="9.5" letter-spacing="1.3" fill="%s">&#8230; AND IT WEARS OFF OVER TWO WEEKS</text>' % (MONO, INK))
    p.append('<line x1="28" y1="292" x2="286" y2="292" stroke="%s" stroke-width="2" opacity=".35"/>' % INK)
    p.append('<path d="M30 266 L 286 290" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % CORAL)
    p.append('<path d="M30 266 L 286 278" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="7 6"/>' % BLUE)
    p.append('<text x="294" y="281" %s font-size="8.5" fill="%s">WITH A CUE</text>' % (MONO, BLUE))
    p.append('<text x="294" y="295" %s font-size="8.5" fill="%s">WITHOUT</text>' % (MONO, CORAL))
    return _wrap('\n'.join(p), 'A bar chart: reading the system explanation catches 0.68 of errors, writing your own catches 0.78. Below, two falling lines show detection decaying over two weeks, the decline shallower when a retrieval cue is present.')


def fig_autoglass():
    """Close on the aperture: a windscreen coming down onto the frame, held on
    suction cups, steadied by a gloved hand. Glass, not car assembly."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text class="fig-cap" x="24" y="28" %s font-size="9.5" letter-spacing="1.3" fill="%s">SET BY HAND AND MACHINE TOGETHER</text>' % (MONO, INK))
    p.append('<path d="M74 288 L 108 214 L 292 214 L 326 288 Z" fill="%s" fill-opacity=".10" stroke="%s" stroke-width="2.5"/>' % (INK, INK))
    p.append('<path d="M94 280 L 122 224 L 278 224 L 306 280 Z" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 6" opacity=".55"/>' % INK)
    p.append('<g transform="rotate(-6 200 126)">')
    p.append('<path d="M112 168 L 140 76 L 262 76 L 290 168 Z" fill="%s" fill-opacity=".55" stroke="%s" stroke-width="2.5"/>' % (LIME, INK))
    p.append('<path d="M134 160 L 154 92 L 214 92 L 214 160 Z" fill="%s" fill-opacity=".30"/>' % PAPER)
    for cx,cy in ((152,110),(250,110),(200,148)):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="72" stroke="%s" stroke-width="3"/>' % (cx, cy-13, cx, INK))
        p.append('<circle cx="%d" cy="%d" r="13" fill="%s" stroke="%s" stroke-width="2.5"/>' % (cx, cy, PAPER, INK))
        p.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (cx, cy, INK))
    p.append('<rect x="140" y="56" width="122" height="16" rx="5" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LAV, INK))
    p.append('</g>')
    p.append('<path d="M388 22 L 330 40 L 268 58" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>' % INK)
    p.append('<circle cx="330" cy="40" r="8" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LAV, INK))
    for x in (140, 200, 262):
        p.append('<path d="M%d 184 L %d 208" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round" opacity=".85"/>' % (x, x, BLUE))
        p.append('<path d="M%d 199 L %d 209 L %d 199" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/>' % (x-6, x, x+6, BLUE))
    p.append('<path d="M62 200 C 44 194, 36 174, 50 168 C 42 156, 56 146, 68 154 L 98 172 L 88 204 Z" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (CORAL, INK))
    return _wrap('\n'.join(p), 'A curved windscreen pane held on three suction cups hanging from a manipulator arm, descending into the trapezoid aperture of a vehicle body, with a gloved hand steadying its lower edge.')


def fig_doorhandover():
    """A guest at their own door, in a robe, taking a parcel from the robot."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text class="fig-cap" x="24" y="30" %s font-size="9.5" letter-spacing="1.3" fill="%s">THE DOOR OPENS WIDER. THE GUEST SAYS LESS.</text>' % (MONO, INK))
    p.append('<rect x="30" y="52" width="150" height="228" fill="none" stroke="%s" stroke-width="2.5"/>' % INK)
    p.append('<path d="M180 52 L 246 78 L 246 254 L 180 280 Z" fill="%s" fill-opacity=".55" stroke="%s" stroke-width="2.5"/>' % (LAV, INK))
    p.append('<circle cx="192" cy="170" r="5" fill="%s"/>' % INK)
    p.append('<path d="M62 280 L 68 176 C 68 156, 124 156, 124 176 L 130 280 Z" fill="%s" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (PAPER, INK))
    p.append('<circle cx="96" cy="118" r="21" fill="%s" stroke="%s" stroke-width="2.5"/>' % (CORAL, INK))
    p.append('<path d="M84 160 L 96 202 L 108 160" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % INK)
    p.append('<rect x="70" y="210" width="52" height="10" rx="4" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LIME, INK))
    p.append('<path d="M120 182 C 148 182, 162 190, 178 198" fill="none" stroke="%s" stroke-width="9" stroke-linecap="round"/>' % INK)
    p.append('<path d="M120 182 C 148 182, 162 190, 178 198" fill="none" stroke="%s" stroke-width="4" stroke-linecap="round"/>' % PAPER)
    p.append('<path d="M296 274 L 296 152 C 296 130, 372 130, 372 152 L 372 274 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (BLUE, INK))
    p.append('<rect x="312" y="152" width="44" height="26" rx="5" fill="%s" stroke="%s" stroke-width="2"/>' % (PAPER, INK))
    p.append('<circle cx="325" cy="165" r="3.5" fill="%s"/><circle cx="343" cy="165" r="3.5" fill="%s"/>' % (INK, INK))
    p.append('<path d="M296 208 L 272 196 L 272 228 L 296 238 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LIME, INK))
    p.append('<rect x="186" y="186" width="36" height="28" rx="3" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LIME, INK))
    p.append('<line x1="204" y1="186" x2="204" y2="214" stroke="%s" stroke-width="2"/>' % INK)
    p.append('<g opacity=".4"><path d="M196 74 h60 a6 6 0 0 1 6 6 v26 a6 6 0 0 1-6 6 h-32 l-12 12 v-12 h-16 a6 6 0 0 1-6-6 V80 a6 6 0 0 1 6-6 z" fill="%s" stroke="%s" stroke-width="2.5"/></g>' % (PAPER, INK))
    p.append('<line x1="198" y1="118" x2="262" y2="70" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % CORAL)
    return _wrap('\n'.join(p), 'A person in a belted robe stands at their open hotel-room door, one arm reaching out to take a parcel from the open hatch of a delivery robot in the corridor. A speech bubble above is faded and struck through.')


def fig_remote():
    """A laptop at a kitchen table, the team present only as a call grid."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text x="24" y="32" %s font-size="9.5" letter-spacing="1.3" fill="%s">THE WHOLE TEAM, ON ONE TABLE</text>' % (MONO, INK))
    # window and a plant, so it reads as home not office
    p.append('<rect x="272" y="54" width="104" height="96" fill="%s" fill-opacity=".35" stroke="%s" stroke-width="2.5"/>' % (BLUE, INK))
    p.append('<line x1="324" y1="54" x2="324" y2="150" stroke="%s" stroke-width="2"/>' % INK)
    p.append('<line x1="272" y1="102" x2="376" y2="102" stroke="%s" stroke-width="2"/>' % INK)
    p.append('<path d="M300 214 C 292 190, 306 176, 300 160 M300 190 C 286 184, 282 172, 284 166 M300 182 C 314 176, 318 166, 316 160" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % INK)
    p.append('<path d="M288 214 L 312 214 L 308 240 L 292 240 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (CORAL, INK))
    # the laptop
    p.append('<path d="M62 224 L 84 118 L 232 118 L 254 224 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (INK, INK))
    p.append('<rect x="92" y="126" width="132" height="86" fill="%s"/>' % PAPER)
    cells=[(98,132,LIME),(162,132,LAV),(98,174,BLUE),(162,174,CORAL)]
    for x,y,col in cells:
        p.append('<rect x="%d" y="%d" width="56" height="34" rx="3" fill="%s" fill-opacity=".8" stroke="%s" stroke-width="1.5"/>' % (x, y, col, INK))
        p.append('<circle cx="%d" cy="%d" r="7" fill="%s" opacity=".8"/>' % (x+28, y+13, INK))
        p.append('<path d="M%d %d a10 10 0 0 1 20 0 z" fill="%s" opacity=".8"/>' % (x+18, y+29, INK))
    p.append('<rect x="46" y="224" width="224" height="12" rx="5" fill="%s"/>' % INK)
    # a mug
    p.append('<path d="M300 262 h34 v20 a10 10 0 0 1 -10 10 h-14 a10 10 0 0 1 -10 -10 z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LIME, INK))
    p.append('<path d="M334 268 a9 9 0 0 1 0 14" fill="none" stroke="%s" stroke-width="2.5"/>' % INK)
    return _wrap('\n'.join(p), 'An open laptop on a table showing a four-person video call grid, beside a window, a houseplant and a mug.')


def fig_coding():
    """A code editor with one line flagged: what checking an AI answer looks like."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<rect x="30" y="42" width="340" height="216" rx="6" fill="%s" stroke="%s" stroke-width="2.5"/>' % (INK, INK))
    p.append('<rect x="30" y="42" width="340" height="24" rx="6" fill="%s"/>' % INK)
    for i,c in enumerate([CORAL, LIME, LAV]):
        p.append('<circle cx="%d" cy="54" r="4.5" fill="%s"/>' % (48+i*16, c))
    p.append('<text x="200" y="58" %s font-size="9" letter-spacing="1.2" fill="%s" text-anchor="middle" opacity=".65">SUGGESTED BY THE MODEL</text>' % (MONO, PAPER))
    rows=[(88,150,BLUE),(106,210,None),(124,178,None),(142,246,None),
          (160,196,'FLAG'),(178,164,None),(196,222,None),(214,140,LIME),(232,188,None)]
    for y,w,kind in rows:
        if kind=='FLAG':
            p.append('<rect x="44" y="%d" width="316" height="18" rx="3" fill="%s" fill-opacity=".22"/>' % (y-4, CORAL))
            p.append('<rect x="44" y="%d" width="4" height="18" fill="%s"/>' % (y-4, CORAL))
        p.append('<text x="56" y="%d" %s font-size="9" fill="%s" opacity=".5">%02d</text>' % (y+8, MONO, PAPER, rows.index((y,w,kind))+1))
        col = CORAL if kind=='FLAG' else (kind if kind else PAPER)
        op  = '1' if kind=='FLAG' else ('.85' if kind else '.34')
        p.append('<rect x="78" y="%d" width="%d" height="7" rx="3.5" fill="%s" opacity="%s"/>' % (y+2, w, col, op))
    # the human catching it
    p.append('<circle cx="352" cy="164" r="20" fill="none" stroke="%s" stroke-width="3.5"/>' % CORAL)
    p.append('<line x1="366" y1="178" x2="382" y2="196" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % CORAL)
    p.append('<text x="30" y="286" %s font-size="9.5" letter-spacing="1.3" fill="%s">ONE LINE IS WRONG. WHO NOTICES, AND WHEN?</text>' % (MONO, INK))
    return _wrap('\n'.join(p), 'A dark code editor window with numbered lines of code, one line highlighted in coral and circled by a magnifying glass.')


def fig_crowdfund():
    """Two campaigns, identical until one of them discloses."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text x="24" y="32" %s font-size="9.5" letter-spacing="1.3" fill="%s">TWO CAMPAIGNS, ONE LABEL APART</text>' % (MONO, INK))
    def campaign(y, pct, label, col, disclosed):
        out=['<text x="24" y="%d" %s font-size="9" letter-spacing="1" fill="%s">%s</text>' % (y-12, MONO, INK, label)]
        out.append('<rect x="24" y="%d" width="270" height="26" rx="13" fill="%s" opacity=".22"/>' % (y, INK))
        out.append('<rect x="24" y="%d" width="%d" height="26" rx="13" fill="%s" stroke="%s" stroke-width="2.5"/>' % (y, int(270*pct), col, INK))
        out.append('<text x="306" y="%d" font-family="Archivo, Arial Black, Arial, sans-serif" font-size="21" font-weight="800" fill="%s">%d%%</text>' % (y+21, INK, int(pct*100)))
        if disclosed:
            out.append('<rect x="24" y="%d" width="128" height="20" rx="4" fill="%s" stroke="%s" stroke-width="2"/>' % (y+34, CORAL, INK))
            out.append('<text x="88" y="%d" %s font-size="8.5" letter-spacing="1" fill="%s" text-anchor="middle">AI DISCLOSED</text>' % (y+48, MONO, INK))
        return out
    p+=campaign(66, 0.86, 'HANDMADE, NO LABEL', LIME, False)
    p+=campaign(160, 0.31, 'HANDMADE, AND DISCLOSED', CORAL, True)
    p.append('<path d="M186 108 C 196 128, 196 136, 186 152" fill="none" stroke="%s" stroke-width="2.5" stroke-dasharray="5 5"/>' % INK)
    p.append('<path d="M180 144 L 186 154 L 193 144" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % INK)
    p.append('<text x="24" y="272" %s font-size="9" letter-spacing="1" fill="%s" opacity=".72">THE MORE HANDMADE THE PITCH, THE HARDER THE FALL</text>' % (MONO, INK))
    return _wrap('\n'.join(p), 'Two crowdfunding progress bars. The first, an unlabelled handmade campaign, is nearly full. The second, the same campaign carrying an AI-disclosed label, stops far short.')


def fig_diversity():
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    def panel(x0,title,pts,colour,rings):
        out=['<rect x="%d" y="52" width="168" height="196" fill="none" stroke="%s" stroke-width="2"/>' % (x0, INK),
             '<text x="%d" y="40" %s font-size="10.5" letter-spacing="1.6" fill="%s" text-anchor="middle">%s</text>' % (x0+84, MONO, INK, title)]
        for r in rings:
            out.append('<circle cx="%d" cy="150" r="%d" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="4 6" opacity=".45"/>' % (x0+84, r, colour))
        for dx,dy in pts:
            out.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (x0+84+dx, 150+dy, colour))
        return out
    spread=[(-58,-62),(-24,-78),(16,-66),(52,-44),(64,-6),(48,40),(14,66),(-26,74),(-58,44),(-68,4),(-8,-22),(28,12),(-36,22),(2,40),(-14,-46),(38,-22)]
    tight=[(-13,-14),(-4,-19),(8,-12),(14,2),(9,13),(-2,17),(-12,11),(-17,-1),(0,0),(5,-6),(-7,4),(12,-4),(-3,9),(17,9),(-18,-10),(3,-9)]
    p+=panel(22,'ANSWERED BY PEOPLE',spread,INK,[])
    p+=panel(210,'ANSWERED BY A MODEL',tight,BLUE,[66,44,26])
    p.append('<text x="294" y="274" %s font-size="9" letter-spacing="1.2" fill="%s" text-anchor="middle" opacity=".72">EACH GENERATION, TIGHTER</text>' % (MONO, INK))
    return _wrap('\n'.join(p), 'Two framed panels. On the left, answers given by people scatter across the whole frame. On the right, answers given by a model cluster near the centre inside rings marking each generation drawing tighter.')

def fig_repeat():
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER,
       '<text x="98" y="34" %s font-size="9.5" letter-spacing="1.2" fill="%s" text-anchor="middle">ONE WORDING, SIX TIMES</text>' % (MONO, INK),
       '<text x="302" y="34" %s font-size="9.5" letter-spacing="1.2" fill="%s" text-anchor="middle">SAMPLED WORDINGS</text>' % (MONO, INK)]
    for i in range(6):
        y=58+i*36; op=1.0-i*0.15
        p.append('<rect x="22" y="%d" width="152" height="22" fill="%s" stroke="%s" stroke-width="2" opacity="%.2f"/>' % (y, LAV, INK, op))
        for k in range(5):
            p.append('<rect x="%d" y="%d" width="18" height="6" fill="%s" opacity="%.2f"/>' % (32+k*27, y+8, INK, op*.7))
    for i,w in enumerate([152,128,146,112,138,120]):
        y=58+i*36
        p.append('<rect x="226" y="%d" width="%d" height="22" fill="%s" stroke="%s" stroke-width="2"/>' % (y, w, LIME, INK))
        n=3+(i%3)
        step=max(14,(w-24)//n)
        for k in range(n):
            p.append('<rect x="%d" y="%d" width="%d" height="6" fill="%s" opacity=".7"/>' % (236+k*step, y+8, max(9,step-9), INK))
    p.append('<text x="98" y="214" font-family="Archivo, Arial Black, Arial, sans-serif" font-size="150" font-weight="800" fill="%s" fill-opacity=".8" stroke="%s" stroke-width="3" text-anchor="middle">?</text>' % (CORAL, INK))
    return _wrap('\n'.join(p), 'Two columns of bars. On the left the same bar repeats six times and fades down the column, with a large question mark over it. On the right six different bars each keep their strength.')

def fig_earnings():
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER,
       '<text x="22" y="32" %s font-size="9.5" letter-spacing="1.4" fill="%s">WHAT MANAGEMENT SAYS</text>' % (MONO, INK)]
    heights=[18,34,26,46,30,58,40,66,30,22,44,62,74,52,36,26,42,30,20,34,28,46,24,18]
    hot={11,12,13}
    for i,h in enumerate(heights):
        x=24+i*15; y=112-h//2
        col=CORAL if i in hot else INK
        op='1' if i in hot else '.5'
        p.append('<rect x="%d" y="%d" width="8" height="%d" rx="3" fill="%s" opacity="%s"/>' % (x, y, h, col, op))
    p.append('<rect x="%d" y="34" width="%d" height="156" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="5 5" opacity=".85"/>' % (24+11*15-6, 15*3+4, CORAL))
    p.append('<text x="22" y="216" %s font-size="9.5" letter-spacing="1.4" fill="%s">WHAT THE FIRM THEN SPENDS</text>' % (MONO, INK))
    p.append('<path d="M24 268 L 140 268 L 198 264 L 206 242 L 268 234 L 330 228 L 376 222" fill="none" stroke="%s" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>' % BLUE)
    p.append('<line x1="202" y1="200" x2="202" y2="278" stroke="%s" stroke-width="2" stroke-dasharray="4 4"/>' % CORAL)
    p.append('<circle cx="202" cy="253" r="6" fill="%s" stroke="%s" stroke-width="2"/>' % (CORAL, INK))
    return _wrap('\n'.join(p), 'An audio waveform of an earnings call with three bars highlighted and boxed, and beneath it a spending line that turns upward at the moment those words were spoken.')

def fig_triage():
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER,
       '<text x="200" y="26" %s font-size="9.5" letter-spacing="1.8" fill="%s" text-anchor="middle" opacity=".7">ARRIVING &#8594; SORTED &#8594; SERVED</text>' % (MONO, INK)]
    # an undifferentiated queue
    for i,y in enumerate([70,98,126,154,182,210,238]):
        cx=26+(i%2)*14
        p.append('<circle cx="%d" cy="%d" r="7.5" fill="%s" opacity=".75"/>' % (cx, y, INK))
        p.append('<line x1="%d" y1="%d" x2="112" y2="154" stroke="%s" stroke-width="1.4" opacity=".24"/>' % (cx+11, y, INK))
    # the model doing the sorting
    p.append('<path d="M112 154 L 146 112 L 214 112 L 248 154 L 214 196 L 146 196 Z" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LAV, INK))
    p.append('<text x="180" y="150" %s font-size="13" letter-spacing="2.5" fill="%s" text-anchor="middle">AI</text>' % (MONO, INK))
    p.append('<text x="180" y="170" %s font-size="8.5" letter-spacing="1.3" fill="%s" text-anchor="middle" opacity=".72">TRIAGE</text>' % (MONO, INK))
    # three lanes, each ending well clear of its label
    for y,w,col,name in [(74,24,LIME,'ROUTINE'),(154,11,BLUE,'SPECIALIST'),(234,5,CORAL,'URGENT')]:
        p.append('<path d="M248 154 C 282 154, 282 %d, 316 %d" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" opacity=".92"/>' % (y, y, col, w))
        p.append('<circle cx="316" cy="%d" r="%.1f" fill="%s" stroke="%s" stroke-width="2"/>' % (y, w/2.0+1.5, col, INK))
        p.append('<text x="392" y="%d" %s font-size="9" letter-spacing="1.1" fill="%s" text-anchor="end">%s</text>' % (y+3, MONO, INK, name))
    return _wrap('\n'.join(p), 'A queue of identical arrivals feeds a hexagonal node marked AI triage, which splits into three outgoing lanes of very different thickness labelled routine, specialist and urgent.')

def fig_hiring():
    """AI in hiring: a stack of applications, a model that ranks them, and the
    part of the decision that stays with a person."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text class="fig-cap" x="22" y="26" %s font-size="9.5" letter-spacing="1.3" fill="%s">THE MODEL RANKS. SOMEONE STILL DECIDES.</text>' % (MONO, INK))
    # applications going in
    for i,(x,y) in enumerate(((22,86),(34,110),(46,134))):
        p.append('<rect x="%d" y="%d" width="62" height="80" rx="4" fill="%s" stroke="%s" stroke-width="2.5"/>' % (x, y, PAPER, INK))
        for k in range(4):
            p.append('<rect x="%d" y="%d" width="%d" height="5" rx="2.5" fill="%s" opacity=".45"/>' % (x+9, y+16+k*14, 44-(k%2)*12, INK))
        p.append('<circle cx="%d" cy="%d" r="7" fill="%s" opacity=".7"/>' % (x+18, y+9, INK))
    p.append('<path d="M116 176 L 146 176" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % INK)
    p.append('<path d="M138 170 L 148 176 L 138 182" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % INK)
    # the model
    p.append('<rect x="150" y="140" width="72" height="72" rx="10" fill="%s" stroke="%s" stroke-width="2.5"/>' % (LAV, INK))
    p.append('<text x="186" y="176" %s font-size="13" letter-spacing="2" fill="%s" text-anchor="middle">AI</text>' % (MONO, INK))
    p.append('<text x="186" y="194" %s font-size="8" letter-spacing="1.2" fill="%s" text-anchor="middle" opacity=".72">SCREEN</text>' % (MONO, INK))
    # the ranked shortlist it produces
    scores=[('94',LIME),('88',LIME),('61',None),('47',None)]
    for i,(sc,col) in enumerate(scores):
        y=76+i*38
        p.append('<rect x="248" y="%d" width="112" height="28" rx="4" fill="%s" stroke="%s" stroke-width="2.5"/>' % (y, col if col else PAPER, INK))
        p.append('<circle cx="266" cy="%d" r="8" fill="%s" opacity=".75"/>' % (y+14, INK))
        p.append('<rect x="280" y="%d" width="40" height="5" rx="2.5" fill="%s" opacity=".5"/>' % (y+11, INK))
        p.append('<text x="348" y="%d" %s font-size="11" fill="%s" text-anchor="end">%s</text>' % (y+18, MONO, INK, sc))
    p.append('<path d="M226 176 L 244 176" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % INK)
    # the person who signs it off
    p.append('<circle cx="304" cy="238" r="15" fill="%s" stroke="%s" stroke-width="2.5"/>' % (CORAL, INK))
    p.append('<path d="M280 286 C 280 258, 328 258, 328 286" fill="none" stroke="%s" stroke-width="2.5"/>' % INK)
    p.append('<path d="M248 104 C 224 104, 224 238, 282 244" fill="none" stroke="%s" stroke-width="2.5" stroke-dasharray="6 6" opacity=".75"/>' % CORAL)
    return _wrap('\n'.join(p), 'A stack of job applications feeds a box marked AI screen, which outputs a ranked shortlist with match scores; a dashed line runs from the top-ranked candidate down to a person who makes the final call.')


def fig_edubot():
    """The tutor itself: a lesson answered in the language the learner speaks."""
    p=['<rect x="0" y="0" width="400" height="300" fill="%s"/>' % PAPER]
    p.append('<text class="fig-cap" x="22" y="26" %s font-size="9.5" letter-spacing="1.3" fill="%s">THE LESSON, IN THE LANGUAGE AT HOME</text>' % (MONO, INK))
    # blackboard behind
    p.append('<rect x="216" y="52" width="164" height="112" rx="4" fill="%s" stroke="%s" stroke-width="2.5"/>' % (INK, INK))
    for i,w in enumerate((104, 76, 118, 60)):
        p.append('<rect x="234" y="%d" width="%d" height="6" rx="3" fill="%s" opacity=".5"/>' % (72+i*22, w, PAPER))
    # the phone
    p.append('<rect x="48" y="44" width="148" height="238" rx="18" fill="%s" stroke="%s" stroke-width="2.5"/>' % (INK, INK))
    p.append('<rect x="58" y="66" width="128" height="192" rx="6" fill="%s"/>' % PAPER)
    p.append('<rect x="98" y="52" width="48" height="7" rx="3.5" fill="%s" opacity=".55"/>' % PAPER)
    # the tutor speaks first
    p.append('<circle cx="76" cy="88" r="11" fill="%s" stroke="%s" stroke-width="2"/>' % (LAV, INK))
    p.append('<text x="76" y="92" %s font-size="8" fill="%s" text-anchor="middle">AI</text>' % (MONO, INK))
    p.append('<path d="M92 78 h84 a5 5 0 0 1 5 5 v30 a5 5 0 0 1-5 5 h-84 a5 5 0 0 1-5-5 V83 a5 5 0 0 1 5-5 z" fill="%s" stroke="%s" stroke-width="2"/>' % (LIME, INK))
    for i,w in enumerate((66, 52)):
        p.append('<rect x="96" y="%d" width="%d" height="5" rx="2.5" fill="%s" opacity=".62"/>' % (88+i*13, w, INK))
    # the learner answers
    p.append('<path d="M84 136 h84 a5 5 0 0 1 5 5 v24 a5 5 0 0 1-5 5 h-84 a5 5 0 0 1-5-5 v-24 a5 5 0 0 1 5-5 z" fill="%s" fill-opacity=".45" stroke="%s" stroke-width="2"/>' % (BLUE, INK))
    p.append('<rect x="92" y="146" width="56" height="5" rx="2.5" fill="%s" opacity=".62"/>' % INK)
    p.append('<rect x="92" y="157" width="38" height="5" rx="2.5" fill="%s" opacity=".62"/>' % INK)
    # and back again
    p.append('<path d="M92 182 h84 a5 5 0 0 1 5 5 v22 a5 5 0 0 1-5 5 h-84 a5 5 0 0 1-5-5 v-22 a5 5 0 0 1 5-5 z" fill="%s" stroke="%s" stroke-width="2"/>' % (LIME, INK))
    p.append('<rect x="100" y="192" width="64" height="5" rx="2.5" fill="%s" opacity=".62"/>' % INK)
    # the languages it will take
    langs=[('HAUSA',True),('YOR&#217;B&#193;',False),('IGBO',False)]
    for i,(nm,on) in enumerate(langs):
        x=62+i*44
        p.append('<rect x="%d" y="226" width="40" height="18" rx="9" fill="%s" stroke="%s" stroke-width="2"/>' % (x, CORAL if on else PAPER, INK))
        p.append('<text x="%d" y="239" %s font-size="6.5" letter-spacing=".5" fill="%s" text-anchor="middle">%s</text>' % (x+20, MONO, INK, nm))
    # a learner beside it
    p.append('<circle cx="286" cy="204" r="20" fill="%s" stroke="%s" stroke-width="2.5"/>' % (CORAL, INK))
    p.append('<path d="M250 286 C 250 240, 322 240, 322 286" fill="none" stroke="%s" stroke-width="2.5"/>' % INK)
    p.append('<path d="M232 202 C 244 196, 250 198, 262 202" fill="none" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % INK)
    return _wrap('\n'.join(p), 'A phone showing a tutoring conversation: an AI avatar asks a question, the learner replies, the tutor answers again, with language chips for Hausa, Yoruba and Igbo underneath. A blackboard and a student stand behind it.')

FIGURES={'retrieval':fig_retrieval,'diversity':fig_diversity,'repeat':fig_repeat,'earnings':fig_earnings,'triage':fig_triage,'autoglass':fig_autoglass,'doorhandover':fig_doorhandover,'remote':fig_remote,'coding':fig_coding,'crowdfund':fig_crowdfund,'hiring':fig_hiring,'edubot':fig_edubot}

if __name__=='__main__':
    import io,os
    out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'figures_preview.html')
    b=['<style>body{background:#F6F4F9;font-family:system-ui;margin:0;padding:18px;display:grid;grid-template-columns:repeat(2,1fr);gap:16px}div{border:2px solid #1E102F;background:#fff}svg{display:block;width:100%;height:auto}h3{margin:0;padding:7px 11px;background:#1E102F;color:#F6F4F9;font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-family:monospace}</style>']
    for k,fn in FIGURES.items(): b.append('<div><h3>%s</h3>%s</div>'%(k,fn()))
    io.open(out,'w',encoding='utf-8').write('\n'.join(b)); print('wrote',out)
