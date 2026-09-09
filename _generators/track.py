# -*- coding: utf-8 -*-
"""Apply word-level tracked changes (w:ins / w:del) to a .docx paragraph by paragraph."""
import re, html, difflib

AUTHOR = "Claude"
DATE   = "2026-09-09T00:00:00Z"

PARA_RE = re.compile(r'<w:p(?:\s[^>]*)?>.*?</w:p>|<w:p(?:\s[^>]*)?/>', re.S)
RUN_RE  = re.compile(r'<w:r(?:\s[^>]*)?>.*?</w:r>', re.S)
RPR_RE  = re.compile(r'<w:rPr>.*?</w:rPr>', re.S)
TXT_RE  = re.compile(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>|<w:tab\s*/>|<w:br\s*/>', re.S)
PPR_RE  = re.compile(r'<w:pPr>.*?</w:pPr>', re.S)

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

class Doc:
    def __init__(self, path):
        self.path = path
        self.xml  = open(path, encoding='utf8').read()
        self._id  = 9000

    def nid(self):
        self._id += 1
        return self._id

    def paras(self):
        return list(PARA_RE.finditer(self.xml))

    @staticmethod
    def runs_of(para):
        """-> (list of (rPr, text), start_off, end_off, between_junk)"""
        rs = list(RUN_RE.finditer(para))
        if not rs:
            return [], None, None, ''
        segs = []
        for m in rs:
            r = m.group(0)
            pr = RPR_RE.search(r)
            pr = pr.group(0) if pr else ''
            t = ''
            for tm in TXT_RE.finditer(r):
                if tm.group(0).startswith('<w:tab'):   t += '\t'
                elif tm.group(0).startswith('<w:br'):  t += '\n'
                else:                                  t += html.unescape(tm.group(1))
            segs.append((pr, t))
        a, b = rs[0].start(), rs[-1].end()
        junk = ''.join(para[rs[i].end():rs[i+1].start()] for i in range(len(rs)-1))
        return segs, a, b, junk

    @staticmethod
    def text_of(para):
        segs, *_ = Doc.runs_of(para)
        return ''.join(t for _, t in segs)

    def find(self, anchor):
        """Return the match object of the single paragraph whose text contains anchor."""
        hits = [m for m in self.paras() if anchor in self.text_of(m.group(0))]
        if len(hits) != 1:
            raise SystemExit("anchor %r matched %d paragraphs" % (anchor, len(hits)))
        return hits[0]

    # ---------- emit helpers ----------
    def _run(self, pr, txt):
        return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (pr, esc(txt))

    def _del(self, pr, txt):
        return ('<w:del w:id="%d" w:author="%s" w:date="%s"><w:r>%s'
                '<w:delText xml:space="preserve">%s</w:delText></w:r></w:del>'
                % (self.nid(), AUTHOR, DATE, pr, esc(txt)))

    def _ins(self, pr, txt):
        return ('<w:ins w:id="%d" w:author="%s" w:date="%s"><w:r>%s'
                '<w:t xml:space="preserve">%s</w:t></w:r></w:ins>'
                % (self.nid(), AUTHOR, DATE, pr, esc(txt)))

    # ---------- public API ----------
    def edit(self, anchor, *pairs, **kw):
        """Apply (old, new) replacements inside one paragraph, as one tracked diff."""
        if len(pairs) == 2 and isinstance(pairs[0], str):
            pairs = [(pairs[0], pairs[1])]
        m = self.find(anchor)
        para = m.group(0)
        segs, a, b, junk = self.runs_of(para)
        if junk.strip() and not re.fullmatch(r'(?:<w:proofErr[^>]*/>|<w:lastRenderedPageBreak/>|\s)*', junk):
            raise SystemExit("unexpected inter-run content in %r: %r" % (anchor, junk[:200]))
        full = newfull = ''.join(t for _, t in segs)
        for old, rep in pairs:
            n = newfull.count(old)
            if n != 1:
                raise SystemExit("old %r appears %d times in %r" % (old, n, full[:160]))
            newfull = newfull.replace(old, rep)
        return self._retext(m, para, segs, a, b, full, newfull, block=kw.get('block', False))

    def retext(self, anchor, newfull, block=False):
        m = self.find(anchor)
        para = m.group(0)
        segs, a, b, junk = self.runs_of(para)
        full = ''.join(t for _, t in segs)
        return self._retext(m, para, segs, a, b, full, newfull, block=block)

    TOK = re.compile(r'\s+|\S+')

    @classmethod
    def _tok(cls, t):
        return cls.TOK.findall(t)

    @staticmethod
    def _coalesce(ops, toks_a, toks_b, min_keep=3):
        """Merge change blocks separated by a trivially short 'equal' run, so a
        rewritten phrase reads as one deletion + one insertion, not a word salad."""
        out = list(ops)
        changed = True
        while changed:
            changed = False
            for i in range(1, len(out) - 1):
                tag, i1, i2, j1, j2 = out[i]
                if tag != 'equal':
                    continue
                span = ''.join(toks_a[i1:i2])
                if out[i-1][0] == 'equal' or out[i+1][0] == 'equal':
                    continue
                if len(span.strip()) and (i2 - i1 <= min_keep) and len(span.strip()) <= 12:
                    p_, q_ = out[i-1], out[i+1]
                    out[i-1:i+2] = [('replace', p_[1], q_[2], p_[3], q_[4])]
                    changed = True
                    break
        return out

    def _retext(self, m, para, segs, a, b, full, newfull, block=False):
        prmap = []
        for pr, t in segs:
            prmap.extend([pr] * len(t))

        def prat(i):
            if not prmap: return ''
            return prmap[max(0, min(i, len(prmap) - 1))]

        out = []
        if block:
            ops = [('replace', 0, len(full), 0, len(newfull))]
            A = list(full); B = list(newfull)
            charmode = True
        else:
            A, B = self._tok(full), self._tok(newfull)
            sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
            ops = self._coalesce(sm.get_opcodes(), A, B)
            charmode = False

        # token index -> char offset in `full`
        off, starts = 0, []
        for t in A:
            starts.append(off); off += len(t) if not charmode else 1
        starts.append(off)

        for tag, i1, i2, j1, j2 in ops:
            atxt = ''.join(A[i1:i2]); btxt = ''.join(B[j1:j2])
            c1 = starts[i1] if i1 < len(starts) else len(full)
            if tag == 'equal':
                for pr, chunk in self._bypr(atxt, prmap, c1):
                    out.append(self._run(pr, chunk))
            elif tag == 'delete':
                for pr, chunk in self._bypr(atxt, prmap, c1):
                    out.append(self._del(pr, chunk))
            elif tag == 'insert':
                out.append(self._ins(prat(c1 - 1), btxt))
            else:
                for pr, chunk in self._bypr(atxt, prmap, c1):
                    out.append(self._del(pr, chunk))
                out.append(self._ins(prat(c1), btxt))

        newpara = para[:a] + ''.join(out) + para[b:]
        self.xml = self.xml[:m.start()] + newpara + self.xml[m.end():]
        return self

    @staticmethod
    def _bypr(text, prmap, off):
        """Split `text` into runs of identical rPr, preserving formatting."""
        if not text: return []
        res, cur, curpr = [], '', (prmap[off] if off < len(prmap) else '')
        for k, ch in enumerate(text):
            pr = prmap[off + k] if off + k < len(prmap) else curpr
            if pr != curpr and cur:
                res.append((curpr, cur)); cur, curpr = '', pr
            curpr = pr; cur += ch
        if cur: res.append((curpr, cur))
        return res

    def insert_para_before(self, anchor, text, model=None):
        return self._insert_para(anchor, text, model, before=True)

    def insert_para_after(self, anchor, text, model=None):
        return self._insert_para(anchor, text, model, before=False)

    def _insert_para(self, anchor, text, model=None, before=False):
        """Insert a wholly new, tracked paragraph beside the anchor paragraph."""
        m = self.find(anchor)
        src = self.find(model).group(0) if model else m.group(0)
        ppr = PPR_RE.search(src)
        ppr = ppr.group(0) if ppr else '<w:pPr/>'
        # mark the paragraph mark itself as inserted
        insmark = '<w:rPr><w:ins w:id="%d" w:author="%s" w:date="%s"/></w:rPr>' % (
            self.nid(), AUTHOR, DATE)
        if '<w:rPr>' in ppr:
            ppr = ppr.replace('<w:rPr>', '<w:rPr><w:ins w:id="%d" w:author="%s" w:date="%s"/>' % (
                self.nid(), AUTHOR, DATE), 1)
        else:
            ppr = ppr.replace('</w:pPr>', insmark + '</w:pPr>')
        segs, *_ = self.runs_of(src)
        pr = segs[0][0] if segs else ''
        p = '<w:p>%s%s</w:p>' % (ppr, self._ins(pr, text))
        at = m.start() if before else m.end()
        self.xml = self.xml[:at] + p + self.xml[at:]
        return self

    def save(self, src_docx, out_docx):
        import zipfile, shutil
        zin = zipfile.ZipFile(src_docx)
        zout = zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED)
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename == 'word/document.xml':
                data = self.xml.encode('utf8')
            zout.writestr(it, data)
        zout.close()
