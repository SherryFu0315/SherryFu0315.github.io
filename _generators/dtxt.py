import sys, zipfile, re, html
z=zipfile.ZipFile(sys.argv[1])
x=z.read('word/document.xml').decode('utf8')
x=re.sub(r'<w:p[ >]', '\n<w:p ', x)
x=re.sub(r'<w:tab/>','\t',x)
x=re.sub(r'<w:br/>',' | ',x)
x=re.sub(r'<[^>]+>','',x)
for line in x.split('\n'):
    line=html.unescape(line).strip()
    if line: print(line)
