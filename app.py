# ============================================================
# PERSONASKILL AI — app.py
# VERSION: 2.0
# ============================================================

import streamlit as st
import io
from fpdf import FPDF
from datetime import date
import re
import tempfile
import os

# ─────────────────────────────────────────
# SECTION 1: CONSTANTS
# ─────────────────────────────────────────
APP_TITLE        = "PersonaSkill AI"
APP_VERSION      = "v2.0"
MAX_SCORE        = 100
HYBRID_THRESHOLD = 5
QUESTION_COUNT   = 7

# ─────────────────────────────────────────
# SECTION 2: PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide"
)

# ─────────────────────────────────────────
# SECTION 3: QUESTIONS DATA
# ─────────────────────────────────────────
QUESTIONS = [
    {
        "id": "Q1",
        "title": "🔧 Troubleshooting",
        "desc": "When your WiFi stops working, do you test each device one by one before calling support?"
    },
    {
        "id": "Q2",
        "title": "🗺️ Navigation",
        "desc": "When driving to a new place, do you mentally map shortcuts and alternate routes on the fly?"
    },
    {
        "id": "Q3",
        "title": "📦 Inventory",
        "desc": "At home, do you naturally track which supplies are running low before they run out?"
    },
    {
        "id": "Q4",
        "title": "🎯 Domino Effect",
        "desc": "Before making a decision, do you instinctively think about what chain of events it might trigger?"
    },
    {
        "id": "Q5",
        "title": "⚡ Optimization",
        "desc": "When doing a repetitive task, do you automatically look for a faster or easier way to do it?"
    },
    {
        "id": "Q6",
        "title": "🔍 Detection",
        "desc": "In a conversation or situation, do you often notice small details or inconsistencies others miss?"
    },
    {
        "id": "Q7",
        "title": "🌀 Pattern Intuition",
        "desc": "In everyday life, do you often notice recurring patterns — in people's habits, prices, or events?"
    },
]

# ─────────────────────────────────────────
# SECTION 4: DOMAIN LIST
# ─────────────────────────────────────────
DOMAINS = [
    "⚙️ Engineering & Tech",
    "🔬 Science & Healthcare",
    "💼 Business & Finance",
    "🎨 Creative & Design",
    "📚 Education & Research",
    "🏛️ Law & Administration",
    "🛒 Sales & Marketing",
    "🌱 Exploring / Not Sure",
]

# ─────────────────────────────────────────
# SECTION 5: PERSONA MAP & SUMMARIES
# ─────────────────────────────────────────
PERSONA_MAP = {
    "Analytical & Data": {
        (75, 100): "🧠 The Data Architect",
        (50, 74):  "🔍 The Pattern Hunter",
        (0,  49):  "📊 The Detail Observer",
    },
    "Operations & Logic": {
        (75, 100): "⚙️ The Efficiency Ninja",
        (50, 74):  "🔧 The Systems Builder",
        (0,  49):  "📋 The Process Tracker",
    },
    "Strategy & AI-Thinking": {
        (75, 100): "🚀 The AI Strategist",
        (50, 74):  "🎯 The Logic Visionary",
        (0,  49):  "💡 The Strategic Thinker",
    },
}

PERSONA_SUMMARY = {
    "🧠 The Data Architect":      "You naturally build mental models from raw information. You see structure where others see chaos.",
    "🔍 The Pattern Hunter":      "You instinctively spot trends and connections. Data is your second language.",
    "📊 The Detail Observer":     "You notice what others miss. Your precision and attention to detail is a rare gift.",
    "⚙️ The Efficiency Ninja":    "You're wired to eliminate waste and streamline everything. Speed + accuracy is your superpower.",
    "🔧 The Systems Builder":     "You think in processes and workflows. You naturally turn messy situations into clean systems.",
    "📋 The Process Tracker":     "You bring order to chaos. Tracking, organizing, and following through is where you shine.",
    "🚀 The AI Strategist":       "You think several moves ahead. Connecting big-picture strategy with intelligent execution is your zone.",
    "🎯 The Logic Visionary":     "You blend creative thinking with structured logic. You see solutions before others see the problem.",
    "💡 The Strategic Thinker":   "You have a natural instinct for planning and foresight. You rarely act without a mental blueprint.",
    "🌐 The Renaissance Analyst": "You're a rare multi-dimensional thinker — equally strong in data, logic, and strategy.",
}

