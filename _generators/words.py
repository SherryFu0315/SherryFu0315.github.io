# -*- coding: utf-8 -*-
"""
words.py — every sentence on the website that a reader sees.

This is the file to edit when you want to change the wording. You do not need to
know any Python; you are only changing the text between the quote marks.

    HOME_INTRO = "the words you want"
                  ^^^^^^^^^^^^^^^^^^ change this part only

Three rules:

  1. Leave the quote marks at both ends alone. If your text needs to contain a
     quote mark, use the triple-quoted form that some entries below already use.
  2. Leave anything that looks like __N_CITED__ alone. Those are filled in with
     real numbers when the site is built.
  3. Things like &mdash; &rsquo; &amp; are punctuation spelled out so browsers
     render them properly: &mdash; is a long dash, &rsquo; is an apostrophe,
     &amp; is an ampersand. Keep them as they are, and copy the pattern if you
     need one. A plain apostrophe or & typed directly can break the page.

Anything wrapped in <b>...</b> is bold on the page, and <a href="...">...</a> is
a link. Those may be moved or removed with the sentence they sit in.

When you have saved your changes, double-click "Preview site.command" in the main
folder to rebuild and look at the result.

Names of projects, their authors, status and descriptions are NOT here — those
live in projects.py, one block per study.
"""



# ==========================================================================
#  THE HOMEPAGE AND THE RESEARCH PAGE
#  Also the navigation and the footer, which appear on every page except the map.
# ==========================================================================

# Where it appears: top navigation bar, first link (back to the front page)
HOME_NAV_HOME = "Home"

# Where it appears: top navigation bar, link to the research page
HOME_NAV_RESEARCH = "Research"

# Where it appears: top navigation bar, link to the research map page
HOME_NAV_UNIVERSE = "Universe"

# Where it appears: top navigation bar, link to the publications page
HOME_NAV_PUBLICATIONS = "Publications"

# Where it appears: top navigation bar, link to the teaching page
HOME_NAV_TEACHING = "Teaching"

# Where it appears: top navigation bar, the highlighted button at the right
HOME_NAV_WORK_WITH_ME = "Work with me"

# Where it appears: footer, the postal address in the first column
HOME_FOOT_ADDRESS = """Department of Computer Information Systems<br>
      J. Mack Robinson College of Business, Georgia State University<br>
      55 Park Place NE, Suite 1727, Atlanta, GA 30303"""

# Where it appears: footer, heading of the middle column
HOME_FOOT_ELSEWHERE_TITLE = "Elsewhere"

# Where it appears: footer, first link of the "Elsewhere" column
HOME_FOOT_GOOGLE_SCHOLAR = "Google Scholar"

# Where it appears: footer, second link of the "Elsewhere" column
HOME_FOOT_LINKEDIN = "LinkedIn"

# Where it appears: footer, heading of the last column
HOME_FOOT_CREDITS_TITLE = "Credits"

# Where it appears: footer, the sentence under the "Credits" heading
HOME_FOOT_CREDIT_LINE = """Photography and figure credits: <a href="/credits/">credits</a>."""

# ---- The front page (/) ----

# Where it appears: browser tab and search results title for the front page
HOME_PAGE_TITLE = "Xinyu Fu &mdash; Human&ndash;AI Complementarity"

# Where it appears: job title and affiliation beside the photo at the top of the front page
HOME_ROLE = """<b>Assistant Professor of Computer Information Systems</b><br>
          J. Mack Robinson College of Business<br>Georgia State University"""

# Where it appears: the statement paragraph under the name at the top of the front page
HOME_THESIS = "<b>I am fascinated by how people can achieve more with less through better ways of working with AI.</b> My research explores the design of human&ndash;AI collaboration and its behavioral and organizational implications."

# Where it appears: list of links at the top of the front page, the email row
HOME_RAIL_EMAIL = "Email"

# Where it appears: list of links at the top of the front page, the Google Scholar row
HOME_RAIL_GOOGLE_SCHOLAR = "Google Scholar"

# Where it appears: small note beside "Google Scholar" in that list of links
HOME_RAIL_GOOGLE_SCHOLAR_NOTE = "Publications &amp; citations"

# Where it appears: list of links at the top of the front page, the LinkedIn row
HOME_RAIL_LINKEDIN = "LinkedIn"

# Where it appears: list of links at the top of the front page, the students row
HOME_RAIL_STUDENTS = "Students"

# Where it appears: small note beside "Students" in that list of links
HOME_RAIL_STUDENTS_NOTE = "RA volunteers welcome &rarr;"

