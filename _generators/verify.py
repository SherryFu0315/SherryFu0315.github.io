import sys, zipfile, re, html
import xml.etree.ElementTree as ET
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
path=sys.argv[1]; mode=sys.argv[2]   # accept | reject
x=zipfile.ZipFile(path).read('word/document.xml')
root=ET.fromstring(x)               # also validates well-formedness
body=root.find(W+'body')
out=[]
def para_text(p):
    res=[]
    def walk(el, in_del=False, in_ins=False):
        for ch in el:
            if ch.tag==W+'del':   walk(ch, True, in_ins)
            elif ch.tag==W+'ins': walk(ch, in_del, True)
            elif ch.tag==W+'r':
                if in_del and mode=='accept': continue
                if in_ins and mode=='reject': continue
                for t in ch:
                    if t.tag in (W+'t', W+'delText'): res.append(t.text or '')
                    elif t.tag==W+'tab': res.append('\t')
            elif ch.tag==W+'hyperlink': walk(ch, in_del, in_ins)
    walk(p)
    return ''.join(res)
def emit(el):
    for ch in el:
        if ch.tag==W+'p':
            # a paragraph whose mark is an insertion disappears on reject
            ppr=ch.find(W+'pPr')
            newpara = ppr is not None and ppr.find(W+'rPr') is not None and ppr.find(W+'rPr').find(W+'ins') is not None
            t=para_text(ch)
            if mode=='reject' and newpara: continue
            out.append(t)
        elif ch.tag in (W+'tbl',W+'tr',W+'tc',W+'sdt',W+'sdtContent'): emit(ch)
emit(body)
for line in out:
    if line.strip(): print(line)
