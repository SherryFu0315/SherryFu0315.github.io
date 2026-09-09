import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subprocess
def paras(path):
    out = subprocess.run(['/usr/bin/python3', os.path.dirname(os.path.abspath(__file__))+'/dtxt.py', path],
                         capture_output=True, text=True).stdout
    return [l.strip() for l in out.split('\n')]
HEAD = re.compile(r'^(references|reference list|bibliography|works cited)\s*$', re.I)
YEAR = re.compile(r'\((19|20)\d\d[a-z]?\)|\b(19|20)\d\d[a-z]?\.')
def refs(path):
    ps = paras(path)
    idx = [i for i,l in enumerate(ps) if HEAD.match(l)]
    if not idx: return []
    start = idx[-1]
    out = []
    for l in ps[start+1:]:
        if len(l) < 25: continue
        if YEAR.search(l): out.append(l)
    return out
if __name__ == '__main__':
    for f in sys.argv[1:]:
        r = refs(f)
        print('%4d  %s' % (len(r), os.path.basename(f)))
        for x in r[:2]: print('        ', x[:150])
