# -*- coding: utf-8 -*-
"""One source of truth. Two axes, straight from her own table:
   columns  = what kind of AI the study is about
   rows     = intervention-oriented, or observational."""

COLS = [
  dict(id='llm',      name='LLM / MLLM',  sub='Language and multimodal models', c='#8FA6FF'),
  dict(id='agentic',  name='Agentic AI',  sub='Models that converse and act',   c='#FF7874'),
  dict(id='embodied', name='Embodied AI', sub='Machines that move among us',    c='#ECB8FF'),
]
ROWS = [
  dict(id='intervention', name='Intervention', sub='Augmenting human capability'),
  dict(id='observational', name='Observational', sub='Consequences of AI at work'),
]

# art is deliberately empty: photographs are coming, and a placeholder would
# only have to be taken out again.
PROJECTS = [
 dict(id='retrieval', col='llm', row='intervention', order=1,
   chip='Forthcoming', venue='Journal of Management Information Systems',
   title='Knowing Is Not Enough: Information Retrievability as a Precondition to Effective LLM Oversight',
   short='Knowing Is Not Enough',
   authors='<b>Fu, X.</b>, Ramasubbu, N., &amp; Galletta, D.',
   method='Two field experiments',
   finding=("Reading the system's own account of why it errs is not enough. People made to "
            "<b>write that explanation themselves</b> caught meaningfully more errors. And the habit wears "
            "off, a little each day, unless something puts the knowledge back within reach."),
   photo=('retrieval.jpg','A hand annotating a printed AI response beside a laptop, marking a claim to check.'),
   metrics=[('+10.6pp','more errors caught writing your own explanation than reading one (N = 400)'),
            ('&minus;2.5pp','detection lost per day of use; &minus;1.7 with a retrieval cue')],
   links=[('Preprint on arXiv','https://arxiv.org/abs/2609.01976'),
          ('Preprint on SSRN','https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7392398')]),

 dict(id='remote', col=None, row=None, order=4,
   chip='Under review', venue='',
   title='Remote Work and Firm Productivity',
   short='Remote Work and Firm Productivity',
   authors='Fan, C., <b>Fu, X.</b>, &amp; Ramasubbu, N.',
   method='Multi-country firm panel',
   finding=("Firms that went remote early and <b>kept it</b> grew sales faster by the third survey round, "
            "about a year on. Going remote late, or going and then retreating, bought nothing. And more remote "
            "was not better &mdash; performance rose with the remote share up to a point, then fell."),
   photo=('remote.jpg','An empty boardroom at dusk, a conference speakerphone on the table and a city skyline beyond the glass.'),
   metrics=[('+7.8pp','faster sales growth for early, persistent adopters'),
            ('3,199','firms across 19 countries')],
   links=[]),

 dict(id='misaligned', col=None, row=None, order=13,
   chip='In progress', venue='',
   title='The Cost of Conformity: How Social Signal Alignment Backfires on Identity-Expressive Creative Platforms',
   short='The Cost of Conformity',
   authors='<b>Fu, X.</b>, Ramasubbu, N., Maruping, L. M., &amp; Janansefat, S.',
   method='Switchback field experiment, with a pre-registered lab replication',
   finding=("A switchback field experiment on a rap-creation platform, where anything you post carries "
            "your name. The design intuition is that showing people more of what is popular encourages "
            "them to make something. It does the reverse: when the signal from a user&rsquo;s friends and "
            "the signal from the platform <b>agree</b>, recording falls off. Signals that disagree send "
            "browsing and preparation sharply up &mdash; and almost none of it turns into a finished "
            "track. The drop lands hardest on the platform&rsquo;s most active creators, the ones it can "
            "least afford to lose."),
   photo=('misaligned.jpg','A tiled pattern of music-making app icons.'),
   metrics=[], links=[]),

 dict(id='errors', col='llm', row='intervention', order=5,
   chip='Under review', venue='',
   title='Detecting AI Errors: Transfer of Training and Reflective Practice',
   short='Detecting AI Errors',
   authors='<b>Fu, X.</b>, Ramasubbu, N., &amp; Galletta, D.',
   method='Two randomized experiments',
   finding=("A warning that makes you reflect <b>while</b> you work lifts decision quality far above working "
            "with no AI at all. In the field experiment, the same information delivered as an after-the-fact "
            "review left people below the no-AI baseline. When the checking happens matters more than what the "
            "checking says."),
   photo=('errors.jpg','An isometric illustration of people inspecting code on a laptop with a magnifying glass over a flagged defect.'),
   metrics=[('0.90&ndash;0.95','with reflection during the task'),
            ('0.45','with no AI at all'),
            ('0.34','with the review afterwards')],
   links=[]),

 dict(id='secd', col='llm', row='intervention', order=7,
   chip='Working paper', venue='',
   title='Epistemic Calibration Model',
   short='Epistemic Calibration Model',
   authors='Rai, A., <b>Fu, X.</b>, &amp; Xia, Y.',
   method='Computational field study',
   finding=("Ask a room of people the same programming question and you get genuinely different answers. "
            "Ask a model the same question many times and the answers cluster &mdash; and <b>newer models "
            "cluster tighter, not looser</b>. Broadening the prompt, raising the temperature and keeping prior "
            "answers out of the context pull some of the variety back, but nowhere near all of it."),
   photo=('secd.jpg','A lightbulb made up of many small differently coloured figures.'),
   metrics=[('375','Stack Overflow questions, sampled after every training cutoff'),
            ('2.4&ndash;6.8%','of the narrowing those levers recover &mdash; still far more alike than human answers')],
   links=[]),

 dict(id='creativity', col='llm', row='observational', order=6,
   chip='Working paper', venue='',
   title='AI Authenticity: How AI Disclosure and Authenticity Signals Shape Crowdfunding Valuation',
   short='AI Authenticity',
   authors='Yang, J., <b>Fu, X.</b>, Ramasubbu, N., &amp; Fan, C.',
   method='Natural experiment',
   finding=("A platform made AI disclosure mandatory and funding fell across it. Projects that had built "
            "their pitch on human craft were <b>shielded from the general suspicion and punished hardest when "
            "they actually disclosed</b>. Authenticity works as armour right up until the moment it is "
            "contradicted."),
   photo=('creativity.jpg','A woodworker&rsquo;s bench with a hand-turned bowl and shavings, beside a laptop showing the listing for it.'),
   metrics=[('12,521','projects around the disclosure mandate'),
            ('~1 in 10','of those that could disclose actually did')],
   links=[]),

 dict(id='investment', col='llm', row='observational', order=9,
   chip='Under review', venue='',
   title='Managerial Investment Expectations and Real Estate Investment',
   short='Managerial Investment Expectations',
   authors='Bond, S., Devine, A., <b>Fu, X.</b>, &amp; Zheng, S.',
   method='Archival panel',
   finding=("What managers say they expect about the future, read out of what they tell analysts on earnings "
            "calls, and what their firms actually go on to spend."),
   photo=('investment.jpg','A poster reading AI impact on NYC real estate over a stylised Manhattan skyline.'),
   metrics=[], links=[]),

 dict(id='stimulus', col='agentic', row='intervention', order=12,
   chip='Under review', venue='',
   title='Generative Stimulus Sampling: Relational Randomization for Repeated-Exposure Digital Interventions',
   short='Generative Stimulus Sampling',
   authors='<b>Fu, X.</b>, Ramasubbu, N., Maruping, L. M., Wang, G., Xie, J., &amp; Wang, K.',
   method='Full-text census and experiments',
   finding=("Repeat a message and the effect fades &mdash; but is that the intervention wearing off, or "
            "just that one wording? <b>Generative stimulus sampling</b> builds an audited pool of differently "
            "worded versions that all carry the same intervention, then randomises not only which one a person "
            "sees but <b>how far it moves from the one they saw last</b>. The distance between one message and "
            "the next becomes a variable you set, rather than an accident of the materials."),
   photo=('stimulus.jpg','The GSS Research Studio public preview, asking what repeated-message experiment to build.'),
   metrics=[('425','randomized experiments in the census'),
            ('53%','re-expose the same participant to the same stimulus')],
   links=[]),

 dict(id='edubot', col='agentic', row='intervention', order=3,
   chip='Deployed', venue='Student&ndash;faculty project',
   title='EduBot Naija',
   short='EduBot Naija',
   authors='A student&ndash;faculty collaboration supported by Georgia State University',
   method='Deployed system',
   finding=("An AI tutor that teaches the curriculum in local Nigerian languages, built by students for "
            "communities the English-only version of the internet was never going to reach. A collaboration "
            "with <a href=\"https://www.apluscomputertrainingtech.com.ng/\">A+ Computer Training "
            "Technology</a>, who build and run it in Nigeria."),
   photo=('edubot.jpg','Secondary-school students in uniform seated together at the EduBot Naija launch.'),
   metrics=[],
   links=[('ITEdgeNews','https://www.itedgenews.africa/edubot-naija-launches-ai-powered-multilingual-learning-platform-across-nigeria/'),
          ('TechAfrica News','https://techafricanews.com/2025/08/14/a-computer-training-launches-edubot-nigeria-to-deliver-ai-powered-education-in-indigenous-languages/'),
          ('NaijaEyes','https://naijaeyesblog.com/tech/edubot-nigeria-ai-education/'),
          ('Launch video','https://www.youtube.com/watch?v=3TnI3x-V_eQ')]),

 dict(id='sales', col='agentic', row='observational', order=11,
   chip='Under review', venue='',
   title='When Better Opportunities Backfire: Worker Responses to Parallel AI Deployment',
   short='When Better Opportunities Backfire',
   authors='<b>Fu, X.</b>, Luo, S., Ramasubbu, N., Shen, P., Wang, X., &amp; Wang, Y.',
   method='Field quasi-experiment',
   finding=("An insurer handed its cold calls to an AI voice agent, leaving human agents a better set of "
            "leads to work. Their conversion on the day's first calls <b>fell</b>. Expecting something better "
            "next makes the thing in your hand easier to drop: early in the shift agents spent measurably less "
            "time on each promising lead, and were readier to push it back to the shared queue."),
   photo=('sales.jpg','A humanoid AI head in profile beside a woman wearing a call-centre headset, a speech waveform between them.'),
   metrics=[('&minus;4.5pp','fall in conversion on the first calls of the day'),
            ('&minus;13%','less time spent on those early high-intent calls'),
            ('567k','outbound calls around the AI routing change')],
   links=[]),

 dict(id='triage', col='agentic', row='observational', order=14,
   chip='In progress', venue='',
   title='Need Assessment in Online Credence Services: How AI Triage Reshapes Demand Allocation',
   short='AI Triage in Credence Services',
   authors='<b>Fu, X.</b>, Chen, L., Geng, S., Hsieh, J. P. A., Xie, J., &amp; Zhang, W.',
   method='In progress',
   finding=("When customers cannot judge the service they are buying &mdash; a diagnosis, a legal opinion, a "
            "repair &mdash; putting a model at the front door decides who reaches which expert. That routing is "
            "an allocation decision wearing the costume of a convenience feature."),
   photo=('triage.jpg','A phone showing a healthcare chatbot triaging a patient&rsquo;s symptoms, with a robot mascot beside it.'),
   metrics=[], links=[]),

 dict(id='hrm', col='agentic', row='observational', order=2,
   chip='Published', venue='Wiley ISE Book Series',
   title='AI in Human Resource Management',
   short='AI in Human Resource Management',
   authors='<b>Fu, X.</b>, Nah, F. F.-H., Liu, S., Zhang, K., Huang, Z., Zheng, R., Xie, W., &amp; Yimingjiang, Y.',
   method='Book chapter',
   finding=("Chapter 14 of <em>Advances in Human&ndash;AI Collaboration</em>, edited by V. G. Duffy, "
            "W. Karwowski and G. Salvendy (Wiley, 2026, pp. 263&ndash;285), on what changes for the people "
            "doing the work when AI enters hiring, evaluation and development &mdash; and on which parts of "
            "the job it stubbornly should not take over."),
   photo=('hrm.jpg','An isometric illustration titled AI in HR: candidate profiles on screens, a magnifying glass and a chart, being worked through by two people.'),
   metrics=[],
   links=[('Chapter at Wiley','https://onlinelibrary.wiley.com/doi/10.1002/9781394266401.ch14'),
          ('Record at CityU','https://scholars.cityu.edu.hk/en/publications/ai-in-human-resource-management/')]),

 dict(id='manufacturing', col='embodied', row='intervention', order=8,
   chip='Under review', venue='',
   title='Embodied AI and Shop-Floor Workers',
   short='Embodied AI and Shop-Floor Workers',
   authors='<b>Fu, X.</b>, Mathiassen, L., &amp; Ramasubbu, N.',
   method='Revelatory case study',
   finding=("A U.S. auto-glass plant put embodied AI on its shop floor. Workers came out of it describing "
            "their jobs as more meaningful &mdash; and the ones who grew the most, taking on more control "
            "<em>and</em> more responsibility at once, were the <b>least likely to advance</b>. The firm's "
            "advancement criteria had been built for a more divided shop floor, and had no category &mdash; and "
            "no role &mdash; for people whose work now crossed all of them."),
   photo=('manufacturing.jpg','A robotic arm moving a large sheet of flat glass along a conveyor in a bright glass plant.'),
   metrics=[], links=[]),

 dict(id='surgery', col='embodied', row='intervention', order=15,
   chip='In progress', venue='',
   title='Robotic Surgery',
   short='Robotic Surgery',
   authors='Jing, X., <b>Fu, X.</b>, &amp; Liu, S.',
   method='Clinical team study',
   finding=("A surgeon drives the console, but an operating theatre is a team. When a robot joins the "
            "table, the scrub nurse, the anaesthetist and the assistants all have to learn a new set of "
            "cues from one another &mdash; where to stand, when to speak, what a paused arm means. This "
            "project asks how that <b>shared choreography</b> gets learned, and how much of the surgical "
            "outcome rides on the team settling into it rather than on any one person's skill at the "
            "controls."),
   photo=('surgery.jpg','Robotic surgical instruments manipulating small objects on a surgical drape under theatre lights.'),
   emoji='&#129535;',
   metrics=[], links=[]),

 dict(id='service', col='embodied', row='observational', order=10,
   chip='Under review', venue='',
   title='Service Robots in Hospitality: Spatial and Data Privacy in Boundary-Spanning Encounters',
   short='The Privacy Asymmetry of Service Robots',
   authors='Zhang, A., <b>Fu, X.</b>, Maruping, L. M., &amp; Liu, S.',
   method='Field experiment',
   finding=("When a robot rather than a person brings something to a hotel-room door, guests protect two "
            "kinds of privacy in opposite directions at once: they <b>open the door wider and go quiet</b>. "
            "Physical guard drops, informational guard goes up. Any service design that treats &ldquo;privacy&rdquo; "
            "as one dial will get one of them wrong."),
   photo=('service.jpg','A hotel guest in a white robe reaching into the open lid of a delivery robot in a carpeted corridor.'),
   metrics=[('&minus;0.79','spatial guard &mdash; the door opens wider'),
            ('+1.03','informational guard &mdash; the guest says less')],
   links=[]),
]