# ─────────────────────────────────────────
# SECTION 6: DOMAIN CAREER MAP
# 8 Domains x 3 Categories + Hybrid = 80 unique outcomes
# ─────────────────────────────────────────
DOMAIN_CAREER_MAP = {
    "⚙️ Engineering & Tech": {
        "Analytical & Data": {
            "roles": [
                ("Data Analyst",       "Your eye for patterns turns raw data into engineering decisions."),
                ("QA / Test Engineer", "Your detail-detection catches bugs before they reach production."),
                ("Systems Analyst",    "You break down complex systems and find what's not working."),
            ],
            "skills": ["Python", "SQL", "Power BI"]
        },
        "Operations & Logic": {
            "roles": [
                ("DevOps Engineer",     "Your optimization mindset keeps systems running efficiently."),
                ("Civil Site Engineer", "You manage workflows, resources, and timelines on ground."),
                ("Mechanical Engineer", "Your process thinking fits perfectly in design-to-production pipelines."),
            ],
            "skills": ["Linux", "AutoCAD", "Project Management"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("AI/ML Engineer",       "Your pattern intuition gives you an edge in building intelligent systems."),
                ("Tech Product Manager", "You connect engineering capabilities with strategic business goals."),
                ("R&D Engineer",         "Your foresight drives innovation before the market demands it."),
            ],
            "skills": ["Machine Learning", "Python", "System Design"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Technical Product Manager", "You bridge engineering and strategy — a rare and valuable combination."),
                ("Solutions Architect",       "Your multi-dimensional thinking designs systems end-to-end."),
                ("Tech Consultant",           "You solve complex technical problems with strategic clarity."),
            ],
            "skills": ["System Design", "Python", "Project Management"]
        },
    },

    "🔬 Science & Healthcare": {
        "Analytical & Data": {
            "roles": [
                ("Medical Lab Technician", "Your precision in detecting anomalies ensures accurate diagnoses."),
                ("Clinical Data Analyst",  "You turn patient data into insights that improve treatment outcomes."),
                ("Epidemiologist",         "Your pattern recognition tracks disease spread before it peaks."),
            ],
            "skills": ["Medical Statistics", "Excel", "SPSS"]
        },
        "Operations & Logic": {
            "roles": [
                ("Hospital Administrator", "Your systems thinking keeps complex healthcare operations smooth."),
                ("Pharmacist",             "Your inventory and process tracking ensures zero medication errors."),
                ("Healthcare Coordinator", "You optimize patient flow and resource allocation naturally."),
            ],
            "skills": ["Healthcare Management", "ERP Systems", "Process Improvement"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Medical Researcher",    "Your ability to see connections drives breakthrough discoveries."),
                ("Health Policy Analyst", "You think ahead on how policies will impact public health outcomes."),
                ("Biotech Strategist",    "You spot opportunities in science before they become mainstream."),
            ],
            "skills": ["Research Methodology", "Data Analysis", "Public Health"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Clinical Research Manager", "You combine analytical rigor with operational excellence in trials."),
                ("Health Informatics Lead",   "Your hybrid thinking connects patient data with hospital strategy."),
                ("Public Health Consultant",  "You analyze, operate, and strategize — all at once."),
            ],
            "skills": ["Research Methods", "Healthcare Management", "Data Analysis"]
        },
    },

    "💼 Business & Finance": {
        "Analytical & Data": {
            "roles": [
                ("Financial Analyst", "Your detail orientation spots risks others miss in balance sheets."),
                ("Auditor",           "Your inconsistency detection makes you a natural at finding discrepancies."),
                ("Business Analyst",  "You translate data patterns into business recommendations."),
            ],
            "skills": ["Excel", "SQL", "Financial Modeling"]
        },
        "Operations & Logic": {
            "roles": [
                ("Operations Manager",   "Your optimization mindset keeps business processes lean and efficient."),
                ("Supply Chain Manager", "You naturally track inventory, logistics, and vendor performance."),
                ("Project Manager",      "Your systematic thinking delivers projects on time and on budget."),
            ],
            "skills": ["ERP Systems", "Lean Six Sigma", "MS Project"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Strategy Consultant", "Your foresight helps businesses make smarter long-term moves."),
                ("Investment Analyst",  "Your pattern recognition spots market trends before they peak."),
                ("Entrepreneur",        "You see opportunities others don't — and plan 3 steps ahead."),
            ],
            "skills": ["Strategic Planning", "Market Research", "Financial Forecasting"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Management Consultant",        "Your multi-dimensional thinking solves complex business problems."),
                ("CFO / Finance Director",       "You combine number precision with big-picture financial strategy."),
                ("Business Development Manager", "You analyze markets, run operations, and think strategically."),
            ],
            "skills": ["Financial Modeling", "Strategic Planning", "Communication"]
        },
    },

    "🎨 Creative & Design": {
        "Analytical & Data": {
            "roles": [
                ("UX Researcher",      "Your detail observation reveals what users truly need vs what they say."),
                ("Brand Analyst",      "You spot visual and market patterns that shape brand strategy."),
                ("Content Strategist", "Your analytical mind finds what content works and why."),
            ],
            "skills": ["Figma", "Google Analytics", "User Research"]
        },
        "Operations & Logic": {
            "roles": [
                ("Creative Project Manager", "You keep creative teams organized without killing the creative flow."),
                ("Production Designer",      "Your process thinking ensures designs move smoothly from concept to output."),
                ("Art Director",             "You build systems that maintain visual consistency across all channels."),
            ],
            "skills": ["Adobe Suite", "Project Management", "Brand Guidelines"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Creative Director",  "You see the big picture — connecting creativity with business impact."),
                ("AI Content Creator", "Your pattern intuition helps you craft content that resonates at scale."),
                ("Design Strategist",  "You anticipate design trends before they become mainstream."),
            ],
            "skills": ["Design Thinking", "AI Tools", "Brand Strategy"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Creative Technologist", "You blend design thinking with analytical and strategic skills."),
                ("UX Strategist",         "Your hybrid mind connects user research with business outcomes."),
                ("Brand Consultant",      "You analyze brands, design solutions, and think long-term."),
            ],
            "skills": ["Design Thinking", "Analytics", "Brand Strategy"]
        },
    },

    "📚 Education & Research": {
        "Analytical & Data": {
            "roles": [
                ("Research Analyst",    "Your pattern recognition drives meaningful academic discoveries."),
                ("Curriculum Designer", "You spot gaps in learning materials others overlook."),
                ("Academic Evaluator",  "Your detail orientation ensures quality in assessments and outcomes."),
            ],
            "skills": ["Research Methods", "SPSS", "Academic Writing"]
        },
        "Operations & Logic": {
            "roles": [
                ("School Administrator", "Your systems thinking keeps educational institutions running smoothly."),
                ("Training Manager",     "You design and optimize learning processes for maximum effectiveness."),
                ("E-learning Developer", "You build structured, logical learning experiences for online platforms."),
            ],
            "skills": ["LMS Platforms", "Instructional Design", "Project Management"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Education Consultant", "You see where education is heading and help institutions adapt."),
                ("EdTech Strategist",    "Your foresight connects pedagogy with emerging technologies."),
                ("Learning Scientist",   "You research how people learn and design better systems around it."),
            ],
            "skills": ["EdTech Tools", "Data Analysis", "Strategic Planning"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Academic Director",      "You combine research depth with institutional strategy."),
                ("EdTech Product Manager", "Your hybrid thinking builds learning tools that actually work."),
                ("Training Consultant",    "You design, deliver, and strategize learning programs."),
            ],
            "skills": ["Instructional Design", "Research", "Strategic Planning"]
        },
    },

    "🏛️ Law & Administration": {
        "Analytical & Data": {
            "roles": [
                ("Legal Analyst",      "Your inconsistency detection is invaluable in case research and review."),
                ("Compliance Officer", "You naturally spot regulatory gaps before they become violations."),
                ("Policy Researcher",  "Your pattern recognition connects legal precedents with current cases."),
            ],
            "skills": ["Legal Research", "Documentation", "MS Office"]
        },
        "Operations & Logic": {
            "roles": [
                ("Court Administrator", "You keep complex legal workflows organized and on schedule."),
                ("HR Manager",          "Your process tracking ensures smooth people operations."),
                ("Government Officer",  "Your systematic thinking navigates bureaucratic processes efficiently."),
            ],
            "skills": ["Administration", "Policy Implementation", "ERP Systems"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Corporate Lawyer",      "You think 10 moves ahead in negotiations and contract strategy."),
                ("Policy Strategist",     "Your foresight shapes laws and regulations that stand the test of time."),
                ("Legal Tech Consultant", "You connect legal expertise with technology to modernize law practice."),
            ],
            "skills": ["Strategic Thinking", "Legal Tech", "Negotiation"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Legal Operations Manager", "You run legal departments with both analytical and strategic precision."),
                ("Policy Advisor",           "Your hybrid mind shapes policies that are practical and future-proof."),
                ("Compliance Strategist",    "You connect regulatory detail with long-term organizational strategy."),
            ],
            "skills": ["Legal Research", "Strategic Planning", "Communication"]
        },
    },

    "🛒 Sales & Marketing": {
        "Analytical & Data": {
            "roles": [
                ("Marketing Analyst", "You find patterns in campaign data that others miss entirely."),
                ("CRM Analyst",       "Your detail tracking turns customer data into retention strategies."),
                ("SEO Specialist",    "Your pattern recognition decodes search algorithms naturally."),
            ],
            "skills": ["Google Analytics", "Excel", "CRM Tools"]
        },
        "Operations & Logic": {
            "roles": [
                ("Sales Operations Manager", "You optimize the entire sales process for maximum efficiency."),
                ("Campaign Manager",         "You run multi-channel campaigns with military-level coordination."),
                ("Retail Manager",           "Your inventory and process tracking keeps stores running smoothly."),
            ],
            "skills": ["CRM", "Marketing Automation", "Excel"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Growth Strategist",    "You spot market opportunities and design campaigns before trends peak."),
                ("Brand Strategist",     "Your big-picture thinking builds brands that last decades."),
                ("AI Marketing Manager", "You blend data intuition with AI tools to scale marketing impact."),
            ],
            "skills": ["Growth Hacking", "AI Marketing Tools", "Strategic Planning"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("Growth Manager",            "You analyze data, run campaigns, and think strategically — all at once."),
                ("Marketing Director",        "Your multi-dimensional thinking drives full-funnel marketing impact."),
                ("Product Marketing Manager", "You connect product, data, and go-to-market strategy seamlessly."),
            ],
            "skills": ["Growth Strategy", "Analytics", "Marketing Automation"]
        },
    },

    "🌱 Exploring / Not Sure": {
        "Analytical & Data": {
            "roles": [
                ("Data Analyst",       "Strong analytical thinkers thrive here regardless of background."),
                ("Research Assistant", "Your observation skills make you valuable in any research setting."),
                ("Business Analyst",   "A versatile role that values pattern recognition above all else."),
            ],
            "skills": ["Excel", "SQL", "Critical Thinking"]
        },
        "Operations & Logic": {
            "roles": [
                ("Operations Coordinator", "Your process mindset is valuable in any industry."),
                ("Project Coordinator",    "Every field needs someone who can organize and execute efficiently."),
                ("Logistics Analyst",      "Your optimization instinct fits perfectly in supply chain roles."),
            ],
            "skills": ["MS Office", "Project Management", "Communication"]
        },
        "Strategy & AI-Thinking": {
            "roles": [
                ("Management Trainee",  "Your strategic thinking is the foundation every organization wants."),
                ("Startup Founder",     "You see problems and solutions others don't — that's entrepreneurship."),
                ("AI Tools Consultant", "Help businesses adopt AI tools — no deep tech background needed."),
            ],
            "skills": ["Strategic Thinking", "AI Tools", "Communication"]
        },
        "Hybrid Thinker": {
            "roles": [
                ("General Management Trainee", "Your versatile thinking makes you adaptable to any industry."),
                ("Entrepreneur / Founder",     "Hybrid thinkers make the best founders — you see the full picture."),
                ("Strategy & Ops Analyst",     "A role that values both analytical and strategic multi-tasking."),
            ],
            "skills": ["Critical Thinking", "MS Office", "Communication"]
        },
    },
}