# Where it appears: small label at the top of the starry card linking to the research map
HOME_MAP_EYEBROW = "Interactive"

# Where it appears: headline on the starry card linking to the research map
HOME_MAP_HEADLINE = "The shoulders we stand on"

# Where it appears: paragraph on the starry card linking to the research map
# (the study and paper counts fill themselves in)
HOME_MAP_BLURB = "__N_STUDIES__ of my studies, drawn among the __N_CITED__ papers they lean on. Nothing here is placed by hand &mdash; two studies sit near each other only because they draw on the same work. Mostly it shows what a small corner of a field any one person&rsquo;s research is."

# Where it appears: button at the bottom of the starry card linking to the research map
HOME_MAP_BUTTON = "Open the map &rarr;"

# Where it appears: heading of the projects section in the middle of the front page
HOME_SELECTED_RESEARCH_TITLE = "Selected Research"

# Where it appears: small caption beside the "Selected Research" heading
HOME_SELECTED_RESEARCH_COUNT = """Six of thirteen &middot; <a href="/research/">all projects</a>"""

# Where it appears: small boxed label above the headline of the "come work with me" block
HOME_JOIN_EYEBROW = "Student research assistants"

# Where it appears: headline of the "come work with me" block on the front page
HOME_JOIN_HEADLINE = "Come work on this with me."

# Where it appears: opening paragraph of the "come work with me" block on the front page
HOME_JOIN_LEDE = "I take on <b>student research assistant volunteers</b> year-round, undergraduate and graduate. You do not need research experience and you do not need to have taken my class. You need to be curious and to finish things."

# Where it appears: second paragraph of the "come work with me" block, about past students
HOME_JOIN_RECENT_STUDENTS = "Recent students have cleaned and coded field data, run literature searches, built the experiment platforms my studies run on, and sat in on analysis from the first regression to the last."

# Where it appears: item 01 of the numbered "what to send" list on the front page
HOME_JOIN_SEND_CV = "A <b>CV or r&eacute;sum&eacute;</b>. One page is plenty."

# Where it appears: item 02 of the numbered "what to send" list on the front page
HOME_JOIN_SEND_WRITING_SAMPLE = "One <b>writing sample</b>. A course project report is perfectly fine &mdash; I care how you build an argument, not where it was published."

# Where it appears: item 03 of the numbered "what to send" list on the front page
HOME_JOIN_SEND_WHICH_PROJECT = "Two sentences on <b>which project caught your eye</b>, and why."

# Where it appears: label on the email button under the "what to send" list
HOME_JOIN_EMAIL_BUTTON = "Email xinyufu [at] gsu.edu"

# Where it appears: small link under the email button, to the "Work with me" page
HOME_JOIN_MORE_LINK = "Who I work with, and what the work is like &rarr;"

# Where it appears: heading of the first of the three columns near the bottom of the front page
HOME_RECENT_TITLE = "Recent"

# Where it appears: "Recent" column, the 2026 item
HOME_RECENT_JMIS = "<i>Knowing Is Not Enough</i> accepted at the Journal of Management Information Systems"

# Where it appears: "Recent" column, the 2025 item
HOME_RECENT_TEACHING_AWARD = "Unforgettable Educator Award, Robinson College of Business &mdash; nominated by students"

# Where it appears: "Recent" column, the 2024 item
HOME_RECENT_NSSFC = "National Social Science Fund of China, national-level funding"

# Where it appears: heading of the second of the three columns near the bottom of the front page
HOME_PRESS_TITLE = "In the press"

# Where it appears: "In the press" column, the 2025 item
HOME_PRESS_EDUBOT = """<a href="https://www.itedgenews.africa/edubot-naija-launches-ai-powered-multilingual-learning-platform-across-nigeria/">EduBot Naija launches AI-powered multilingual learning platform across Nigeria</a> &mdash; ITEdgeNews, on a student&ndash;faculty project building curriculum-aligned lessons in local Nigerian languages"""

# Where it appears: heading of the third of the three columns near the bottom of the front page
HOME_TEACHING_TITLE = "Teaching now"

# Where it appears: "Teaching now" column, the Fall 2026 course
HOME_TEACHING_F26 = """<a href="https://sherryfu0315.github.io/cis4394-agentic-ai/index.html">Agentic AI</a> &mdash; a <a href="https://path.mit.edu/">PATH</a> course"""

# Where it appears: "Teaching now" column, the Spring 2026 course
HOME_TEACHING_S26 = "Agentic AI"