# Short enough to sit under a star, on the map and on the front page's
# miniature of it. The full title stays in the tooltip. It lives here rather
# than in either builder so the two cannot drift apart.
LABEL = {
    'retrieval': 'LLM oversight',           'errors': 'Detecting AI errors',
    'secd': 'Epistemic calibration',        'creativity': 'AI authenticity',
    'investment': 'Investment expectations','stimulus': 'Stimulus sampling',
    'sales': 'Parallel AI in sales',        'triage': 'AI triage',
    'manufacturing': 'Shop-floor embodied AI', 'service': 'Service robots',
    'misaligned': 'Cost of conformity',     'remote': 'Remote work',
    'hrm': 'AI in HR',                      'edubot': 'EduBot Naija',
    'surgery': 'Robotic surgery',
}

# How large a star is drawn, by how far along the work is.
STAR_SIZE = {'Forthcoming': 3, 'Published': 3, 'Deployed': 3, 'Under review': 2}


# What the front page shows, and in what order. This is an editorial sequence,
# not a date: the accepted paper opens, the study that shares its question
# follows, then the one that got built and deployed, then the wider consequences
# of AI use, then the broader survey, and the adjacent work last. The research
# page keeps its own order (the `order` field), and everything left out is one
# click away under "all projects".
FEATURED = ['retrieval', 'errors', 'edubot', 'creativity', 'hrm', 'remote']


