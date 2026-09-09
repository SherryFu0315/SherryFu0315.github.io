# -*- coding: utf-8 -*-
"""
Layout for the citation sky.

The graph is bipartite: Xinyu Fu's own studies on one side, the works they cite on
the other, with an edge wherever a study cites a work. Nothing here is hand-placed.

Two stages, because they answer different questions:

  1. The studies are laid out by force simulation over the coupling graph — two
     studies pull together in proportion to how many references they share. This
     is the part where distance carries meaning.

  2. Each cited work is then placed in the halo of the study (or between the
     studies) that cite it, at a hash-seeded angle and radius.

Stage 2 used to be a force simulation too, and it was wrong: uniform pairwise
repulsion run to equilibrium settles into a hexagonal lattice, which reads as
graph paper rather than as a sky. It was also a worse claim — it implied every
reference repels every other, when the only real relation a reference has is to
the paper that cites it.

Deterministic: every offset comes from a hash of the work's key, so the same
input always produces the same sky.
"""
import hashlib
import math

import numpy as np

W, H = 1600.0, 1024.0
SEED = 20260909

# ---- stage 1: the studies -------------------------------------------------
S_ITERS   = 900
S_SPRING  = 0.010      # coupled studies pull together
S_REST    = 210.0      # ... to about this far apart when they share one work
S_REPEL   = 330000.0   # every study pushes every other away
S_GRAVITY = 0.0016
S_DAMP    = 0.86

# ---- stage 2: the halo of literature around each study --------------------
HALO      = 150.0      # radius a study's own references spread over
HALO_MIN  = 0.20       # nothing sits right on top of its study
SHARED_J  = 0.20       # jitter for a work pulled between several studies
DECLUMP   = 40         # relaxation passes to separate coincident points
MIN_GAP   = 5.0        # ... only enough that no two dots sit on top of
                       # each other; push harder and the field turns into a lattice


def _h(key, salt):
    d = hashlib.sha256((salt + '|' + key).encode('utf8')).digest()
    return int.from_bytes(d[:6], 'big') / float(1 << 48)


def _study_positions(sid, pairs):
    n = len(sid)
    idx = {s: i for i, s in enumerate(sid)}
    pos = np.zeros((n, 2))
    for i in range(n):                              # start on a ring
        a = 2 * math.pi * i / max(1, n)
        pos[i] = [W / 2 + 460 * math.cos(a), H / 2 + 310 * math.sin(a)]

    ea, eb, ew = [], [], []
    for (a, b), k in pairs.items():
        if a in idx and b in idx:
            ea.append(idx[a]); eb.append(idx[b]); ew.append(k)
    ea = np.array(ea, dtype=np.int32); eb = np.array(eb, dtype=np.int32)
    ew = np.array(ew, dtype=float) if len(ew) else np.zeros(0)

    vel = np.zeros((n, 2))
    centre = np.array([W / 2, H / 2])
    for _ in range(S_ITERS):
        f = np.zeros((n, 2))
        if len(ea):
            d = pos[eb] - pos[ea]
            dist = np.maximum(np.linalg.norm(d, axis=1), 1e-6)
            # more shared references -> shorter rest length -> closer together
            rest = S_REST / np.sqrt(ew)
            mag = (S_SPRING * ew * (dist - rest) / dist)[:, None] * d
            np.add.at(f, ea, mag)
            np.add.at(f, eb, -mag)
        dp = pos[:, None, :] - pos[None, :, :]
        r2 = np.maximum((dp ** 2).sum(axis=2), 900.0)
        np.fill_diagonal(r2, np.inf)
        f += ((S_REPEL / r2)[:, :, None] * dp / np.sqrt(r2)[:, :, None]).sum(axis=1)
        f -= S_GRAVITY * (pos - centre)
        vel = (vel + f) * S_DAMP
        step = np.linalg.norm(vel, axis=1)
        over = step > 22.0
        if over.any():
            vel[over] *= (22.0 / step[over])[:, None]
        pos += vel
    return pos