# Where it appears: last row of the "Teaching now" column, linking to the teaching page
HOME_TEACHING_ALL_COURSES = "All courses &rarr;"

# ---- The research page (/research/) ----

# Where it appears: browser tab and search results title for the research page
RESEARCH_PAGE_TITLE = "Research &mdash; Xinyu Fu"

# Where it appears: heading at the top of the research page
RESEARCH_HEADING = "Research"

# Where it appears: small caption beside the "Research" heading
RESEARCH_COUNT = """Fifteen projects, most settled first &middot; <a href="/universe/">see the map</a>"""

# Where it appears: note under the list of projects on the research page
RESEARCH_UNDER_REVIEW_NOTE = """Work under review is listed without a journal
    name until a decision is final. Conference papers and service are on the
    <a href="/publications/">publications page</a>."""

# Where it appears: button at the bottom of the research page, linking to the "Work with me" page
RESEARCH_JOIN_BUTTON = "Want to work on one of these? &rarr;"

# Where it appears: stand-in shown for a project that has no one-line finding written yet
# (used for the project cards on both the research page and the front page)
RESEARCH_FINDING_COMING_SOON = "A short description of this project is coming."

# Where it appears: top-left corner of the two-axis grid of projects
RESEARCH_MATRIX_CORNER = "Research&nbsp;/ AI"


# ==========================================================================
#  THE RESEARCH MAP
#  The page at /universe/ with the two views of the stars.
# ==========================================================================

# Where it appears: browser tab / search-result title for the research map page
MAP_PAGE_TITLE = "Research Universe &mdash; Xinyu Fu"

# Where it appears: top navigation bar, first link (back to the front page)
MAP_NAV_HOME = "Home"

# Where it appears: top navigation bar, link to the research page
MAP_NAV_RESEARCH = "Research"

# Where it appears: top navigation bar, link to this map page
MAP_NAV_UNIVERSE = "Universe"

# Where it appears: top navigation bar, link to the publications page
MAP_NAV_PUBLICATIONS = "Publications"

# Where it appears: top navigation bar, link to the teaching page
MAP_NAV_TEACHING = "Teaching"

# Where it appears: top navigation bar, the highlighted button at the right
MAP_NAV_WORK_WITH_ME = "Work with me"

# Where it appears: the big headline at the top of the map page
MAP_H1 = "How the work<br>connects"

# Where it appears: paragraph beside the headline, shown while the map is in
# the "The literature" arrangement (the study and paper counts fill themselves in)
MAP_HEAD_COPY_CITE = "No axes here &mdash; this is where the literature puts them. Every faint star is a paper one of my studies leans on; the bright ones are the studies. Two sit close together <b>only because they draw on the same work</b>. __N_CSTUDIES__ studies against __N_CITED__ papers is about the right sense of scale."

# Where it appears: the left button of the view switcher, top right of the page
MAP_VIEW_TOGGLE_AXES = "Two axes"

# Where it appears: the right button of the view switcher, top right of the page
MAP_VIEW_TOGGLE_LITERATURE = "The literature"

# Where it appears: button in the bottom-right corner of the map
MAP_BTN_ZOOM_OUT = "Zoom out"

# Where it appears: button in the bottom-right corner of the map, beside "Zoom out"
MAP_BTN_WHOLE_SKY = "Whole sky"

# Where it appears: caption under the map while the "Two axes" arrangement is showing
MAP_BLURB_AXIS = "Where I file each study. The constellations are real ones &mdash; Ursa Major, Cassiopeia, Orion, Lyra, Corvus, Crux &mdash; and the grey points are the places still open in each cell."

# Where it appears: caption under the map while the "The literature" arrangement is
# showing (the two counts fill themselves in)
MAP_BLURB_CITE = "Every faint star is a work one of these studies leans on; the bright ones are the studies. <b>No position here is chosen by hand</b> &mdash; a force simulation runs over the real citation graph, so two studies sit close together only when they draw on the same references, and a work several papers lean on is pulled into the space between them. <b>__N_CITED__</b> works, <b>__N_SHARED__</b> of them reached by more than one study. The point of drawing it this way is the proportion: a working life of research is a small, well-lit patch of somebody else&rsquo;s field."

# Where it appears: heading of the plain-text list of studies below the map
MAP_INDEX_TITLE = "Everything on the map, in plain text"

# Where it appears: sentence under that heading, above the plain-text list
MAP_INDEX_INTRO = "Grouped by what kind of AI each study is about. Works without JavaScript, and reads correctly to a screen reader."

