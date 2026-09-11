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
HOME_NAV_RESEARCH = "Projects"

# Where it appears: top navigation bar, link to the research map page
HOME_NAV_MAP = "Research map"

# Where it appears: top navigation bar, link to the publications page
HOME_NAV_PUBLICATIONS = "Publications"

# Where it appears: top navigation bar, link to the teaching page
HOME_NAV_TEACHING = "Teaching"

# Where it appears: top navigation bar, the highlighted button at the right
HOME_NAV_MENTORING = "Mentoring"

# Where it appears: footer, the postal address in the first column
HOME_FOOT_ADDRESS = """Department of Computer Information Systems<br>
      J. Mack Robinson College of Business, Georgia State University<br>
      55 Park Place NE, Atlanta, GA 30303"""

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
HOME_PAGE_TITLE = "Xinyu Fu &middot; Human&ndash;AI Complementarity"

# Where it appears: the greeting at the top of the front page, in the serif face
HOME_HELLO = "Hi, I&rsquo;m Xinyu Fu."

# Where it appears: first paragraph of the front page introduction &mdash; who she
# is, and the question the work is about
HOME_INTRO_1 = """I&rsquo;m an Assistant Professor of <a href="https://robinson.gsu.edu/academic-departments/computer-information-systems/">Computer Information Systems</a> at the J. Mack Robinson College of Business, <a href="https://www.gsu.edu/">Georgia State University</a>. I am fascinated by what makes <span class="nb">human&ndash;AI</span> collaboration greater than the sum of its parts. Specifically, my research explores how different <span class="nb">human&ndash;AI</span> configurations shape human performance, the organization of work, and the consequences of AI use."""

# Where it appears: second and last paragraph of the front page introduction
HOME_INTRO_2 = """My PhD is in <a href="https://business.pitt.edu/phd/phd-in-info-systems-and-tech-management/">Information Systems and Technology Management</a>, from the Katz Graduate School of Business at the <a href="https://www.pitt.edu/">University of Pittsburgh</a>, where I was advised by <a href="http://www.pitt.edu/~galletta/">Dr. Dennis Galletta</a> and <a href="https://sites.google.com/site/narayanramasubbu/">Dr. Narayan Ramasubbu</a>. I spent the summer of 2019 as a visiting scholar at <a href="https://www.harvard.edu/">Harvard University</a>."""

# Where it appears: the three links under the portrait at the top of the front page
HOME_EMAIL = "xinyufu [at] gsu.edu"
HOME_LINK_SCHOLAR = "Google Scholar"
HOME_LINK_LINKEDIN = "LinkedIn"


# Where it appears: heading of the projects section in the middle of the front page
HOME_SELECTED_RESEARCH_TITLE = "Selected Research"

# Where it appears: small caption beside the "Selected Research" heading
HOME_SELECTED_RESEARCH_COUNT = """<a href="/research/">All projects &rarr;</a>"""


# ==========================================================================
#  THE NEWS BAND ON THE FRONT PAGE
#  Latest news down the left, the press and the current course stacked on
#  the right.
# ==========================================================================

# Where it appears: heading of the news column, left of the news band
HOME_NEWS_TITLE = "Latest news"

# Where it appears: the four items of that column, newest first. The short text
# before each one is the year it happened.
HOME_NEWS_1 = """<a href="https://arxiv.org/abs/2609.01976"><i>Knowing Is Not Enough</i></a> accepted at the Journal of Management Information Systems"""
HOME_NEWS_2 = """<i>The Privacy Asymmetry of Service Robots</i> accepted at CIST, with doctoral candidate <a href="/join/#advising">Anqi Zhang</a>"""
HOME_NEWS_3 = """<i>Pathways to AI-Ready Entry-Level Talent</i> accepted at ICIS, the curriculum paper from <a href="https://path.mit.edu/">PATH</a>"""
HOME_NEWS_4 = """<a href="https://onlinelibrary.wiley.com/doi/10.1002/9781394266401.ch14">AI in Human Resource Management</a> published in <i>Advances in Human&ndash;AI Collaboration</i> (Wiley)"""

# Where it appears: link under the four news items. It goes to the publications
# page, so it says so — "more news" pointing at a publication list is a small
# broken promise.
HOME_NEWS_MORE = "All publications &rarr;"

