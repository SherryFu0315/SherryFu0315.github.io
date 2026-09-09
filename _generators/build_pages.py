# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B   # reuse FONTS, nav(), FOOT so every page stays identical

R = B.R

PEOPLE = [
 dict(name='Anqi Zhang', url='https://anqizhang1.github.io/',
      role='Doctoral candidate, Computer Information Systems',
      note='Committee co-chair, with Prof. Likoebe M. Maruping. Service automation, privacy and human&ndash;robot interaction.'),
 dict(name='Xinyuan Wei', url='https://xinyuan-wei-xw.github.io/',
      role='Doctoral student, Digital Innovation',
      note='Committee member. Center for Digital Innovation, Robinson College of Business.'),
 dict(name='Shaohui Wang', url='https://drusagi.github.io/',
      role='Doctoral candidate, Computer Information Systems',
      note='Committee member.'),
 dict(name='Yingxin Zhou', url='https://ualr.edu/business/people/yingxin-zhou/',
      role='Assistant Professor of Business Information Systems, University of Arkansas at Little Rock',
      note='Committee member. Graduated from Georgia State.'),
 dict(name='Kartikeya Negi', url='https://www.linkedin.com/in/kartik-negi/',
      role='Texas State University',
      note='Committee member. Graduated from Georgia State.'),
 dict(name='Theresa Le', url='https://aisel.aisnet.org/treos_amcis2025/194/',
      role='Master&rsquo;s student, Georgia State University',
      note='Advised as an undergraduate on the AMCIS 2025 TREO talk <em>Talk to Me: A Preliminary Review on the Evolution and Impact of Emotional AI</em>, with Kaitlyn Yu Mai.'),
]

def person(p):
    nm = ('<a href="%s">%s</a>' % (p['url'], p['name'])) if p['url'] else p['name']
    return ('      <li>\n        <span class="p-name">%s</span>\n'
            '        <span class="p-role">%s</span>\n'
            '        <span class="p-note">%s</span>\n      </li>' % (nm, p['role'], p['note']))

people_html = '\n'.join(person(p) for p in PEOPLE)

JOIN = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Work with me &mdash; Xinyu Fu</title>
<meta name="description" content="Xinyu Fu welcomes student research assistant volunteers at Georgia State University. Send a CV and one writing sample &mdash; a course project report is perfectly fine.">
FONTS
</head>
<body>

<div class="topbar"></div>
<div class="shell">

NAV

  <section class="cta">
    <div>
      <p class="eyebrow eyebrow--boxed">Student research assistants &middot; volunteers</p>
      <h2>Come work on this with me.</h2>
      <p class="lede">I take on <b>student research assistant volunteers</b> year-round, undergraduate and graduate. You do not need prior research experience, and you do not need to have taken my class. You need to be curious and to finish things.</p>
      <p style="font-size:16px;max-width:52ch">These are unpaid volunteer positions. What they are worth is the part you cannot get from coursework: seeing how a study is actually built, how data actually behaves, and how an argument survives &mdash; or does not survive &mdash; three rounds of review.</p>
    </div>
    <div>
      <ol class="send-list">
        <li><span class="n">01</span><span>A <b>CV or r&eacute;sum&eacute;</b>. One page is plenty.</span></li>
        <li><span class="n">02</span><span>One <b>writing sample</b>. A course project report is perfectly fine &mdash; I care how you build an argument, not where it was published.</span></li>
        <li><span class="n">03</span><span>Two sentences on <b>which project caught your eye</b>, and why.</span></li>
      </ol>
      <p style="margin:22px 0 0">
        <a class="btn mail" data-u="xinyufu" data-d="gsu.edu" data-s="Research assistant volunteer" data-b="Hi Dr. Fu,&#10;&#10;I would like to volunteer as a research assistant.&#10;&#10;Attached: my CV and a writing sample.&#10;&#10;The project that caught my eye: " href="#">Email xinyufu [at] gsu.edu</a>
      </p>
      <p style="margin:14px 0 0;font-size:13px;color:var(--muted)">That link opens a message with the three items already listed, so nothing gets forgotten.</p>
    </div>
  </section>

  <div class="sec-head" id="students">
    <h2>Students I work with</h2>
    <span class="count">Doctoral committees and advising</span>
  </div>

  <div class="prose">
    <ul class="people">
