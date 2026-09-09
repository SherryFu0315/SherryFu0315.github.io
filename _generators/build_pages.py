# -*- coding: utf-8 -*-
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import words as T   # all reader-facing wording lives in words.py
import build as B   # reuse FONTS, nav(), FOOT so every page stays identical

R = B.R

PEOPLE = [
 dict(name='Anqi Zhang', url='https://anqizhang1.github.io/',
      role='Doctoral candidate, Computer Information Systems',
      note='Committee co-chair, with Prof. Likoebe M. Maruping. Service automation, privacy and human&ndash;robot interaction.'),
 dict(name='Xinyuan Wei', url='https://xinyuan-wei-xw.github.io/',
      role='Doctoral student, Center for Digital Innovation (CDIN)',
      note='Committee member. Robinson College of Business.'),
 dict(name='Shaohui Wang', url='https://drusagi.github.io/',
      role='Doctoral candidate, Computer Information Systems',
      note='Committee member.'),
 dict(name='Yingxin Zhou', url='https://ualr.edu/business/people/yingxin-zhou/',
      role='Assistant Professor of Business Information Systems, University of Arkansas at Little Rock',
      note='Committee member. Graduated from Georgia State.'),
 dict(name='Kartikeya Negi', url='https://www.linkedin.com/in/kartik-negi/',
      role='Assistant Professor, Texas State University',
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
<title>__JOIN_PAGE_TITLE__</title>
<meta name="description" content="Xinyu Fu welcomes student research assistant volunteers at Georgia State University. Send a CV and one writing sample &mdash; a course project report is perfectly fine.">
FONTS
</head>
<body>

<div class="topbar"></div>
<div class="shell">

NAV

  <section class="cta">
    <div>
      <p class="eyebrow eyebrow--boxed">__JOIN_EYEBROW__</p>
      <h2>__JOIN_CTA_HEADLINE__</h2>
      <p class="lede">__JOIN_LEDE__</p>
      <p style="font-size:16px;max-width:52ch">__JOIN_UNPAID_NOTE__</p>
    </div>
    <div>
      <ol class="send-list">
        <li><span class="n">01</span><span>__JOIN_SEND_CV__</span></li>
        <li><span class="n">02</span><span>__JOIN_SEND_WRITING_SAMPLE__</span></li>
        <li><span class="n">03</span><span>__JOIN_SEND_WHICH_PROJECT__</span></li>
      </ol>
      <p style="margin:22px 0 0">
        <a class="btn mail" data-u="xinyufu" data-d="gsu.edu" data-s="Research assistant volunteer" data-b="Hi Dr. Fu,&#10;&#10;I would like to volunteer as a research assistant.&#10;&#10;Attached: my CV and a writing sample.&#10;&#10;The project that caught my eye: " href="#">__JOIN_EMAIL_BUTTON__</a>
      </p>
    </div>
  </section>

  <div class="sec-head" id="students">
    <h2>__JOIN_STUDENTS_TITLE__</h2>
    <span class="count">__JOIN_STUDENTS_SUBTITLE__</span>
  </div>

  <div class="prose">
    <ul class="people">
PEOPLE
    </ul>
  </div>

  <div class="strip">
    <div class="strip-cell">
      <h3>__JOIN_WHAT_YOU_WOULD_DO_TITLE__</h3>
      <ul>
        <li>__JOIN_WHAT_YOU_WOULD_DO_DATA__</li>
        <li>__JOIN_WHAT_YOU_WOULD_DO_LITERATURE__</li>
        <li>__JOIN_WHAT_YOU_WOULD_DO_PLATFORMS__</li>
        <li>__JOIN_WHAT_YOU_WOULD_DO_ANALYSIS__</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>__JOIN_WHAT_I_ASK_FOR_TITLE__</h3>
      <ul>
        <li>__JOIN_WHAT_I_ASK_FOR_HOURS__</li>
        <li>__JOIN_WHAT_I_ASK_FOR_SEMESTER__</li>
        <li>__JOIN_WHAT_I_ASK_FOR_SPEAK_UP__</li>
        <li>__JOIN_WHAT_I_ASK_FOR_CODING__</li>
      </ul>
    </div>
    <div class="strip-cell">
      <h3>__JOIN_WHAT_YOU_GET_BACK_TITLE__</h3>
      <ul>
        <li>__JOIN_WHAT_YOU_GET_BACK_REFERENCE__</li>
        <li>__JOIN_WHAT_YOU_GET_BACK_COAUTHORSHIP__</li>
        <li>__JOIN_WHAT_YOU_GET_BACK_PHD_ADVICE__</li>
        <li>__JOIN_WHAT_YOU_GET_BACK_SKILLS__</li>
      </ul>
    </div>
  </div>

  <div class="prose">
    <h3>__JOIN_FAQ_TITLE__</h3>

    <p><b>__JOIN_FAQ_NOT_CIS_Q__</b><br>
    __JOIN_FAQ_NOT_CIS_A__</p>

    <p><b>__JOIN_FAQ_NO_ACADEMIC_WRITING_Q__</b><br>
    __JOIN_FAQ_NO_ACADEMIC_WRITING_A__</p>

    <p><b>__JOIN_FAQ_NOT_AT_GSU_Q__</b><br>
    __JOIN_FAQ_NOT_AT_GSU_A__</p>

    <p><b>__JOIN_FAQ_PAID_OR_THESIS_Q__</b><br>
    __JOIN_FAQ_PAID_OR_THESIS_A__</p>

    <p><b>__JOIN_FAQ_NO_REPLY_Q__</b><br>
    __JOIN_FAQ_NO_REPLY_A__</p>

    <h3>__JOIN_COACHING_TITLE__</h3>
    <p>__JOIN_COACHING_TEXT__</p>
  </div>

FOOT

</div>
</body>
</html>
'''
JOIN = (JOIN.replace('FONTS', B.FONTS).replace('NAV', B.nav('/join/'))
            .replace('PEOPLE', people_html).replace('FOOT', B.FOOT)
            .replace('__JOIN_PAGE_TITLE__', T.JOIN_PAGE_TITLE)
            .replace('__JOIN_EYEBROW__', T.JOIN_EYEBROW)
            .replace('__JOIN_CTA_HEADLINE__', T.JOIN_CTA_HEADLINE)
            .replace('__JOIN_LEDE__', T.JOIN_LEDE)
            .replace('__JOIN_UNPAID_NOTE__', T.JOIN_UNPAID_NOTE)
            .replace('__JOIN_SEND_CV__', T.JOIN_SEND_CV)
            .replace('__JOIN_SEND_WRITING_SAMPLE__', T.JOIN_SEND_WRITING_SAMPLE)
            .replace('__JOIN_SEND_WHICH_PROJECT__', T.JOIN_SEND_WHICH_PROJECT)
            .replace('__JOIN_EMAIL_BUTTON__', T.JOIN_EMAIL_BUTTON)
            .replace('__JOIN_STUDENTS_TITLE__', T.JOIN_STUDENTS_TITLE)
            .replace('__JOIN_STUDENTS_SUBTITLE__', T.JOIN_STUDENTS_SUBTITLE)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_TITLE__', T.JOIN_WHAT_YOU_WOULD_DO_TITLE)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_DATA__', T.JOIN_WHAT_YOU_WOULD_DO_DATA)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_LITERATURE__', T.JOIN_WHAT_YOU_WOULD_DO_LITERATURE)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_PLATFORMS__', T.JOIN_WHAT_YOU_WOULD_DO_PLATFORMS)
            .replace('__JOIN_WHAT_YOU_WOULD_DO_ANALYSIS__', T.JOIN_WHAT_YOU_WOULD_DO_ANALYSIS)
            .replace('__JOIN_WHAT_I_ASK_FOR_TITLE__', T.JOIN_WHAT_I_ASK_FOR_TITLE)
            .replace('__JOIN_WHAT_I_ASK_FOR_HOURS__', T.JOIN_WHAT_I_ASK_FOR_HOURS)
            .replace('__JOIN_WHAT_I_ASK_FOR_SEMESTER__', T.JOIN_WHAT_I_ASK_FOR_SEMESTER)
            .replace('__JOIN_WHAT_I_ASK_FOR_SPEAK_UP__', T.JOIN_WHAT_I_ASK_FOR_SPEAK_UP)
            .replace('__JOIN_WHAT_I_ASK_FOR_CODING__', T.JOIN_WHAT_I_ASK_FOR_CODING)
            .replace('__JOIN_WHAT_YOU_GET_BACK_TITLE__', T.JOIN_WHAT_YOU_GET_BACK_TITLE)
            .replace('__JOIN_WHAT_YOU_GET_BACK_REFERENCE__', T.JOIN_WHAT_YOU_GET_BACK_REFERENCE)
            .replace('__JOIN_WHAT_YOU_GET_BACK_COAUTHORSHIP__', T.JOIN_WHAT_YOU_GET_BACK_COAUTHORSHIP)
            .replace('__JOIN_WHAT_YOU_GET_BACK_PHD_ADVICE__', T.JOIN_WHAT_YOU_GET_BACK_PHD_ADVICE)
            .replace('__JOIN_WHAT_YOU_GET_BACK_SKILLS__', T.JOIN_WHAT_YOU_GET_BACK_SKILLS)
            .replace('__JOIN_FAQ_TITLE__', T.JOIN_FAQ_TITLE)
            .replace('__JOIN_FAQ_NOT_CIS_Q__', T.JOIN_FAQ_NOT_CIS_Q)
            .replace('__JOIN_FAQ_NOT_CIS_A__', T.JOIN_FAQ_NOT_CIS_A)
            .replace('__JOIN_FAQ_NO_ACADEMIC_WRITING_Q__', T.JOIN_FAQ_NO_ACADEMIC_WRITING_Q)
            .replace('__JOIN_FAQ_NO_ACADEMIC_WRITING_A__', T.JOIN_FAQ_NO_ACADEMIC_WRITING_A)
            .replace('__JOIN_FAQ_NOT_AT_GSU_Q__', T.JOIN_FAQ_NOT_AT_GSU_Q)
            .replace('__JOIN_FAQ_NOT_AT_GSU_A__', T.JOIN_FAQ_NOT_AT_GSU_A)
            .replace('__JOIN_FAQ_PAID_OR_THESIS_Q__', T.JOIN_FAQ_PAID_OR_THESIS_Q)
            .replace('__JOIN_FAQ_PAID_OR_THESIS_A__', T.JOIN_FAQ_PAID_OR_THESIS_A)
            .replace('__JOIN_FAQ_NO_REPLY_Q__', T.JOIN_FAQ_NO_REPLY_Q)
            .replace('__JOIN_FAQ_NO_REPLY_A__', T.JOIN_FAQ_NO_REPLY_A)
            .replace('__JOIN_COACHING_TITLE__', T.JOIN_COACHING_TITLE)
            .replace('__JOIN_COACHING_TEXT__', T.JOIN_COACHING_TEXT))
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
    <span class="count is-award">__TEACHING_AWARD_NOTE__</span>
  </div>

  <div class="prose">

    <h3>__TEACHING_GSU_HEADING__</h3>

    <div class="course">
      <div class="when">Fall 2026</div>
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
      <div class="when">Spring 2026</div>
      <div>
        <h4>__TEACHING_AGENTIC_AI_SPRING_2026_TITLE__</h4>
        <p>__TEACHING_AGENTIC_AI_SPRING_2026_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when">Fall 2025<br>Fall 2024<br>Fall 2023</div>
      <div>
        <h4>__TEACHING_DATA_PROGRAMMING_TITLE__</h4>
        <p>__TEACHING_DATA_PROGRAMMING_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2025<br>Spring 2024</div>
      <div>
        <h4>__TEACHING_DB_FUNDAMENTALS_TITLE__</h4>
        <p>__TEACHING_DB_FUNDAMENTALS_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when">Fall 2024<br>Fall 2023</div>
      <div>
        <h4>__TEACHING_DBMS_TITLE__</h4>
        <p>__TEACHING_DBMS_DESC__</p>
      </div>
    </div>

    <h3>__TEACHING_PITT_HEADING__</h3>

    <div class="course">
      <div class="when">Fall 2021</div>
      <div>
        <h4>__TEACHING_INTRO_IS_TITLE__</h4>
        <p>__TEACHING_INTRO_IS_DESC__</p>
        <blockquote class="quote">__TEACHING_INTRO_IS_STUDENT_QUOTE__
        <cite>__TEACHING_INTRO_IS_QUOTE_CITE__</cite></blockquote>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2021</div>
      <div>
        <h4>__TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE__</h4>
        <p>__TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC__</p>
        <p style="margin-top:8px"><em>__TEACHING_BERNSTEIN_AWARD_NOTE__</em></p>
      </div>
    </div>

    <div class="course">
      <div class="when">Spring 2019</div>
      <div>
        <h4>__TEACHING_ADVANCED_R_TITLE__</h4>
        <p>__TEACHING_ADVANCED_R_DESC__</p>
      </div>
    </div>

    <h3>__TEACHING_ELSEWHERE_HEADING__</h3>

    <div class="course">
      <div class="when">Summer 2019</div>
      <div>
        <h4>__TEACHING_ECOMMERCE_TITLE__</h4>
        <p>__TEACHING_ECOMMERCE_DESC__</p>
      </div>
    </div>

    <div class="course">
      <div class="when">2014&ndash;2017</div>
      <div>
        <h4>__TEACHING_CAREER_CENTER_TITLE__</h4>
        <p>__TEACHING_CAREER_CENTER_DESC__</p>
      </div>
    </div>

    <p style="margin-top:34px"><a class="btn" href="/join/">__TEACHING_JOIN_BUTTON__</a></p>
  </div>

FOOT

</div>
</body>
</html>
'''
TEACH = (TEACH.replace('FONTS', B.FONTS).replace('NAV', B.nav('/teaching/')).replace('FOOT', B.FOOT)
              .replace('__TEACHING_PAGE_TITLE__', T.TEACHING_PAGE_TITLE)
              .replace('__TEACHING_HEADING__', T.TEACHING_HEADING)
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
              .replace('__TEACHING_INTRO_IS_STUDENT_QUOTE__', T.TEACHING_INTRO_IS_STUDENT_QUOTE)
              .replace('__TEACHING_INTRO_IS_QUOTE_CITE__', T.TEACHING_INTRO_IS_QUOTE_CITE)
              .replace('__TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE__', T.TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE)
              .replace('__TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC__', T.TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC)
              .replace('__TEACHING_BERNSTEIN_AWARD_NOTE__', T.TEACHING_BERNSTEIN_AWARD_NOTE)
              .replace('__TEACHING_ADVANCED_R_TITLE__', T.TEACHING_ADVANCED_R_TITLE)
              .replace('__TEACHING_ADVANCED_R_DESC__', T.TEACHING_ADVANCED_R_DESC)
              .replace('__TEACHING_ELSEWHERE_HEADING__', T.TEACHING_ELSEWHERE_HEADING)
              .replace('__TEACHING_ECOMMERCE_TITLE__', T.TEACHING_ECOMMERCE_TITLE)
              .replace('__TEACHING_ECOMMERCE_DESC__', T.TEACHING_ECOMMERCE_DESC)
              .replace('__TEACHING_CAREER_CENTER_TITLE__', T.TEACHING_CAREER_CENTER_TITLE)
              .replace('__TEACHING_CAREER_CENTER_DESC__', T.TEACHING_CAREER_CENTER_DESC)
              .replace('__TEACHING_JOIN_BUTTON__', T.TEACHING_JOIN_BUTTON))
io.open(os.path.join(R, 'teaching/index.html'), 'w', encoding='utf-8').write(TEACH)
print('teaching/index.html', len(TEACH), 'bytes')