# Where it appears: the words revealed when the pointer rests on a research
# card on the front page
HOME_CARD_GO = "View project &rarr;"


# Where it appears: heading of the press cell, top right of the news band
HOME_PRESS_TITLE = "In the press"

# Where it appears: the two press items, each an outlet and a headline
HOME_PRESS_1_OUTLET = "ITEdgeNews"
HOME_PRESS_1 = """<a href="https://www.itedgenews.africa/edubot-naija-launches-ai-powered-multilingual-learning-platform-across-nigeria/">EduBot Naija launches AI-powered multilingual learning platform across Nigeria</a> &middot; also in <a href="https://techafricanews.com/2025/08/14/a-computer-training-launches-edubot-nigeria-to-deliver-ai-powered-education-in-indigenous-languages/">TechAfrica News</a> and <a href="https://www.youtube.com/watch?v=3TnI3x-V_eQ">on video</a>"""

HOME_PRESS_2_OUTLET = "GSU News"
HOME_PRESS_2 = """<a href="https://news.gsu.edu/2026/04/03/mit-raise-and-georgia-state-university-announce-path">MIT RAISE and Georgia State announce PATH</a>, the initiative the Agentic AI course is taught under &middot; <a href="https://www.youtube.com/watch?v=LnyWCPhFzzA&amp;list=PL8lQ0qMEI-E8-64gGMvrHBSqbGQkAsXCD&amp;index=1">talks on video</a>"""


# Where it appears: heading of the teaching cell, bottom right of the news band
HOME_COURSE_TITLE = "Teaching"

# Where it appears: the course name and the terms it has run, in the teaching cell
HOME_COURSE_NAME = "Agentic AI"
HOME_COURSE_TERM = "Fall 2026 &middot; Spring 2026"


# Where it appears: the line under that, on the programme the course belongs to
HOME_COURSE_PATH = """Taught as part of <a href="https://path.mit.edu/">PATH</a>, the MIT RAISE and Georgia State initiative. Machine learning and data programming alongside it, since 2023."""

# Where it appears: the two links at the foot of the teaching cell
HOME_COURSE_LINK = "Course site &rarr;"
HOME_COURSE_ALL = "All courses &rarr;"

# ---- The research page (/research/) ----

# Where it appears: browser tab and search results title for the research page
RESEARCH_PAGE_TITLE = "Projects &middot; Xinyu Fu"

# Where it appears: heading at the top of the research page
RESEARCH_HEADING = "Projects"

# Where it appears: small caption beside the "Research" heading
RESEARCH_COUNT = """Fifteen projects, most settled first &middot; <a href="/universe/">see the map</a>"""

# Where it appears: note under the list of projects on the research page
RESEARCH_UNDER_REVIEW_NOTE = """Work under review is listed without a journal
    name until a decision is final. Conference papers and service are on the
    <a href="/publications/">publications page</a>."""

# Where it appears: button at the bottom of the research page, linking to the contact page
RESEARCH_JOIN_BUTTON = "How students get involved in these &rarr;"

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
MAP_PAGE_TITLE = "Research map &middot; Xinyu Fu"

# Where it appears: top navigation bar, first link (back to the front page)
MAP_NAV_HOME = "Home"

# Where it appears: top navigation bar, link to the research page
MAP_NAV_RESEARCH = "Projects"

# Where it appears: top navigation bar, link to this map page
MAP_NAV_MAP = "Research map"

# Where it appears: top navigation bar, link to the publications page
MAP_NAV_PUBLICATIONS = "Publications"

# Where it appears: top navigation bar, link to the teaching page
MAP_NAV_TEACHING = "Teaching"

# Where it appears: top navigation bar, the highlighted button at the right
MAP_NAV_MENTORING = "Mentoring"

# Where it appears: the big headline at the top of the map page
MAP_H1 = "How the work<br>connects"

# Where it appears: the paragraph beside the map's headline, in the two-axis
# view. The literature view swaps in MAP_HEAD_COPY_CITE.
MAP_HEAD_COPY_AXIS = """Two axes. Across: <b>what kind of AI</b> the study is about. Down: whether it <b>intervenes</b>, building something that makes people better at the work, or <b>observes</b> what AI set off once it arrived. Click an axis to fall into it; click a star to go to the study."""

