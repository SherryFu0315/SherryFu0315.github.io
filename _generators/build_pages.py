# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import words as T   # all reader-facing wording lives in words.py
import build as B   # reuse FONTS, nav(), FOOT so every page stays identical

R = B.R

PEOPLE = [
 dict(name='Anqi Zhang', url='https://anqizhang1.github.io/', now=True,
      role='Doctoral candidate, Computer Information Systems',
      note='Committee co-chair, with Prof. Likoebe M. Maruping'),
 dict(name='Xinyuan Wei', url='https://xinyuan-wei-xw.github.io/', now=True,
      role='Doctoral student, Center for Digital Innovation',
      note='Committee member'),
 dict(name='Shaohui Wang', url='https://drusagi.github.io/', now=True,
      role='Doctoral candidate, Computer Information Systems',
      note='Committee member'),
 dict(name='Theresa Le', url='https://aisel.aisnet.org/treos_amcis2025/194/', now=True,
      role='Master&rsquo;s student, Georgia State University',
      note='Advised as an undergraduate on an AMCIS 2025 TREO talk'),
 dict(name='Yingxin Zhou', url='https://ualr.edu/business/people/yingxin-zhou/', now=False,
      role='Assistant Professor of Business Information Systems, University of Arkansas at Little Rock',
      note='Committee member'),
 dict(name='Kartikeya Negi', url='https://www.linkedin.com/in/kartik-negi/', now=False,
      role='Assistant Professor, Texas State University',
      note='Committee member'),
]

def person(p):
    nm = ('<a href="%s">%s</a>' % (p['url'], p['name'])) if p['url'] else p['name']
    return ('      <li>\n        <span class="p-name">%s</span>\n'
            '        <span class="p-role">%s</span>\n'
            '        <span class="p-note">%s</span>\n      </li>' % (nm, p['role'], p['note']))

people_now  = '\n'.join(person(x) for x in PEOPLE if x['now'])
people_past = '\n'.join(person(x) for x in PEOPLE if not x['now'])

JOIN = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__JOIN_PAGE_TITLE__</title>
<meta name="description" content="The students Xinyu Fu advises at Georgia State University, and how to volunteer as a student research assistant — open year-round, undergraduate and graduate.">
FONTS
</head>
<body>

<div class="topbar"></div>
<div class="shell page-quiet">

NAV

  <header class="page-head page-head--solo">
    <div>
      <h1 class="page-title">__JOIN_CTA_HEADLINE__</h1>
      <p class="intro">__JOIN_LEDE__</p>
    </div>
  </header>

  <section class="sec mod" id="advising">
    <h3>__JOIN_STUDENTS_NOW__</h3>
    <ul class="people">
PEOPLE_NOW
    </ul>
    <h3>__JOIN_STUDENTS_PAST__</h3>
    <ul class="people">
PEOPLE_PAST
    </ul>
  </section>

  <section class="sec mod mod--tint" id="students">
    <h2>__JOIN_RA_TITLE__</h2>
    <p class="intro">__JOIN_RA_LEDE__</p>

    <div class="cols">
      <div>
        <h3>__JOIN_WHAT_YOU_WOULD_DO_TITLE__</h3>
        <ul>
          <li>__JOIN_WHAT_YOU_WOULD_DO_DATA__</li>
          <li>__JOIN_WHAT_YOU_WOULD_DO_LITERATURE__</li>
          <li>__JOIN_WHAT_YOU_WOULD_DO_PLATFORMS__</li>
          <li>__JOIN_WHAT_YOU_WOULD_DO_ANALYSIS__</li>
        </ul>
      </div>
      <div>
        <h3>__JOIN_WHAT_I_ASK_FOR_TITLE__</h3>
        <ul>
          <li>__JOIN_WHAT_I_ASK_FOR_HOURS__</li>
          <li>__JOIN_WHAT_I_ASK_FOR_SEMESTER__</li>
          <li>__JOIN_WHAT_I_ASK_FOR_SPEAK_UP__</li>
          <li>__JOIN_WHAT_I_ASK_FOR_CODING__</li>
        </ul>
      </div>
      <div>
        <h3>__JOIN_SEND_TITLE__</h3>
        <ul>
          <li>__JOIN_SEND_CV__</li>
          <li>__JOIN_SEND_WRITING_SAMPLE__</li>
          <li>__JOIN_SEND_WHICH_PROJECT__</li>
        </ul>
        <p class="cols-go"><a class="btn mail" data-u="xinyufu" data-d="gsu.edu" data-s="Research assistant volunteer" data-b="Hi Dr. Fu,&#10;&#10;I would like to volunteer as a research assistant.&#10;&#10;Attached: my CV and a writing sample.&#10;&#10;The project that caught my eye: " href="#">__JOIN_EMAIL_BUTTON__</a></p>
      </div>
    </div>

  </section>


