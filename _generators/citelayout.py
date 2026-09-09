# -*- coding: utf-8 -*-
"""
Force-directed layout for the citation sky.

The graph is bipartite: Xinyu Fu's own studies on one side, the works they cite on
the other, with an edge wherever a study cites a work. Nothing here is hand-placed.
Two studies end up near each other because they actually draw on the same literature
(bibliographic coupling); a cited work sits between the studies that cite it, or in
the halo of the single study that does.

Deterministic: seeded RNG, fixed iteration count. Same input, same sky.
"""
import json, math, os, hashlib
import numpy as np

W, H = 2000.0, 1280.0          # world box the page pans over
SEED = 20260909

# ---- force constants (tuned against the real graph, see build_citesky.py) ----
ITERS       = 600
K_SPRING    = 0.0075   # study -> cited work
L_REST      = 105.0    # preferred edge length
K_REPEL     = 2600.0   # generic node-node repulsion
K_REPEL_PP  = 90000.0  # study-study repulsion: keep the constellations apart
GRAVITY     = 0.00055
DAMPING     = 0.90
MAX_STEP    = 26.0
CELL        = 150.0    # spatial hash cell for the repulsion neighbourhood


def _rng():
    return np.random.default_rng(SEED)


def _hash_angle(key):
    h = hashlib.sha256(key.encode('utf8')).digest()
    return (int.from_bytes(h[:4], 'big') / 0xFFFFFFFF) * 2 * math.pi


def layout(studies, works):
    """
    studies: [{'id':..., ...}]                     — her own papers, in order
    works:   [{'key':..., 'cited_by':[study ids]}] — the literature

    Returns (study_xy, work_xy) as dicts id/key -> (x, y), plus the coupling edges.
    """
    sid = [s['id'] for s in studies]
    sidx = {s: i for i, s in enumerate(sid)}
    ns = len(sid)

    # only keep works that cite at least one study we know about
    works = [w for w in works if any(c in sidx for c in w['cited_by'])]
    nw = len(works)
    n = ns + nw

    rng = _rng()

    # ---- initial placement -------------------------------------------------
    pos = np.zeros((n, 2))
    for i in range(ns):                       # studies on a ring
        a = 2 * math.pi * i / max(1, ns)
        pos[i] = [W / 2 + 380 * math.cos(a), H / 2 + 250 * math.sin(a)]
    for j, w in enumerate(works):              # works near their citers
        cs = [sidx[c] for c in w['cited_by'] if c in sidx]
        c = pos[cs].mean(axis=0)
        a = _hash_angle(w['key'])
        r = 70 + 110 * rng.random()
        pos[ns + j] = c + [r * math.cos(a), r * math.sin(a)]

    # ---- edges -------------------------------------------------------------
    ea, eb = [], []
    for j, w in enumerate(works):
        for c in w['cited_by']:
            if c in sidx:
                ea.append(sidx[c]); eb.append(ns + j)
    ea = np.array(ea, dtype=np.int32)
    eb = np.array(eb, dtype=np.int32)

    mass = np.ones(n)
    mass[:ns] = 9.0                            # studies are heavy, works orbit them

    vel = np.zeros((n, 2))
    centre = np.array([W / 2, H / 2])

    for it in range(ITERS):
        force = np.zeros((n, 2))

        # springs: study -> cited work
        d = pos[eb] - pos[ea]
        dist = np.maximum(np.linalg.norm(d, axis=1), 1e-6)
        f = (K_SPRING * (dist - L_REST) / dist)[:, None] * d
        np.add.at(force, ea, f)
        np.add.at(force, eb, -f)

        # repulsion, restricted to a spatial neighbourhood so it stays near-linear
        keys = np.floor(pos / CELL).astype(np.int64)
        buckets = {}
        for i in range(n):
            buckets.setdefault((keys[i, 0], keys[i, 1]), []).append(i)
        for (cx, cy), idxs in buckets.items():
            near = []
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    near.extend(buckets.get((cx + dx, cy + dy), ()))
            if len(near) < 2:
                continue
            a_ = np.asarray(idxs)
            b_ = np.asarray(near)
            dd = pos[a_][:, None, :] - pos[b_][None, :, :]        # (A, B, 2)
            r2 = np.maximum((dd ** 2).sum(axis=2), 36.0)          # (A, B)
            mag = K_REPEL / r2
            mag[a_[:, None] == b_[None, :]] = 0.0                 # skip self-pairs
            contrib = (mag[:, :, None] * dd / np.sqrt(r2)[:, :, None]).sum(axis=1)
            np.add.at(force, a_, contrib)

        # studies push each other apart hard, at any distance
        dp = pos[:ns][:, None, :] - pos[:ns][None, :, :]          # (ns, ns, 2)
        r2p = np.maximum((dp ** 2).sum(axis=2), 400.0)
        np.fill_diagonal(r2p, np.inf)
        force[:ns] += ((K_REPEL_PP / r2p)[:, :, None] * dp / np.sqrt(r2p)[:, :, None]).sum(axis=1)

        # gentle pull to centre so the sky does not drift apart
        force -= GRAVITY * (pos - centre) * mass[:, None]

        vel = (vel + force / mass[:, None]) * DAMPING
        step = np.linalg.norm(vel, axis=1)
        over = step > MAX_STEP
        vel[over] *= (MAX_STEP / step[over])[:, None]
        pos += vel

    # ---- fit the world box to the cloud, uniform scale in both axes --------
    # Scaling x and y independently would make on-screen distance stop meaning
    # "shares references with", which is the whole point. So: one scale factor,
    # and the box takes whatever aspect the cloud actually has (widened to a
    # minimum so a landscape viewport is not mostly empty).
    lo, hi = pos.min(axis=0), pos.max(axis=0)
    span = np.maximum(hi - lo, 1.0)
    m = 80.0
    scale = min((W - 2 * m) / span[0], (H - 2 * m) / span[1])
    pos = (pos - lo) * scale + m

    ext = span * scale
    box_w, box_h = float(ext[0]) + 2 * m, float(ext[1]) + 2 * m
    if box_w / box_h < 1.5:                     # pad sideways, don't stretch
        box_w = box_h * 1.5
        pos[:, 0] += (box_w - (ext[0] + 2 * m)) / 2.0

    study_xy = {sid[i]: (round(float(pos[i, 0]), 1), round(float(pos[i, 1]), 1))
                for i in range(ns)}
    work_xy = {works[j]['key']: (round(float(pos[ns + j, 0]), 1),
                                 round(float(pos[ns + j, 1]), 1))
               for j in range(nw)}
    return study_xy, work_xy, works, (round(box_w), round(box_h))


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