# Where it appears: paragraph beside the headline, shown while the map is in
# the "The literature" arrangement (the study and paper counts fill themselves in)
MAP_HEAD_COPY_CITE = "Each bright star is one of my studies. Each faint one is a paper that a study cites. Studies that cite the same papers get pulled together, so the clumps you see are the ones that really do share a literature. <b>Hover a star</b> to see what that study is about; click it for the full entry."

# Where it appears: the left button of the view switcher, top right of the page
MAP_VIEW_TOGGLE_AXES = "Two axes"

# Where it appears: the right button of the view switcher, top right of the page
MAP_VIEW_TOGGLE_LITERATURE = "The literature"

# Where it appears: button in the bottom-right corner of the map
MAP_BTN_ZOOM_OUT = "Zoom out"

# Where it appears: button in the bottom-right corner of the map, beside "Zoom out"
MAP_BTN_WHOLE_SKY = "Whole sky"

# Where it appears: caption under the map while the "Two axes" arrangement is showing
MAP_BLURB_AXIS = "Where I file each study. The constellations are real ones (Ursa Major, Cassiopeia, Orion, Lyra, Corvus, Crux), and the grey points are the places still open in each cell."

# Where it appears: caption under the map while the "The literature" arrangement is
# showing (the two counts fill themselves in)
MAP_BLURB_CITE = """I took the reference list of every piece of work I have finished: __N_CSTUDIES__ of them, citing __N_CITED__ different papers between them. I matched the lists against each other, so a paper cited by two studies becomes one star rather than two. Then a physics simulation runs on it: every study pulls on the papers it cites, and every star pushes its neighbours away. Left to settle, studies that share references drift together and studies that share none drift apart."""


# Where it appears: stand-in shown for a study that has no one-line finding written yet
MAP_FINDING_COMING_SOON = "A short description of this project is coming."


# ==========================================================================
#  THE CONTACT PAGE AND THE TEACHING PAGE
# ==========================================================================

# Where it appears: browser tab and search results title for the contact page
JOIN_PAGE_TITLE = "Mentoring &middot; Xinyu Fu"

# Where it appears: the page title at the top of the contact page, in the serif
JOIN_CTA_HEADLINE = "Students I work with"

# Where it appears: the one paragraph under the title
JOIN_LEDE = """I sit on doctoral committees at Georgia State and advise undergraduate and master&rsquo;s students, and I take on student research assistant volunteers year-round. What follows is who I am working with, and what volunteering actually involves."""


# ==========================================================================
#  THE STUDENT SECTION
#  Short on purpose. Who it is for, what it asks, what to send.
# ==========================================================================

# Where it appears: heading of the student section
JOIN_RA_TITLE = "Student research assistants"

# Where it appears: the paragraph under that heading
JOIN_RA_LEDE = """I take on student research assistant volunteers year-round, undergraduate and graduate. No prior research experience is needed, and you do not need to have taken my class. The positions are unpaid; where a contribution warrants it, they can lead to co-authorship on a submission, or to a reference that speaks to specifics."""


# Where it appears: heading of the first of the three columns
JOIN_WHAT_YOU_WOULD_DO_TITLE = "What the work is"
JOIN_WHAT_YOU_WOULD_DO_DATA = "Cleaning and coding field data: call records, transcripts, scrapes"
JOIN_WHAT_YOU_WOULD_DO_LITERATURE = "Literature searches, and keeping a real annotated bibliography"
JOIN_WHAT_YOU_WOULD_DO_PLATFORMS = "Building the platforms studies run on: React, Python, Qualtrics, Prolific"
JOIN_WHAT_YOU_WOULD_DO_ANALYSIS = "Sitting in on analysis, from the first regression to the last robustness check"

# Where it appears: heading of the second of the three columns
JOIN_WHAT_I_ASK_FOR_TITLE = "What I ask"
JOIN_WHAT_I_ASK_FOR_HOURS = "Five to eight hours a week in term, agreed in advance"
JOIN_WHAT_I_ASK_FOR_SEMESTER = "A semester or more, since research moves slowly"
JOIN_WHAT_I_ASK_FOR_SPEAK_UP = "A word when something is not working, early rather than late"
JOIN_WHAT_I_ASK_FOR_CODING = "Any coding is useful (Python, R, SQL), though no project needs all of it"