FOOT

</div>
</body>
</html>
'''
JOIN = (JOIN.replace('FONTS', B.FONTS).replace('NAV', B.nav('/join/'))
            .replace('PEOPLE_NOW', people_now).replace('PEOPLE_PAST', people_past).replace('FOOT', B.FOOT)
            .replace('__JOIN_PAGE_TITLE__', T.JOIN_PAGE_TITLE)
            .replace('__JOIN_RA_TITLE__', T.JOIN_RA_TITLE)
            .replace('__JOIN_RA_LEDE__', T.JOIN_RA_LEDE)
            .replace('__JOIN_SEND_TITLE__', T.JOIN_SEND_TITLE)
            .replace('__JOIN_CTA_HEADLINE__', T.JOIN_CTA_HEADLINE)
            .replace('__JOIN_LEDE__', T.JOIN_LEDE)
            .replace('__JOIN_SEND_CV__', T.JOIN_SEND_CV)
            .replace('__JOIN_SEND_WRITING_SAMPLE__', T.JOIN_SEND_WRITING_SAMPLE)
            .replace('__JOIN_SEND_WHICH_PROJECT__', T.JOIN_SEND_WHICH_PROJECT)
            .replace('__JOIN_EMAIL_BUTTON__', T.JOIN_EMAIL_BUTTON)
            .replace('__JOIN_STUDENTS_NOW__', T.JOIN_STUDENTS_NOW)
            .replace('__JOIN_STUDENTS_PAST__', T.JOIN_STUDENTS_PAST)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_TITLE__', T.JOIN_WHAT_YOU_WOULD_DO_TITLE)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_DATA__', T.JOIN_WHAT_YOU_WOULD_DO_DATA)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_LITERATURE__', T.JOIN_WHAT_YOU_WOULD_DO_LITERATURE)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_PLATFORMS__', T.JOIN_WHAT_YOU_WOULD_DO_PLATFORMS)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_ANALYSIS__', T.JOIN_WHAT_YOU_WOULD_DO_ANALYSIS)
            .replace('__JOIN_WHAT_I_ASK_FOR_TITLE__', T.JOIN_WHAT_I_ASK_FOR_TITLE)
            .replace('__JOIN_WHAT_I_ASK_FOR_HOURS__', T.JOIN_WHAT_I_ASK_FOR_HOURS)
            .replace('__JOIN_WHAT_I_ASK_FOR_SEMESTER__', T.JOIN_WHAT_I_ASK_FOR_SEMESTER)
            .replace('__JOIN_WHAT_I_ASK_FOR_SPEAK_UP__', T.JOIN_WHAT_I_ASK_FOR_SPEAK_UP)
            .replace('__JOIN_WHAT_I_ASK_FOR_CODING__', T.JOIN_WHAT_I_ASK_FOR_CODING))
io.open(os.path.join(R, 'join/index.html'), 'w', encoding='utf-8').write(JOIN)
print('join/index.html', len(JOIN), 'bytes,', len(PEOPLE), 'people')


TEACH = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TEACHING_PAGE_TITLE__</title>
<meta name="description" content="Courses taught by Xinyu Fu at Georgia State University and the University of Pittsburgh: Agentic AI for Business &amp; Society, Data Programming, and Database Management Systems.">
FONTS
</head>
<body>

<div class="topbar"></div>
<div class="shell">

NAV

  <div class="sec-head">
    <h2>__TEACHING_HEADING__</h2>
    <div class="awards">
      <span class="count is-award">__TEACHING_AWARD_NOTE__</span>
      <span class="count is-award">__TEACHING_AWARD_NOTE_2021__</span>
    </div>
  </div>

  <section class="mod mod--tint">
    <h3>__TEACHING_GSU_HEADING__</h3>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#FF7874" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><path d="M12 1.6c1 6.9 2.5 8.4 9.4 9.4-6.9 1-8.4 2.5-9.4 9.4-1-6.9-2.5-8.4-9.4-9.4 6.9-1 8.4-2.5 9.4-9.4Z"/></svg></span>Fall 2026</div>
      <div>
        <h4><a href="https://sherryfu0315.github.io/cis4394-agentic-ai/index.html">__TEACHING_AGENTIC_AI_TITLE__</a></h4>
        <p>__TEACHING_AGENTIC_AI_DESC__</p>
        <p style="margin-top:10px">__TEACHING_AGENTIC_AI_PATH_NOTE__</p>
        <p class="proj-links" style="margin-top:12px">
          <a href="https://sherryfu0315.github.io/cis4394-agentic-ai/index.html">__TEACHING_AGENTIC_AI_LINK_COURSE_SITE__</a>
          <a href="https://path.mit.edu/">__TEACHING_AGENTIC_AI_LINK_PATH__</a>
          <a href="https://news.gsu.edu/2026/04/03/mit-raise-and-georgia-state-university-announce-path">__TEACHING_AGENTIC_AI_LINK_ANNOUNCEMENT__</a>
          <a href="https://www.youtube.com/watch?v=LnyWCPhFzzA&amp;list=PL8lQ0qMEI-E8-64gGMvrHBSqbGQkAsXCD&amp;index=1">__TEACHING_AGENTIC_AI_LINK_TALKS__</a>
        </p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#FF7874" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><path d="M12 1.6c1 6.9 2.5 8.4 9.4 9.4-6.9 1-8.4 2.5-9.4 9.4-1-6.9-2.5-8.4-9.4-9.4 6.9-1 8.4-2.5 9.4-9.4Z"/></svg></span>Spring 2026</div>
      <div>
        <h4>__TEACHING_AGENTIC_AI_SPRING_2026_TITLE__</h4>
        <p>__TEACHING_AGENTIC_AI_SPRING_2026_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#274CEC" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><circle cx="5" cy="17" r="1.5"/><circle cx="9.5" cy="13.5" r="1.5"/><circle cx="14" cy="12" r="1.5"/><circle cx="18.5" cy="7" r="1.5"/><path d="M3.5 19.5 20.5 5" fill="none" stroke-width="1.4"/></svg></span>Fall 2025<br>Fall 2024<br>Fall 2023</div>
      <div>
        <h4>__TEACHING_DATA_PROGRAMMING_TITLE__</h4>
        <p>__TEACHING_DATA_PROGRAMMING_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#8E5FC0" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><ellipse cx="12" cy="6" rx="7" ry="2.6" fill="none" stroke-width="1.4"/><path d="M5 6v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6V6" fill="none" stroke-width="1.4"/><path d="M5 12v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6v-6" fill="none" stroke-width="1.4"/></svg></span>Spring 2025<br>Spring 2024</div>
      <div>
        <h4>__TEACHING_DB_FUNDAMENTALS_TITLE__</h4>
        <p>__TEACHING_DB_FUNDAMENTALS_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#8E5FC0" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><ellipse cx="12" cy="6" rx="7" ry="2.6" fill="none" stroke-width="1.4"/><path d="M5 6v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6V6" fill="none" stroke-width="1.4"/><path d="M5 12v6c0 1.4 3.1 2.6 7 2.6s7-1.2 7-2.6v-6" fill="none" stroke-width="1.4"/></svg></span>Fall 2024<br>Fall 2023</div>
      <div>
        <h4>__TEACHING_DBMS_TITLE__</h4>
        <p>__TEACHING_DBMS_DESC__</p>
      </div>
    </div>
  </section>

  <section class="mod">
    <h3>__TEACHING_PITT_HEADING__</h3>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#6B5F7D" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><rect x="3" y="5" width="18" height="13" rx="1.6" fill="none" stroke-width="1.4"/><path d="M3 9h18" fill="none" stroke-width="1.4"/><circle cx="5.6" cy="7" r=".8"/></svg></span>Fall 2021</div>
      <div>
        <h4>__TEACHING_INTRO_IS_TITLE__</h4>
        <p>__TEACHING_INTRO_IS_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#274CEC" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><circle cx="5" cy="17" r="1.5"/><circle cx="9.5" cy="13.5" r="1.5"/><circle cx="14" cy="12" r="1.5"/><circle cx="18.5" cy="7" r="1.5"/><path d="M3.5 19.5 20.5 5" fill="none" stroke-width="1.4"/></svg></span>Spring 2021</div>
      <div>
        <h4>__TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE__</h4>
        <p>__TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#274CEC" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><circle cx="5" cy="17" r="1.5"/><circle cx="9.5" cy="13.5" r="1.5"/><circle cx="14" cy="12" r="1.5"/><circle cx="18.5" cy="7" r="1.5"/><path d="M3.5 19.5 20.5 5" fill="none" stroke-width="1.4"/></svg></span>Spring 2019</div>
      <div>
        <h4>__TEACHING_ADVANCED_R_TITLE__</h4>
        <p>__TEACHING_ADVANCED_R_DESC__</p>
      </div>
    </div>
  </section>

  <section class="mod mod--tint">
    <h3>__TEACHING_ELSEWHERE_HEADING__</h3>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#6B5F7D" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><path d="M3.5 4h2.2l2.3 10.4h9.2l2-7.2H7.2" fill="none" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9.5" cy="19" r="1.5"/><circle cx="16.5" cy="19" r="1.5"/></svg></span>Summer 2019</div>
      <div>
        <h4>__TEACHING_ECOMMERCE_TITLE__</h4>
        <p>__TEACHING_ECOMMERCE_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when"><span class="ico" style="--ic:#6B5F7D" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor"><circle cx="12" cy="12" r="8.4" fill="none" stroke-width="1.4"/><path d="m15 9-4.2 1.6L9 15l4.2-1.6L15 9Z"/></svg></span>2014&ndash;2017</div>
      <div>
        <h4>__TEACHING_CAREER_CENTER_TITLE__</h4>
        <p>__TEACHING_CAREER_CENTER_DESC__</p>
      </div>
    </div>
  </section>

  <section class="mod">
    <h3>__TEACHING_COACHING_TITLE__</h3>
    <p>__TEACHING_COACHING_TEXT__</p>
  </section>

FOOT

</div>
</body>
</html>
'''
TEACH = (TEACH.replace('FONTS', B.FONTS).replace('NAV', B.nav('/teaching/')).replace('FOOT', B.FOOT)
              .replace('__TEACHING_PAGE_TITLE__', T.TEACHING_PAGE_TITLE)
              .replace('__TEACHING_HEADING__', T.TEACHING_HEADING)
            .replace('__TEACHING_COACHING_TITLE__', T.TEACHING_COACHING_TITLE)
            .replace('__TEACHING_COACHING_TEXT__', T.TEACHING_COACHING_TEXT)
              .replace('__TEACHING_AWARD_NOTE__', T.TEACHING_AWARD_NOTE)
              .replace('__TEACHING_GSU_HEADING__', T.TEACHING_GSU_HEADING)
              .replace('__TEACHING_AGENTIC_AI_TITLE__', T.TEACHING_AGENTIC_AI_TITLE)
              .replace('__TEACHING_AGENTIC_AI_DESC__', T.TEACHING_AGENTIC_AI_DESC)
              .replace('__TEACHING_AGENTIC_AI_PATH_NOTE__', T.TEACHING_AGENTIC_AI_PATH_NOTE)
              .replace('__TEACHING_AGENTIC_AI_LINK_COURSE_SITE__', T.TEACHING_AGENTIC_AI_LINK_COURSE_SITE)
              .replace('__TEACHING_AGENTIC_AI_LINK_PATH__', T.TEACHING_AGENTIC_AI_LINK_PATH)
              .replace('__TEACHING_AGENTIC_AI_LINK_ANNOUNCEMENT__', T.TEACHING_AGENTIC_AI_LINK_ANNOUNCEMENT)
              .replace('__TEACHING_AGENTIC_AI_LINK_TALKS__', T.TEACHING_AGENTIC_AI_LINK_TALKS)
              .replace('__TEACHING_AGENTIC_AI_SPRING_2026_TITLE__', T.TEACHING_AGENTIC_AI_SPRING_2026_TITLE)
              .replace('__TEACHING_AGENTIC_AI_SPRING_2026_DESC__', T.TEACHING_AGENTIC_AI_SPRING_2026_DESC)
              .replace('__TEACHING_DATA_PROGRAMMING_TITLE__', T.TEACHING_DATA_PROGRAMMING_TITLE)
              .replace('__TEACHING_DATA_PROGRAMMING_DESC__', T.TEACHING_DATA_PROGRAMMING_DESC)
              .replace('__TEACHING_DB_FUNDAMENTALS_TITLE__', T.TEACHING_DB_FUNDAMENTALS_TITLE)
              .replace('__TEACHING_DB_FUNDAMENTALS_DESC__', T.TEACHING_DB_FUNDAMENTALS_DESC)
              .replace('__TEACHING_DBMS_TITLE__', T.TEACHING_DBMS_TITLE)
              .replace('__TEACHING_DBMS_DESC__', T.TEACHING_DBMS_DESC)
              .replace('__TEACHING_PITT_HEADING__', T.TEACHING_PITT_HEADING)
              .replace('__TEACHING_INTRO_IS_TITLE__', T.TEACHING_INTRO_IS_TITLE)
              .replace('__TEACHING_INTRO_IS_DESC__', T.TEACHING_INTRO_IS_DESC)
              .replace('__TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE__', T.TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE)
              .replace('__TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC__', T.TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC)
              .replace('__TEACHING_AWARD_NOTE_2021__', T.TEACHING_AWARD_NOTE_2021)
              .replace('__TEACHING_ADVANCED_R_TITLE__', T.TEACHING_ADVANCED_R_TITLE)
              .replace('__TEACHING_ADVANCED_R_DESC__', T.TEACHING_ADVANCED_R_DESC)
              .replace('__TEACHING_ELSEWHERE_HEADING__', T.TEACHING_ELSEWHERE_HEADING)
              .replace('__TEACHING_ECOMMERCE_TITLE__', T.TEACHING_ECOMMERCE_TITLE)
              .replace('__TEACHING_ECOMMERCE_DESC__', T.TEACHING_ECOMMERCE_DESC)
              .replace('__TEACHING_CAREER_CENTER_TITLE__', T.TEACHING_CAREER_CENTER_TITLE)
              .replace('__TEACHING_CAREER_CENTER_DESC__', T.TEACHING_CAREER_CENTER_DESC))

io.open(os.path.join(R, 'teaching/index.html'), 'w', encoding='utf-8').write(TEACH)
print('teaching/index.html', len(TEACH), 'bytes')