# ─────────────────────────────────────────
# SECTION 7: SCORING FUNCTIONS
# ─────────────────────────────────────────
def calculate_scores(ans):
    Q1 = ans['Q1']; Q2 = ans['Q2']; Q3 = ans['Q3']
    Q4 = ans['Q4']; Q5 = ans['Q5']; Q6 = ans['Q6']; Q7 = ans['Q7']
    analytical = round((Q1*0.4 + Q3*0.3 + Q6*0.3) * 10, 1)
    operations = round((Q2*0.4 + Q5*0.4 + Q1*0.2) * 10, 1)
    strategy   = round((Q4*0.4 + Q7*0.4 + Q5*0.2) * 10, 1)
    return min(analytical, MAX_SCORE), min(operations, MAX_SCORE), min(strategy, MAX_SCORE)


def get_persona(dominant_category, score, is_hybrid):
    if is_hybrid:
        return "🌐 The Renaissance Analyst"
    for (low, high), title in PERSONA_MAP[dominant_category].items():
        if low <= score <= high:
            return title


def get_dominant_secondary(analytical, operations, strategy):
    scores = {
        "Analytical & Data":      analytical,
        "Operations & Logic":     operations,
        "Strategy & AI-Thinking": strategy
    }
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    dominant  = sorted_scores[0]
    secondary = sorted_scores[1]
    is_hybrid = (dominant[1] - secondary[1]) <= HYBRID_THRESHOLD
    return scores, dominant, secondary, is_hybrid