# Where it appears: heading of the third of the three columns
JOIN_SEND_TITLE = "What to send"
JOIN_SEND_CV = "A CV or r&eacute;sum&eacute;, one page"
JOIN_SEND_WRITING_SAMPLE = "One writing sample. A course project report is perfectly fine"
JOIN_SEND_WHICH_PROJECT = "Two sentences on which project caught your eye, and why"

# Where it appears: the email button under the three columns
JOIN_EMAIL_BUTTON = "Email xinyufu [at] gsu.edu"


# Where it appears: the two group headings in the advising section
JOIN_STUDENTS_NOW = "Currently"
JOIN_STUDENTS_PAST = "Previously"

# Where it appears: browser tab and search results title for the teaching page
TEACHING_PAGE_TITLE = "Teaching &middot; Xinyu Fu"

# Where it appears: main heading at the top of the teaching page
TEACHING_HEADING = "Teaching"

# Where it appears: small caption beside the "Teaching" heading
TEACHING_AWARDS_TITLE = "Teaching awards"
TEACHING_AWARD_NOTE = "<b>2025 Unforgettable Educator Award</b>, Robinson College of Business, Georgia State University"

# Where it appears: first institution heading on the teaching page
TEACHING_GSU_HEADING = "Georgia State University"

# Where it appears: course name of the Fall 2026 Georgia State course
TEACHING_AGENTIC_AI_TITLE = "Agentic AI"

# Where it appears: description of the Fall 2026 Agentic AI course
TEACHING_AGENTIC_AI_DESC = "Build. Break. Iterate. The full agent lifecycle practiced from day one: the brain, the tools, the orchestration, the self-evaluation. It ends in a capstone where teams take a real problem from idea to working prototype and pitch it."

# Where it appears: second paragraph of the Fall 2026 Agentic AI course, about the PATH initiative
TEACHING_AGENTIC_AI_PATH_NOTE = """Taught as part of <a href="https://path.mit.edu/"><b>PATH</b></a> (Pathways for AI Training and Hiring), a multi-year MIT RAISE and Georgia State initiative building industry-aligned AI training, with the Robinson College of Business anchoring the Georgia hub."""

# Where it appears: link row under the Fall 2026 Agentic AI course, course site link
TEACHING_AGENTIC_AI_LINK_COURSE_SITE = "Course site"

# Where it appears: link row under the Fall 2026 Agentic AI course, PATH link
TEACHING_AGENTIC_AI_LINK_PATH = "PATH"

# Where it appears: link row under the Fall 2026 Agentic AI course, news announcement link
TEACHING_AGENTIC_AI_LINK_ANNOUNCEMENT = "The announcement"

# Where it appears: link row under the Fall 2026 Agentic AI course, talks link
TEACHING_AGENTIC_AI_LINK_TALKS = "Talks"

# Where it appears: course name of the Spring 2026 Georgia State course
TEACHING_AGENTIC_AI_SPRING_2026_TITLE = """<a href="https://catalogs.gsu.edu/preview_course_nopop.php?catoid=46&amp;coid=110537">Agentic AI</a>"""

# Where it appears: description of the Spring 2026 Agentic AI course
TEACHING_AGENTIC_AI_SPRING_2026_DESC = "Undergraduate. The first run of the course, co-taught with Dr. Amrita George."

# Where it appears: course name of the Georgia State data programming course
TEACHING_DATA_PROGRAMMING_TITLE = "Data Programming"

# Where it appears: description of the Georgia State data programming course
TEACHING_DATA_PROGRAMMING_DESC = "Undergraduate. Python and machine learning for people who came to solve business problems rather than to write software: wrangling the data, training a model, reading what it is actually telling you, and the point at which it earns the right to be believed."

# Where it appears: course name of the Georgia State graduate database course
TEACHING_DB_FUNDAMENTALS_TITLE = """<a href="https://catalogs.gsu.edu/preview_course_nopop.php?catoid=43&amp;coid=103745">Fundamentals of Database Management Systems</a>"""

# Where it appears: description of the Georgia State graduate database course
TEACHING_DB_FUNDAMENTALS_DESC = "Graduate core."

