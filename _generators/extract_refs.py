# -*- coding: utf-8 -*-
"""Pull the reference list out of each manuscript into refs_raw/<id>.txt."""
import os, re, sys, subprocess, json

SP  = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SP, 'refs_raw')
os.makedirs(OUT, exist_ok=True)
H = os.path.expanduser('~')

SOURCES = [
 ('retrieval',     H+'/Downloads/[External] RE_ [External]Resubmission of 12942-R2/JMIS-12942-Final-Manuscript.docx'),
 ('errors',        H+'/Downloads/DetectAIErrors_DSS 3/01-DetectAIErrors-Manuscript-DSS.docx'),
 ('secd',          H+'/Library/CloudStorage/OneDrive-GeorgiaStateUniversity/ECM-MISQ/Epistemic Convergence Clean.docx'),
 ('creativity',    H+'/Downloads/Authenticity project/Try1-JMIS/Crowdfunding-AIdisclosure-20260614.docx'),
 ('manufacturing', H+'/Downloads/EmbodiedAI-20260701 LM.docx'),
 ('sales',         H+'/Downloads/AISales-paper-20260905.docx'),
 ('stimulus',      H+'/Downloads/02_GSS_Manuscript_0907.docx'),
 ('service',       H+'/Downloads/OneDrive_1_8-24-2026/Service robot_Manuscript_Sub.docx'),
 ('investment',    H+'/Downloads/Managerial Investment Expectations and Corporate Investment.docx'),
 ('triage',        H+'/Downloads/AITriage/AI_Triage_FullManuscript_MISQ_Updated.docx'),
 ('misaligned',    H+'/Downloads/Aligned Social Signals/CostOfConformity_MISQ_v5_tracked.docx'),
 ('remote',        H+'/Library/CloudStorage/Dropbox-GSUDropbox/Xinyu Fu/share_with_Xinyu/Paper_MSOM/Submission/Remote_work_Manusript_Sub.docx'),
]

HEAD = re.compile(r'^\W{0,4}(references|reference list|bibliography|works cited)\W{0,4}$', re.I)
# a reference line has a year somewhere and is reasonably long
YEAR = re.compile(r'\b(1[89]|20)\d\d[a-z]?\b')
STOP = re.compile(r'^\W{0,4}(appendix|online appendix|supplement\w*|table \d|figure \d|web appendix)\b', re.I)

def paras(path):
    r = subprocess.run(['/usr/bin/python3', SP + '/dtxt.py', path], capture_output=True, text=True)
    return [l.rstrip() for l in r.stdout.split('\n')]

def grab(path):
    ps = paras(path)
    title = next((l.strip() for l in ps if l.strip()), '')
    heads = [i for i, l in enumerate(ps) if HEAD.match(l.strip())]
    if not heads:
        return title, [], 'NO REFERENCES HEADING'
    # choose the heading followed by the most reference-like lines
    best, bestn = None, -1
    for h in heads:
        n = sum(1 for l in ps[h+1:h+400] if len(l.strip()) > 40 and YEAR.search(l))
        if n > bestn: best, bestn = h, n
    refs, buf = [], ''
    for l in ps[best+1:]:
        t = l.strip()
        if STOP.match(t):
            break
        if not t:
            continue
        if len(t) < 40 and not YEAR.search(t):
            # likely a stray heading or page artefact; flush and skip
            continue
        refs.append(t)
    # keep only lines that carry a year (drops running heads, page numbers)
    refs = [r for r in refs if YEAR.search(r) and len(r) > 40]
    return title, refs, ''

manifest = {}
for pid, path in SOURCES:
    if not os.path.exists(path):
        print('%-14s MISSING  %s' % (pid, path)); continue
    title, refs, err = grab(path)
    manifest[pid] = dict(file=path, title=title, n=len(refs))
    with open(os.path.join(OUT, pid + '.txt'), 'w', encoding='utf8') as f:
        f.write('\n'.join(refs))
    print('%-14s %4d refs  %s%s' % (pid, len(refs), err and '['+err+'] ' or '', title[:80]))
json.dump(manifest, open(os.path.join(OUT, '_manifest.json'), 'w'), indent=1)