def clean_for_pdf(text):
    if not text:
        return ""

    # ✅ Remove emojis
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U0001F900-\U0001F9FF"
        u"\U00002600-\U000026FF"
        u"\U0001FA00-\U0001FA6F"
        u"\uFE0F"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)

    # ✅ Replace problematic unicode
    replacements = {
        "\u2014": "-", "\u2013": "-",
        "\u2018": "'", "\u2019": "'",
        "\u201C": '"', "\u201D": '"',
        "\u2026": "...", "\u00A0": " ",
        "\u2022": "-", "\u2039": "<", "\u203A": ">",
    }

    for orig, repl in replacements.items():
        text = text.replace(orig, repl)

    # 🔥 CRITICAL FIX: Force latin-1 safe text
    text = text.encode("latin-1", "ignore").decode("latin-1")

    return text.strip()



# ✅ Custom PDF class for footer (FIXED WAY)
class MyPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(180, 180, 180)
        self.cell(
            0, 10,
            f"PersonaSkill AI  |  Page {self.page_no()}  |  {APP_TITLE} {APP_VERSION}",
            align="C"
        )


def generate_pdf(user_name, domain, persona, summary, a, o, s, dominant, secondary, is_hybrid, roadmap):

    def safe(text):
        return clean_for_pdf(str(text))

    persona_clean   = safe(persona)
    summary_clean   = safe(summary)
    secondary_clean = safe(secondary[0] if secondary else "")
    domain_clean    = safe(domain)
    name_clean      = safe(user_name) if user_name else "Friend"

    # ✅ Use custom class
    pdf = MyPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── PAGE 1: COVER ──
    pdf.add_page()
    pdf.ln(20)

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(67, 97, 238)
    pdf.cell(0, 12, safe("PersonaSkill AI"), ln=True, align="C")

    pdf.ln(4)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, safe("Your Career Intelligence Report"), ln=True, align="C")

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 11)
    pdf.cell(0, 8, safe(f"Prepared for: {name_clean}"), ln=True, align="C")

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, safe(f"Domain: {domain_clean}"), ln=True, align="C")

    pdf.ln(10)
    pdf.set_draw_color(67, 97, 238)
    pdf.set_line_width(0.8)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())

    pdf.ln(14)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, persona_clean, ln=True, align="C")

    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 8, summary_clean, align="C")

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, safe(f"Secondary Strength: {secondary_clean}"), ln=True, align="C")

    pdf.ln(14)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())

    pdf.ln(12)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, safe(f"Generated on: {date.today().strftime('%B %d, %Y')}"), ln=True, align="C")

    pdf.ln(4)
    pdf.cell(0, 8, safe("Powered by behavioral pattern analysis"), ln=True, align="C")

    # ── PAGE 2: SCORES ──
    pdf.add_page()
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(67, 97, 238)
    pdf.cell(0, 12, safe("Your Psychometric Scores"), ln=True)

    pdf.ln(4)
    pdf.set_draw_color(67, 97, 238)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)

    for category, score, desc in [
        ("Analytical & Data",      a, "Measures your ability to observe details, identify inconsistencies, and analyze patterns."),
        ("Operations & Logic",     o, "Measures your ability to optimize processes, navigate systems, and execute efficiently."),
        ("Strategy & AI-Thinking", s, "Measures your ability to think ahead, recognize patterns, and make high-impact decisions."),
    ]:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 9, safe(category), ln=True)

        filled = int(score / 10)
        bar = "[" + ("=" * filled) + ("-" * (10 - filled)) + "]"

        pdf.set_font("Helvetica", "", 13)
        pdf.set_text_color(67, 97, 238)
        pdf.cell(0, 8, safe(f"{bar}   {score} / 100"), ln=True)

        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(110, 110, 110)
        pdf.multi_cell(0, 6, safe(desc))

        pdf.ln(6)

    if is_hybrid:
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(67, 97, 238)
        pdf.cell(0, 8, safe("Note: You are a Hybrid Thinker!"), ln=True)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6, safe(
            "Your top two scores are within 5 points - "
            "meaning you have rare multi-dimensional thinking ability."
        ))

    # ── PAGE 3: CAREER ROADMAP ──
    pdf.add_page()
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(67, 97, 238)
    pdf.cell(0, 12, safe("Your Career Roadmap"), ln=True)

    pdf.ln(4)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, safe(f"Field: {domain_clean}"), ln=True)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 9, safe("Top Career Roles For You"), ln=True)

    pdf.ln(3)
    for role, reason in roadmap["roles"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 7, safe(f"  {role}"), ln=True)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(110, 110, 110)
        pdf.multi_cell(0, 6, safe(f"  {reason}"))

        pdf.ln(3)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 9, safe("Skills to Build Next"), ln=True)

    pdf.ln(3)
    for skill in roadmap["skills"]:
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(67, 97, 238)
        pdf.cell(0, 7, safe(f"  - {skill}"), ln=True)

    pdf.ln(10)
    pdf.set_draw_color(67, 97, 238)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(67, 97, 238)
    pdf.multi_cell(0, 8, safe(
        '"Your natural wiring is your biggest career advantage. Now go build on it."'
    ))

    # ✅ FINAL FIX: Proper PDF output
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        pdf.output(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, 'rb') as f:
        pdf_bytes = f.read()

    os.unlink(tmp_path)
    return pdf_bytes