# Where it appears: course name of the Georgia State undergraduate database course
TEACHING_DBMS_TITLE = """<a href="https://catalogs.gsu.edu/preview_course_nopop.php?catoid=42&amp;coid=97477">Database Management Systems</a>"""

# Where it appears: description of the Georgia State undergraduate database course
TEACHING_DBMS_DESC = "Undergraduate core."

# Where it appears: the coaching section near the foot of the teaching page
TEACHING_COACHING_TITLE = "Competition coaching"

TEACHING_COACHING_TEXT = """I coached the Georgia State team at <a href="https://carlsonschool.umn.edu/conferences/comis">CoMIS 2025</a>, the international undergraduate MIS case competition hosted by the Carlson School at the University of Minnesota. The team took first place at the group level and advanced to the final round."""

# Where it appears: second institution heading on the teaching page
TEACHING_PITT_HEADING = "University of Pittsburgh"

# Where it appears: course name of the Pittsburgh introductory course
TEACHING_INTRO_IS_TITLE = """<a href="https://catalog.upp.pitt.edu/preview_course_nopop.php?catoid=72&amp;coid=376733">Introduction to Information Systems</a>"""

# Where it appears: description of the Pittsburgh introductory course
TEACHING_INTRO_IS_DESC = "Undergraduate core. Instructor."


# Where it appears: course name of the Pittsburgh Python elective
TEACHING_DATA_PROGRAMMING_ESSENTIALS_TITLE = """<a href="https://catalog.upp.pitt.edu/preview_course_nopop.php?catoid=189&amp;coid=1009994">Data Programming Essentials with Python</a>"""

# Where it appears: description of the Pittsburgh Python elective
TEACHING_DATA_PROGRAMMING_ESSENTIALS_DESC = "MBA and MS elective. Instructor; also teaching assistant for this course in Spring and Fall 2019."

# Where it appears: second award badge beside the "Teaching" heading
TEACHING_AWARD_NOTE_2021 = "<b>2021 <span class=\"nb\">Doris &amp; Douglas</span> Bernstein Doctoral Student Teaching Award</b>, University of Pittsburgh"

# Where it appears: course name of the Pittsburgh R elective
TEACHING_ADVANCED_R_TITLE = """<a href="https://catalog.upp.pitt.edu/preview_course_nopop.php?catoid=189&amp;coid=1010122">Advanced Data Programming with R</a>"""

# Where it appears: description of the Pittsburgh R elective
TEACHING_ADVANCED_R_DESC = "MBA and MS elective. Teaching assistant."

# Where it appears: third institution heading on the teaching page
TEACHING_ELSEWHERE_HEADING = "Elsewhere"

# Where it appears: course name of the Harvard course
TEACHING_ECOMMERCE_TITLE = """<a href="https://www.summer.harvard.edu/course-catalog/courses/electronic-commerce-strategies/34433?subjects=Management">E-Commerce</a>"""

# Where it appears: description of the Harvard course
TEACHING_ECOMMERCE_DESC = "MBA. Teaching assistant, Harvard University."

# Where it appears: role name of the Tsinghua entry at the bottom of the teaching page
TEACHING_CAREER_CENTER_TITLE = """<a href="https://career.tsinghua.edu.cn/careeren/Students.htm">Career Center instructor and student mentor</a>"""

# Where it appears: description of the Tsinghua entry at the bottom of the teaching page
TEACHING_CAREER_CENTER_DESC = "Tsinghua University."


# Where it appears: second paragraph of the note under the map, in the literature view
MAP_BLURB_CITE_2 = """Only __N_SHARED__ of those __N_CITED__ papers are cited by more than one study, which is why most stars sit in a single halo. Those __N_SHARED__ are the pale gold ones, and a line is drawn between two studies wherever they share a reference, and the more they share the heavier the line."""

# Where it appears: last paragraph of the note under the map, in the literature view
MAP_BLURB_CITE_3 = """The proportion is the part worth standing back for. A working life of research is a small, well-lit patch of somebody else&rsquo;s field. Every study is also listed in plain words on the <a href="/research/">research page</a>."""

# Where it appears: heading above the note under the map, in the literature view
MAP_METHOD_HEADING = "How this is drawn"