PEOPLE
    </ul>
  </div>

  <div class="strip">
    <div class="strip-cell">
      <h3>What you would actually do</h3>
      <ul>
        <li>Clean, code and merge field data &mdash; call records, interview transcripts, platform scrapes</li>
        <li>Run structured literature searches and keep a real annotated bibliography</li>
        <li>Build the experiment platforms studies run on (React, Python, Qualtrics, Prolific)</li>
        <li>Sit in on analysis, from the first regression to the last robustness check</li>
        <li>Read drafts and say what does not make sense &mdash; this one is not decoration</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>What I ask for</h3>
      <ul>
        <li>Roughly 5&ndash;8 hours a week during term, agreed in advance</li>
        <li>One semester minimum. Research is slow; a month teaches you nothing</li>
        <li>Tell me early when something is not working. That is not failure, that is the job</li>
        <li>Any coding background helps &mdash; Python, R, SQL, JavaScript &mdash; but none is required for every project</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>What you get back</h3>
      <ul>
        <li>A reference that says something specific, because I will know your work</li>
        <li>Co-authorship on conference submissions where the contribution earns it</li>
        <li>An honest read on whether a PhD is right for you, from someone with no stake in the answer</li>
        <li>Skills that transfer: cleaning messy data, defending a claim, writing to be understood</li>
      </ul>
    </div>
  </div>

  <div class="prose">
    <h3>Common questions</h3>

    <p><b>I am not a CIS major. Should I still write?</b><br>
    Yes. My studies run on sales calls, factory floors, hotel corridors, crowdfunding pages and online communities. Psychology, economics, management, statistics, communication, computer science &mdash; all of it is useful. Say in your email what you bring.</p>

    <p><b>I have never written anything academic. What do I send?</b><br>
    A course project report. A term paper. A technical write-up from an internship. A well-argued blog post. I am reading for whether you can hold a claim and support it, not for a literature review.</p>

    <p><b>I am not at Georgia State.</b><br>
    Still write. Some projects work remotely. Say where you are and what your term dates look like.</p>

    <p><b>Can this turn into a paid position or a thesis?</b><br>
    Sometimes. Funded slots come and go with grants, and undergraduate projects have grown out of RA work before. Start with the volunteer route and we will see what it becomes.</p>

    <p><b>I emailed and did not hear back.</b><br>
    Send it again after two weeks. That is not rudeness, that is my inbox.</p>

    <h3>Competition coaching</h3>
    <p>I coached the Georgia State team at <a href="https://carlsonschool.umn.edu/conferences/comis"><b>CoMIS 2025</b></a>, the international undergraduate MIS case competition hosted by the Carlson School at the University of Minnesota. The team took first place at the group level and advanced to the final round. If your team wants a faculty coach, write to me early &mdash; these things are won in the preparation, not the room.</p>
  </div>

FOOT