# ─────────────────────────────────────────
# SECTION 9: MAIN HEADER
# ─────────────────────────────────────────
st.title("🧠 PersonaSkill AI")
st.subheader("Discover the skills you were born with — not just the ones you studied for.")
st.divider()

# ─────────────────────────────────────────
# SECTION 10: USER NAME + DOMAIN SELECTOR
# ─────────────────────────────────────────
col_name, col_domain = st.columns(2)

with col_name:
    user_name = st.text_input(
        "👤 Your Name (optional)",
        placeholder="e.g. Abu Aasif",
        max_chars=50
    )

with col_domain:
    selected_domain = st.selectbox(
        "🌐 Select Your Field / Domain",
        options=DOMAINS,
        index=0,
        help="Choose the field you work in or are interested in."
    )

st.divider()

# ─────────────────────────────────────────
# SECTION 11: QUESTIONS + TRACK ANSWERS
# ─────────────────────────────────────────
answers        = {}
answered_count = 0

st.markdown("### 📝 Answer the questions below honestly:")
st.caption("Rate each situation from 0 (Not at all like me) to 10 (Exactly like me)")
st.write("")

for q in QUESTIONS:
    st.markdown(f"**{q['title']}**")
    st.caption(q['desc'])
    val = st.slider(
        label="Rate yourself",
        min_value=0,
        max_value=10,
        value=0,
        key=q['id']
    )
    answers[q['id']] = val
    if val > 0:
        answered_count += 1
    st.divider()