# Where it appears: stand-in shown for a study that has no one-line finding written yet
MAP_FINDING_COMING_SOON = "A short description of this project is coming."


# ==========================================================================
#  THE "WORK WITH ME" PAGE AND THE TEACHING PAGE
# ==========================================================================

# Where it appears: browser tab and search results title for the "Work with me" page
JOIN_PAGE_TITLE = "Work with me &mdash; Xinyu Fu"

# Where it appears: small boxed label above the headline at the top of the "Work with me" page
JOIN_EYEBROW = "Student research assistants &middot; volunteers"

# Where it appears: main headline at the top of the "Work with me" page
JOIN_CTA_HEADLINE = "Come work on this with me."

# Where it appears: opening paragraph under the headline on the "Work with me" page
JOIN_LEDE = "I take on <b>student research assistant volunteers</b> year-round, undergraduate and graduate. You do not need prior research experience, and you do not need to have taken my class. You need to be curious and to finish things."

# Where it appears: second paragraph under the headline, about the positions being unpaid
JOIN_UNPAID_NOTE = "These are unpaid volunteer positions. What they are worth is the part you cannot get from coursework: seeing how a study is actually built, and how data actually behaves."

# Where it appears: item 01 of the numbered "what to send" list on the "Work with me" page
JOIN_SEND_CV = "A <b>CV or r&eacute;sum&eacute;</b>. One page is plenty."

# Where it appears: item 02 of the numbered "what to send" list on the "Work with me" page
JOIN_SEND_WRITING_SAMPLE = "One <b>writing sample</b>. A course project report is perfectly fine &mdash; I care how you build an argument, not where it was published."

# Where it appears: item 03 of the numbered "what to send" list on the "Work with me" page
JOIN_SEND_WHICH_PROJECT = "Two sentences on <b>which project caught your eye</b>, and why."

# Where it appears: label on the email button under the "what to send" list
JOIN_EMAIL_BUTTON = "Email xinyufu [at] gsu.edu"


# Where it appears: section heading above the list of students, on the "Work with me" page
JOIN_STUDENTS_TITLE = "Students I work with"

# Where it appears: small caption beside the "Students I work with" heading
JOIN_STUDENTS_SUBTITLE = "Doctoral committees and advising"

# Where it appears: heading of the first of the three columns on the "Work with me" page
JOIN_WHAT_YOU_WOULD_DO_TITLE = "What you would actually do"

# Where it appears: "What you would actually do" column, data item
JOIN_WHAT_YOU_WOULD_DO_DATA = "Clean, code and merge field data &mdash; call records, interview transcripts, platform scrapes"

# Where it appears: "What you would actually do" column, literature search item
JOIN_WHAT_YOU_WOULD_DO_LITERATURE = "Run structured literature searches and keep a real annotated bibliography"

# Where it appears: "What you would actually do" column, experiment platform item
JOIN_WHAT_YOU_WOULD_DO_PLATFORMS = "Build the experiment platforms studies run on (React, Python, Qualtrics, Prolific)"

# Where it appears: "What you would actually do" column, analysis item
JOIN_WHAT_YOU_WOULD_DO_ANALYSIS = "Sit in on analysis, from the first regression to the last robustness check"


# Where it appears: heading of the second of the three columns on the "Work with me" page
JOIN_WHAT_I_ASK_FOR_TITLE = "What I ask for"

# Where it appears: "What I ask for" column, hours item
JOIN_WHAT_I_ASK_FOR_HOURS = "Roughly 5&ndash;8 hours a week during term, agreed in advance"

# Where it appears: "What I ask for" column, length of commitment item
JOIN_WHAT_I_ASK_FOR_SEMESTER = "One semester minimum. Research is slow; a month teaches you nothing"

# Where it appears: "What I ask for" column, speaking up item
JOIN_WHAT_I_ASK_FOR_SPEAK_UP = "Tell me early when something is not working. That is not failure, that is the job"

# Where it appears: "What I ask for" column, coding background item
JOIN_WHAT_I_ASK_FOR_CODING = "Any coding background helps &mdash; Python, R, SQL, JavaScript &mdash; but none is required for every project"

# Where it appears: heading of the third of the three columns on the "Work with me" page
JOIN_WHAT_YOU_GET_BACK_TITLE = "What you get back"

# Where it appears: "What you get back" column, reference letter item
JOIN_WHAT_YOU_GET_BACK_REFERENCE = "A reference that says something specific, because I will know your work"