</div>
</body>
</html>
'''
JOIN = (JOIN.replace('FONTS', B.FONTS).replace('NAV', B.nav('/join/'))
            .replace('PEOPLE', people_html).replace('FOOT', B.FOOT))
io.open(os.path.join(R, 'join/index.html'), 'w', encoding='utf-8').write(JOIN)
print('join/index.html', len(JOIN), 'bytes,', len(PEOPLE), 'people')


TEACH = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Teaching &mdash; Xinyu Fu</title>
<meta name="description" content="Courses taught by Xinyu Fu at Georgia State University and the University of Pittsburgh: Agentic AI for Business &amp; Society, Data Programming, and Database Management Systems.">
FONTS
</head>
<body>

<div class="topbar"></div>
<div class="shell">

NAV

  <div class="sec-head">
    <h2>Teaching</h2>
    <span class="count">2025 Unforgettable Educator Award &middot; nominated by students</span>
  </div>

  <div class="prose">

    <h3>Georgia State University</h3>

    <div class="course">
      <div class="when">Fall 2026</div>
      <div>
        <h4><a href="https://sherryfu0315.github.io/cis4394-agentic-ai/index.html">Agentic AI</a></h4>
        <p>Build. Break. Iterate. The full agent lifecycle practiced from day one &mdash; the brain, the tools, the orchestration, the self-evaluation &mdash; ending in a capstone where teams take a real problem from idea to working prototype and pitch it.</p>
        <p style="margin-top:10px">Taught as part of <a href="https://path.mit.edu/"><b>PATH</b></a> &mdash; Pathways for AI Training and Hiring, a multi-year MIT RAISE and Georgia State initiative building industry-aligned AI training, with the Robinson College of Business anchoring the Georgia hub.</p>
        <p class="proj-links" style="margin-top:12px">
          <a href="https://sherryfu0315.github.io/cis4394-agentic-ai/index.html">Course site</a>
          <a href="https://path.mit.edu/">PATH</a>
          <a href="https://news.gsu.edu/2026/04/03/mit-raise-and-georgia-state-university-announce-path">The announcement</a>
          <a href="https://www.youtube.com/watch?v=LnyWCPhFzzA&amp;list=PL8lQ0qMEI-E8-64gGMvrHBSqbGQkAsXCD&amp;index=1">Talks</a>
        </p>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2026</div>
      <div>
        <h4>Agentic AI</h4>
        <p>Undergraduate. The first run of the course, co-taught with Dr. Amrita George.</p>
      </div>
    </div>

    <div class="course">
      <div class="when">Fall 2025<br>Fall 2024 &middot; Fall 2023</div>
      <div>
        <h4>Data Programming</h4>
        <p>Undergraduate. Python for people who came to solve business problems rather than to write software &mdash; data wrangling, analysis, and the point at which a model earns the right to be believed.</p>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2025<br>Spring 2024</div>
      <div>
        <h4>Fundamentals of Database Management Systems</h4>
        <p>Graduate core.</p>
      </div>
    </div>

    <div class="course">
      <div class="when">Fall 2024<br>Fall 2023</div>
      <div>
        <h4>Database Management Systems</h4>
        <p>Undergraduate core.</p>
      </div>
    </div>

    <h3>University of Pittsburgh</h3>

    <div class="course">
      <div class="when">Fall 2021</div>
      <div>
        <h4>Introduction to Information Systems</h4>
        <p>Undergraduate core. Instructor.</p>
        <blockquote class="quote">&ldquo;Professor Fu was fantastic. She created an environment where everyone learned, and worked her hardest to let students of every coding level keep up. I am grateful for how easily she broke down machine learning.&rdquo;
        <cite>Student evaluation, 2021</cite></blockquote>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2021</div>
      <div>
        <h4>Data Programming Essentials with Python</h4>
        <p>MBA and MS elective. Instructor; also teaching assistant for this course in Spring and Fall 2019.</p>
        <p style="margin-top:8px"><em>2021 Doris &amp; Douglas Bernstein Doctoral Student Teaching Award &mdash; one student per year.</em></p>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2019</div>
      <div>
        <h4>Advanced Data Programming with R</h4>
        <p>MBA and MS elective. Teaching assistant.</p>
      </div>
    </div>

    <h3>Elsewhere</h3>

    <div class="course">
      <div class="when">Summer 2019</div>
      <div>
        <h4>E-Commerce</h4>
        <p>MBA. Teaching assistant, Harvard University.</p>
      </div>
    </div>

    <div class="course">
      <div class="when">2014&ndash;2017</div>
      <div>
        <h4>Career Center instructor and student mentor</h4>
        <p>Tsinghua University.</p>
      </div>
    </div>

    <p style="margin-top:34px"><a class="btn" href="/join/">Students I work with, and how to join &rarr;</a></p>
  </div>

FOOT

</div>
</body>
</html>
'''
TEACH = TEACH.replace('FONTS', B.FONTS).replace('NAV', B.nav('/teaching/')).replace('FOOT', B.FOOT)
io.open(os.path.join(R, 'teaching/index.html'), 'w', encoding='utf-8').write(TEACH)
print('teaching/index.html', len(TEACH), 'bytes')