# ─────────────────────────────────────────
# SECTION 12: SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.header("💡 About")
    st.write(
        "PersonaSkill AI analyzes your everyday behavior patterns "
        "to reveal your hidden natural talents and ideal career paths."
    )
    st.divider()
    if user_name:
        st.markdown(f"**👤 Hey, {user_name}!**")
    st.markdown(f"**🌐 Field:** {selected_domain}")
    st.divider()
    st.markdown("**📊 Your Progress**")
    st.progress(answered_count / QUESTION_COUNT)
    st.caption(f"{answered_count} of {QUESTION_COUNT} questions answered")
    st.divider()
    st.warning("⚠️ This is a behavioral insight tool, not a clinical assessment.")
    st.divider()
    st.caption(f"{APP_VERSION} | Built with Streamlit")

# ─────────────────────────────────────────
# SECTION 13: VALIDATION + CALCULATE BUTTON
# ─────────────────────────────────────────
all_zero = all(v == 0 for v in answers.values())

st.markdown("### ✨ Ready to meet your inner genius?")

if all_zero:
    st.warning("⚠️ Please answer at least a few questions to get meaningful results.")

calculate = st.button(
    label="🚀 Calculate My Skills",
    disabled=all_zero,
    use_container_width=True
)

# ─────────────────────────────────────────
# SECTION 14: RESULTS
# ─────────────────────────────────────────
if calculate:

    a, o, s = calculate_scores(answers)
    scores, dominant, secondary, is_hybrid = get_dominant_secondary(a, o, s)
    persona = get_persona(dominant[0], dominant[1], is_hybrid)
    summary = PERSONA_SUMMARY[persona]

    # Domain-specific roadmap
    domain_data = DOMAIN_CAREER_MAP[selected_domain]
    roadmap     = domain_data["Hybrid Thinker"] if is_hybrid else domain_data[dominant[0]]

    st.balloons()
    st.divider()

    # Personalized heading
    greeting = f"## 🏆 {user_name}'s Results" if user_name else "## 🏆 Your Results"
    st.markdown(greeting)

    # 3 Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🔍 Analytical & Data",      value=f"{a} / 100")
        st.progress(a / 100)
    with col2:
        st.metric(label="⚙️ Operations & Logic",     value=f"{o} / 100")
        st.progress(o / 100)
    with col3:
        st.metric(label="🚀 Strategy & AI-Thinking", value=f"{s} / 100")
        st.progress(s / 100)

    st.write("")

    # Persona Card
    name_line = f"Hey **{user_name}**, you are" if user_name else "You are"
    st.success(f"""
### {name_line} —
# {persona}

{summary}

🥈 *Secondary strength: **{secondary[0]}***
🌐 *Field: **{selected_domain}***
    """)

    # Career Roadmap
    with st.expander("🗺️ View Your Career Roadmap", expanded=True):
        st.markdown("### 💼 Top Career Roles For You")
        st.caption(f"Matched to your field: **{selected_domain}**")
        st.write("")

        r1, r2, r3 = st.columns(3)
        for col, (role, reason) in zip([r1, r2, r3], roadmap["roles"]):
            with col:
                st.markdown(f"**{role}**")
                st.caption(reason)

        st.divider()

        st.markdown("### 🛠️ Skills to Build Next")
        skill_cols = st.columns(len(roadmap["skills"]))
        for col, skill in zip(skill_cols, roadmap["skills"]):
            with col:
                st.info(f"📌 {skill}")

        st.divider()
        st.markdown(
            "> 💬 *Your natural wiring is your biggest career advantage. Now go build on it.*"
        )

    # Share Button
    st.divider()
    share_name = user_name if user_name else "I"
    share_text = (
        f"{share_name} just discovered my career persona on PersonaSkill AI!\n\n"
        f"I am {persona}\n"
        f"Field: {selected_domain}\n\n"
        f"Find out yours: https://personaskill-ai.streamlit.app"
    )
    st.markdown("### 📣 Share Your Persona")
    st.code(share_text, language=None)
    st.caption("👆 Copy this and share on LinkedIn or WhatsApp!")

    # Retake Button
    st.divider()
    if st.button("🔄 Retake Assessment", use_container_width=True):
        st.rerun()

    # PDF Download
    st.divider()
    with st.container():
        st.markdown("### 📄 Download Your Full Report")
        st.caption("3-page PDF — scores, persona, and domain-specific career roadmap.")

        pdf_bytes = generate_pdf(
            user_name  = user_name,
            domain     = selected_domain,
            persona    = persona,
            summary    = summary,
            a          = a,
            o          = o,
            s          = s,
            dominant   = dominant,
            secondary  = secondary,
            is_hybrid  = is_hybrid,
            roadmap    = roadmap
        )

        file_name = (
            f"PersonaSkill_AI_{user_name.replace(' ', '_')}_Report.pdf"
            if user_name else "PersonaSkill_AI_Report.pdf"
        )

        st.download_button(
            label            = "📥 Download My PDF Report",
            data             = pdf_bytes,
            file_name        = file_name,
            mime             = "application/pdf",
            use_container_width=True
        )