# Where it appears: "What you get back" column, co-authorship item
JOIN_WHAT_YOU_GET_BACK_COAUTHORSHIP = "Co-authorship on conference submissions where the contribution earns it"

# Where it appears: "What you get back" column, PhD advice item
JOIN_WHAT_YOU_GET_BACK_PHD_ADVICE = "An honest read on whether a PhD is right for you, from someone with no stake in the answer"

# Where it appears: "What you get back" column, transferable skills item
JOIN_WHAT_YOU_GET_BACK_SKILLS = "Skills that transfer: cleaning messy data, defending a claim, writing to be understood"

# Where it appears: heading above the questions and answers on the "Work with me" page
JOIN_FAQ_TITLE = "Common questions"

# Where it appears: common questions, first question
JOIN_FAQ_NOT_CIS_Q = "I am not a CIS major. Should I still write?"

# Where it appears: common questions, answer to the first question
JOIN_FAQ_NOT_CIS_A = "Yes. My studies run on sales calls, factory floors, hotel corridors, crowdfunding pages and online communities. Psychology, economics, management, statistics, communication, computer science &mdash; all of it is useful. Say in your email what you bring."

# Where it appears: common questions, second question
JOIN_FAQ_NO_ACADEMIC_WRITING_Q = "I have never written anything academic. What do I send?"

# Where it appears: common questions, answer to the second question
JOIN_FAQ_NO_ACADEMIC_WRITING_A = "A course project report. A term paper. A technical write-up from an internship. A well-argued blog post. I am reading for whether you can hold a claim and support it, not for a literature review."

# Where it appears: common questions, third question
JOIN_FAQ_NOT_AT_GSU_Q = "I am not at Georgia State."

# Where it appears: common questions, answer to the third question
JOIN_FAQ_NOT_AT_GSU_A = "Still write. Some projects work remotely. Say where you are and what your term dates look like."

# Where it appears: common questions, fourth question
JOIN_FAQ_PAID_OR_THESIS_Q = "Can this turn into a paid position or a thesis?"

# Where it appears: common questions, answer to the fourth question
JOIN_FAQ_PAID_OR_THESIS_A = "Sometimes. Funded slots come and go with grants, and undergraduate projects have grown out of RA work before. Start with the volunteer route and we will see what it becomes."

# Where it appears: common questions, fifth question
JOIN_FAQ_NO_REPLY_Q = "I emailed and did not hear back."

# Where it appears: common questions, answer to the fifth question
JOIN_FAQ_NO_REPLY_A = "Please do follow up once more &mdash; a second message is always welcome."

# Where it appears: heading of the last section on the "Work with me" page
JOIN_COACHING_TITLE = "Competition coaching"

# Where it appears: paragraph under the "Competition coaching" heading
JOIN_COACHING_TEXT = """I coached the Georgia State team at <a href="https://carlsonschool.umn.edu/conferences/comis"><b>CoMIS 2025</b></a>, the international undergraduate MIS case competition hosted by the Carlson School at the University of Minnesota. The team took first place at the group level and advanced to the final round."""

# Where it appears: browser tab and search results title for the teaching page
TEACHING_PAGE_TITLE = "Teaching &mdash; Xinyu Fu"

# Where it appears: main heading at the top of the teaching page
TEACHING_HEADING = "Teaching"

# Where it appears: small caption beside the "Teaching" heading
TEACHING_AWARD_NOTE = "2025 Unforgettable Educator Award &middot; nominated by students"

# Where it appears: first institution heading on the teaching page
TEACHING_GSU_HEADING = "Georgia State University"

# Where it appears: course name of the Fall 2026 Georgia State course
TEACHING_AGENTIC_AI_TITLE = "Agentic AI"

# Where it appears: description of the Fall 2026 Agentic AI course
TEACHING_AGENTIC_AI_DESC = "Build. Break. Iterate. The full agent lifecycle practiced from day one &mdash; the brain, the tools, the orchestration, the self-evaluation &mdash; ending in a capstone where teams take a real problem from idea to working prototype and pitch it."

# Where it appears: second paragraph of the Fall 2026 Agentic AI course, about the PATH initiative
TEACHING_AGENTIC_AI_PATH_NOTE = """Taught as part of <a href="https://path.mit.edu/"><b>PATH</b></a> &mdash; Pathways for AI Training and Hiring, a multi-year MIT RAISE and Georgia State initiative building industry-aligned AI training, with the Robinson College of Business anchoring the Georgia hub."""

