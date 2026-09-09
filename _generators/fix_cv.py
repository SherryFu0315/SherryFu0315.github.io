# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from track import Doc

SP  = os.path.dirname(os.path.abspath(__file__))
SRC = "/Users/xinyufu/Downloads/Internal Grant/CV_Xinyu FU_August2026.docx"
d   = Doc(SP + "/cvx/word/document.xml")
E   = d.edit

# ============ header & education ============
E('Professional Expereince', 'Professional Expereince', 'Professional Experience')
E('55 Park Place, 1727', '55 Park Place, 1727', '55 Park Place NE, Suite 1727')
while True:                      # re-find each time: _retext shifts every later offset
    hits = [q for q in d.paras() if 'Georgia State Univeristy' in Doc.text_of(q.group(0))]
    if not hits: break
    m = hits[0]; para = m.group(0); segs, a, b, _ = Doc.runs_of(para)
    full = ''.join(t for _, t in segs)
    d._retext(m, para, segs, a, b, full, full.replace('Univeristy', 'University'))
E('Ph.D., Management of Information Systems',
  'Ph.D., Management of Information Systems', 'Ph.D., Management Information Systems')

# ============ Journal / Book Publications ============
# JMIS 12942 was accepted 31 Aug 2026 under its final title.
E('Managing imperfect algorithms',
  ('“Managing imperfect algorithms: Error detection in collaborative human-AI decision making processes.”',
   '“Knowing Is Not Enough: Information Retrievability as a Precondition to Effective LLM Oversight.”'),
  ('Journal of Management of Information Systems (JMIS)',
   'Journal of Management Information Systems (JMIS)'), block=True)

d.retext('Human–AI collaboration in HRM',
  'Fu, X., Nah, F. F.-H., Liu, S., Zhang, K., Huang, Z., Zheng, R., Xie, W., & Yimingjiang, Y. (2026). '
  '“AI in Human Resource Management.” Chapter 14 in V. G. Duffy, W. Karwowski, & G. Salvendy (Eds.), '
  'Advances in Human–AI Collaboration (Wiley ISE Book Series). Wiley. '
  'https://doi.org/10.1002/9781394266401.ch14', block=True)

# ============ Working Papers ============
# MIS Quarterly rejected 2026-RA-20935 on 20 July 2026 (SE decision letter).
E('Reject and Resubmit at Management of Information Systems Quarterly',
  ('”  Reject and Resubmit at Management of Information Systems Quarterly (MISQ)', '” Working paper.'),
  block=True)

E('When Transparency Backfires',
  'Reject and Rebusmit at Journal of Management of Information Systems (JMIS)',
  'Reject and Resubmit at Journal of Management Information Systems (JMIS)')

E('Reinventing Manufacturing',
  'Management of Information Systems Quarterly (MISQ)', 'MIS Quarterly (MISQ)')

E('Managerial Investment Expectations', 'Zheng. S.', 'Zheng, S.')

E('The Privacy Asymmetry of Service Robots: Spatial and Data Privacy Concerns in Boundary-Spanning Service Encounters.” Under first',
  'Maruping, LM.', 'Maruping, L. M.')

E('Impacts of Parallel AI Deployment on Worker Behavior in Outbound Sales', 'Peng, S.', 'Shen, P.')

E('Repeating a Treatment Repeats Its Wording',
  ('Maruping, LM.', 'Maruping, L. M.'),
  ('review at at Information Systems Research', 'review at Information Systems Research'))

# repositioned; the manuscript now carries a different title
E('Misaligned Social Signals and Creative Engagement',
  ('Fu, X., Ramasubbu, N, Janansefat, S.',
   'Fu, X., Ramasubbu, N., Maruping, L. M., Janansefat, S.'),
  ('\u201cMisaligned Social Signals and Creative Engagement in Digital Platforms: A Field Experiment.\u201d',
   '\u201cThe Cost of Conformity: How Social Signal Alignment Backfires on Identity-Expressive '
   'Creative Platforms.\u201d'),
  block=True)

# ============ Conference Proceedings ============
E('AACRIS 2026', 'Rai, Fu., Fu, X., Xia, Y.', 'Rai, A., Fu, X., Xia, Y.')
E('GenAI Model and Knowledge Collapse', 'Rai, Fu., Fu, X., Xia, Y.', 'Rai, A., Fu, X., Xia, Y.')
E('INFOMRS 2025', 'INFOMRS 2025', 'INFORMS 2025')
E('Robotic Agents Impact Customer Online Reviews',
  ('“Robotic Agents Impact Customer Online Reviews. How Robotic Agents Impact Customer Online Reviews”',
   '“How Robotic Agents Impact Customer Online Reviews”'), block=True)
E('The Privacy Asymmetry of Service Robots: Spatial and Data Privacy Concerns in Boundary-Spanning Service Encounters.” CIST',
  'Maruping, LM.', 'Maruping, L. M.')

# ============ Teaching ============
E('Agentic AI (Undergradate), Spring 2026',
  'Agentic AI (Undergradate), Spring 2026, Instructor, GSU',
  'Agentic AI (Undergraduate), Spring 2026, Co-instructor with Dr. Amrita George, GSU')
E('Data Programming (Undergradaute), Fall 2025',
  'Data Programming (Undergradaute), Fall 2025', 'Data Programming (Undergraduate), Fall 2025')
E('Data Programming (Undergradate Elective)',
  'Data Programming (Undergradate Elective)', 'Data Programming (Undergraduate Elective)')
E('Harvard Univeristy', 'Harvard Univeristy', 'Harvard University')
E('Data Program Essentials with Python (MBA and MS Elective), Fall 2019',
  'Data Program Essentials with Python', 'Data Programming Essentials with Python')
E('Advanced Data Program with R', 'Advanced Data Program with R', 'Advanced Data Programming with R')

# ============ Service & Community Service ============
d.retext('Phd Student thesis committee',
  'PhD student dissertation committees: Anqi Zhang (co-chair); Yingxin Zhou (member); '
  'Kartikeya Negi (member); Shaohui Wang (member); Xinyuan Wei (member)', block=True)
E('MIS Quartery', 'MIS Quartery', 'MIS Quarterly')

# ============ new paragraphs ============
d.insert_para_before('Agentic AI (Undergraduate), Spring 2026',
                     'Agentic AI (Undergraduate), Fall 2026, Instructor, GSU')
d.insert_para_after('achieved 1st place at the group level',
  'Faculty advisor for undergraduate research; advisee work presented as “Talk to Me: '
  'A Preliminary Review on the Evolution and Impact of Emotional AI,” AMCIS 2025 TREO.')

out = SP + "/CV_Xinyu FU_September2026_tracked.docx"
d.save(SRC, out)
print("wrote", out)