def layout(studies, works, box=None):
    """
    studies: [{'id':..., ...}]
    works:   [{'key':..., 'cited_by':[study ids]}]
    box:     (w, h) to normalise into.

    Returns (study_xy, work_xy, kept_works, (box_w, box_h)).
    """
    BW, BH = box if box else (W, H)
    sid = [s['id'] for s in studies]
    idx = {s: i for i, s in enumerate(sid)}
    works = [w for w in works if any(c in idx for c in w['cited_by'])]

    pairs = coupling(studies, works)
    spos = _study_positions(sid, pairs)

    # ---- stage 2: hang each work off the study or studies that cite it ----
    wpos = np.zeros((len(works), 2))
    for j, w in enumerate(works):
        cs = [idx[c] for c in w['cited_by'] if c in idx]
        base = spos[cs].mean(axis=0)
        ang = _h(w['key'], 'a') * 2 * math.pi
        if len(cs) == 1:
            # sqrt keeps the disc evenly filled; the exponent pulls it inward so
            # the halo has a dense core and a thin edge, the way a cluster looks
            u = HALO_MIN + (1 - HALO_MIN) * _h(w['key'], 'r')
            rad = HALO * (u ** 0.62)
        else:
            # a shared work belongs to the space between its citers, not to a halo
            rad = HALO * 0.30 * _h(w['key'], 'r')
        wpos[j] = base + [rad * math.cos(ang), rad * math.sin(ang) * 0.88]

    # ---- fit into the frame, one uniform scale so distance keeps meaning ----
    allp = np.vstack([spos, wpos])
    lo, hi = allp.min(axis=0), allp.max(axis=0)
    span = np.maximum(hi - lo, 1.0)
    m = 0.05 * min(BW, BH) + 20.0
    scale = min((BW - 2 * m) / span[0], (BH - 2 * m) / span[1])
    allp = (allp - lo) * scale
    allp[:, 0] += (BW - span[0] * scale) / 2.0
    allp[:, 1] += (BH - span[1] * scale) / 2.0

    # ---- separate coincident points, in final units --------------------
    # This has to come after the fit: MIN_GAP is a distance on the finished
    # map, and declumping before scaling just shrinks the gap away again.
    ns = len(sid)
    wp = allp[ns:]
    for _ in range(DECLUMP):
        moved = False
        cell = MIN_GAP * 2.0
        buckets = {}
        for j in range(len(wp)):
            buckets.setdefault((int(wp[j, 0] // cell), int(wp[j, 1] // cell)), []).append(j)
        for (cx, cy), ids in buckets.items():
            near = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    near.extend(buckets.get((cx + dx, cy + dy), ()))
            if len(near) < 2:
                continue
            a_ = np.asarray(ids); b_ = np.asarray(near)
            dd = wp[a_][:, None, :] - wp[b_][None, :, :]
            r = np.sqrt(np.maximum((dd ** 2).sum(axis=2), 1e-9))
            close = (r < MIN_GAP) & (a_[:, None] != b_[None, :])
            if not close.any():
                continue
            moved = True
            push = np.where(close[:, :, None],
                            dd / r[:, :, None] * (MIN_GAP - r)[:, :, None] * 0.5, 0.0)
            np.add.at(wp, a_, push.sum(axis=1))
        if not moved:
            break
    allp[ns:] = wp

    study_xy = {sid[i]: (round(float(allp[i, 0]), 1), round(float(allp[i, 1]), 1))
                for i in range(ns)}
    work_xy = {works[j]['key']: (round(float(allp[ns + j, 0]), 1),
                                 round(float(allp[ns + j, 1]), 1))
               for j in range(len(works))}
    return study_xy, work_xy, works, (BW, BH)


def coupling(studies, works):
    """Shared-reference counts between every pair of studies."""
    sid = {s['id'] for s in studies}
    pairs = {}
    for w in works:
        cs = sorted(c for c in w['cited_by'] if c in sid)
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                k = (cs[i], cs[j])
                pairs[k] = pairs.get(k, 0) + 1
    return pairs