# Where it appears: link row under the Fall 2026 Agentic AI course, course site link
TEACHING_AGENTIC_AI_LINK_COURSE_SITE = "Course site"

# Where it appears: link row under the Fall 2026 Agentic AI course, PATH link
TEACHING_AGENTIC_AI_LINK_PATH = "PATH"

# Where it appears: link row under the Fall 2026 Agentic AI course, news announcement link
TEACHING_AGENTIC_AI_LINK_ANNOUNCEMENT = "The announcement"

# Where it appears: link row under the Fall 2026 Agentic AI course, talks link
TEACHING_AGENTIC_AI_LINK_TALKS = "Talks"

# Where it appears: course name of the Spring 2026 Georgia State course
TEACHING_AGENTIC_AI_SPRING_2026_TITLE = "Agentic AI"

# Where it appears: description of the Spring 2026 Agentic AI course
TEACHING_AGENTIC_AI_SPRING_2026_DESC = "Undergraduate. The first run of the course, co-taught with Dr. Amrita George."

# Where it appears: course name of the Georgia State data programming course
TEACHING_DATA_PROGRAMMING_TITLE = "Data Programming"

# Where it appears: description of the Georgia State data programming course
TEACHING_DATA_PROGRAMMING_DESC = "Undergraduate. Python for people who came to solve business problems rather than to write software &mdash; data wrangling, analysis, and the point at which a model earns the right to be believed."

# Where it appears: course name of the Georgia State graduate database course
TEACHING_DB_FUNDAMENTALS_TITLE = "Fundamentals of Database Management Systems"

# Where it appears: description of the Georgia State graduate database course
TEACHING_DB_FUNDAMENTALS_DESC = "Graduate core."

# Where it appears: course name of the Georgia State undergraduate database course
TEACHING_DBMS_TITLE = "Database Management Systems"

# Where it appears: description of the Georgia State undergraduate database course
TEACHING_DBMS_DESC = "Undergraduate core."

# Where it appears: second institution heading on the teaching page
TEACHING_PITT_HEADING = "University of Pittsburgh"

# Where it appears: course name of the Pittsburgh introductory course
TEACHING_INTRO_IS_TITLE = "Introduction to Information Systems"

# Where it appears: description of the Pittsburgh introductory course
TEACHING_INTRO_IS_DESC = "Undergraduate core. Instructor."

# Where it appears: student evaluation quote under the Pittsburgh introductory course
TEACHING_INTRO_IS_STUDENT_QUOTE = "&ldquo;Professor Fu was fantastic. She created an environment where everyone learned, and worked her hardest to let students of every coding level keep up. I am grateful for how easily she broke down machine learning.&rdquo;"

# Where it appears: attribution line under the student evaluation quote
TEACHING_INTRO_IS_QUOTE_CITE = "Student evaluation, 2021"

# Where it appears: course name of the Pittsburgh Python elective
TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE = "Data Programming Essentials with Python"

# Where it appears: description of the Pittsburgh Python elective
TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC = "MBA and MS elective. Instructor; also teaching assistant for this course in Spring and Fall 2019."

# Where it appears: teaching award note under the Pittsburgh Python elective
TEACHING_BERNSTEIN_AWARD_NOTE = "2021 Doris &amp; Douglas Bernstein Doctoral Student Teaching Award &mdash; one student per year."

# Where it appears: course name of the Pittsburgh R elective
TEACHING_ADVANCED_R_TITLE = "Advanced Data Programming with R"

# Where it appears: description of the Pittsburgh R elective
TEACHING_ADVANCED_R_DESC = "MBA and MS elective. Teaching assistant."

# Where it appears: third institution heading on the teaching page
TEACHING_ELSEWHERE_HEADING = "Elsewhere"

# Where it appears: course name of the Harvard course
TEACHING_ECOMMERCE_TITLE = "E-Commerce"

# Where it appears: description of the Harvard course
TEACHING_ECOMMERCE_DESC = "MBA. Teaching assistant, Harvard University."

# Where it appears: role name of the Tsinghua entry at the bottom of the teaching page
TEACHING_CAREER_CENTER_TITLE = "Career Center instructor and student mentor"

# Where it appears: description of the Tsinghua entry at the bottom of the teaching page
TEACHING_CAREER_CENTER_DESC = "Tsinghua University."

# Where it appears: button at the bottom of the teaching page, linking to the "Work with me" page
TEACHING_JOIN_BUTTON = "Students I work with, and how to join &rarr;"

