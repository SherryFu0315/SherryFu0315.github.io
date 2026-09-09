# -*- coding: utf-8 -*-
"""A real constellation per cell. Points are normalised inside the cell box and
listed brightest-first, so the most settled project takes the brightest star.
Empty points stay as grey slots — the sky has room to grow."""

CONSTELLATIONS = {
 ('llm','intervention'): dict(
   name='Ursa Major',
   pts=[(0.16,0.30),(0.19,0.55),(0.40,0.62),(0.43,0.40),(0.62,0.33),(0.80,0.28),(0.96,0.19)],
   links=[(0,1),(1,2),(2,3),(3,0),(3,4),(4,5),(5,6)]),

 ('agentic','intervention'): dict(
   name='Cassiopeia',
   pts=[(0.10,0.32),(0.31,0.64),(0.52,0.34),(0.73,0.68),(0.93,0.26)],
   links=[(0,1),(1,2),(2,3),(3,4)]),

 ('embodied','intervention'): dict(
   name='Orion',
   pts=[(0.20,0.16),(0.74,0.12),(0.40,0.48),(0.50,0.52),(0.60,0.56),(0.26,0.88),(0.80,0.84)],
   links=[(0,2),(1,4),(2,3),(3,4),(2,5),(4,6)]),

 ('llm','observational'): dict(
   name='Lyra',
   pts=[(0.28,0.14),(0.20,0.54),(0.46,0.64),(0.54,0.36),(0.34,0.34)],
   links=[(0,4),(4,3),(3,2),(2,1),(1,4)]),

 ('agentic','observational'): dict(
   name='Corvus',
   pts=[(0.20,0.26),(0.64,0.20),(0.72,0.66),(0.30,0.64),(0.10,0.78)],
   links=[(0,1),(1,2),(2,3),(3,0),(3,4)]),

 ('embodied','observational'): dict(
   name='Crux',
   pts=[(0.46,0.14),(0.50,0.88),(0.80,0.48),(0.18,0.44),(0.62,0.62)],
   links=[(0,1),(3,2)]),
}

# where each cell sits in the 1000 x 640 world
CELLBOX = {
 ('llm','intervention'):        (244,  92, 200, 214),
 ('agentic','intervention'):    (480,  92, 200, 214),
 ('embodied','intervention'):   (716,  92, 200, 214),
 ('llm','observational'):       (244, 348, 200, 214),
 ('agentic','observational'):   (480, 348, 200, 214),
 ('embodied','observational'):  (716, 348, 200, 214),
}