# What each study is called on the front page's cards, and the one line that
# appears when you hover one. Short on purpose: the full title, the authors, the
# method and the numbers are all on the project page, one click away, and the
# card exists to make you want to go there.
#
# Every line below is condensed from that study's own description further up
# this file — nothing here says anything the longer version does not.
CARD = {
    'retrieval':  'Effective LLM oversight',
    'errors':     'Detecting AI errors',
    'edubot':     'EduBot Naija',
    'creativity': 'AI authenticity',
    'hrm':        'AI in human resources',
    'remote':     'Remote work',
}

CARD_LINE = {
    'retrieval':  'Writing the explanation yourself catches far more of the errors '
                  'than reading the system&rsquo;s.',
    'errors':     'When the checking happens matters more than what the checking says.',
    'edubot':     'An AI tutor teaching the curriculum in local Nigerian languages, '
                  'built by students.',
    'creativity': 'Authenticity works as armour right up until the moment it is '
                  'contradicted.',
    'hrm':        'What changes for the people doing the work when AI enters hiring '
                  'and evaluation.',
    'remote':     'Early and persistent adopters grew faster &mdash; but more remote '
                  'was not better.',
}

# A card is too small for "Journal of Management Information Systems".
VENUE_SHORT = {
    'retrieval': 'JMIS',
    'hrm':       'Book chapter',
}
