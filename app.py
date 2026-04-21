# ============================================================
# PERSONASKILL AI — app.py
# ============================================================

import streamlit as st
import io
from fpdf import FPDF
from datetime import date
import re

# ─────────────────────────────────────────
# SECTION 1: CONSTANTS (no magic numbers)
# ─────────────────────────────────────────
APP_TITLE        = "PersonaSkill AI"
APP_VERSION      = "v1.0"
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
# SECTION 4: PERSONA MAP & SUMMARIES
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
# SECTION 5: CAREER ROADMAP DATA
# ─────────────────────────────────────────
CAREER_MAP = {
    "Analytical & Data": {
        "roles": [
            ("Data Analyst",     "Your eye for detail turns raw numbers into business decisions."),
            ("BI Developer",     "You naturally build systems to track and visualize performance."),
            ("ML Ops Engineer",  "Your troubleshooting instinct fits perfectly in model pipelines."),
        ],
        "skills": ["Python", "Power BI", "SQL"]
    },
    "Operations & Logic": {
        "roles": [
            ("Supply Chain Analyst", "Your optimization mindset keeps operations lean and efficient."),
            ("Process Engineer",     "You naturally redesign broken workflows into clean systems."),
            ("Operations Manager",   "Your tracking instinct makes you a natural leader of teams."),
        ],
        "skills": ["Excel", "ERP Systems", "Lean Six Sigma"]
    },
    "Strategy & AI-Thinking": {
        "roles": [
            ("AI Product Manager",  "You connect big-picture strategy with intelligent execution."),
            ("Strategy Consultant", "Your foresight helps businesses make smarter long-term moves."),
            ("Data Scientist",      "Your pattern intuition gives you an edge in building AI models."),
        ],
        "skills": ["Machine Learning", "Prompt Engineering", "Python"]
    },
    "Hybrid Thinker": {
        "roles": [
            ("Analytics Consultant", "You bridge the gap between data, operations, and strategy."),
            ("Business Analyst",     "Your multi-dimensional thinking solves complex business problems."),
            ("Product Analyst",      "You combine logic and creativity to build better products."),
        ],
        "skills": ["SQL", "Tableau", "Communication"]
    },
}

# ─────────────────────────────────────────
# SECTION 6: SCORING FUNCTIONS
# ─────────────────────────────────────────
def calculate_scores(ans):
    """Calculate weighted scores for all 3 categories."""
    Q1 = ans['Q1']
    Q2 = ans['Q2']
    Q3 = ans['Q3']
    Q4 = ans['Q4']
    Q5 = ans['Q5']
    Q6 = ans['Q6']
    Q7 = ans['Q7']

    analytical = round((Q1*0.4 + Q3*0.3 + Q6*0.3) * 10, 1)
    operations = round((Q2*0.4 + Q5*0.4 + Q1*0.2) * 10, 1)
    strategy   = round((Q4*0.4 + Q7*0.4 + Q5*0.2) * 10, 1)

    # Cap scores at MAX_SCORE
    analytical = min(analytical, MAX_SCORE)
    operations = min(operations, MAX_SCORE)
    strategy   = min(strategy,   MAX_SCORE)

    return analytical, operations, strategy


def get_persona(dominant_category, score, is_hybrid):
    """Return persona title based on dominant category and score."""
    if is_hybrid:
        return "🌐 The Renaissance Analyst"
    for (low, high), title in PERSONA_MAP[dominant_category].items():
        if low <= score <= high:
            return title


def get_dominant_secondary(analytical, operations, strategy):
    """Return sorted scores, dominant, secondary, and hybrid flag."""
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
    """Remove emojis and replace special characters for Helvetica compatibility."""
    import re

    # Step 1 — Remove emojis
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

    # Step 2 — Replace special punctuation with ASCII equivalents
    replacements = {
        "\u2014": "-",   # em dash        —  → -
        "\u2013": "-",   # en dash        –  → -
        "\u2018": "'",   # left quote     '  → '
        "\u2019": "'",   # right quote    '  → '
        "\u201C": '"',   # left d-quote   "  → "
        "\u201D": '"',   # right d-quote  "  → "
        "\u2026": "...", # ellipsis       …  → ...
        "\u00A0": " ",   # non-break space   → space
        "\u2022": "-",   # bullet         •  → -
        "\u2039": "<",   # single left angle
        "\u203A": ">",   # single right angle
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)

    return text.strip()

def generate_pdf(persona, summary, a, o, s, dominant, secondary, is_hybrid):
    """Generate a 3-page PDF report in memory and return as bytes."""

    # --- Strip emojis for Helvetica font compatibility ---
    persona_clean   = clean_for_pdf(persona)
    dominant_clean  = clean_for_pdf(dominant[0])
    secondary_clean = clean_for_pdf(secondary[0])
    summary_clean   = clean_for_pdf(summary)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ══════════════════════════════════════
    # PAGE 1 — COVER PAGE
    # ══════════════════════════════════════
    pdf.add_page()
    pdf.ln(20)

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(67, 97, 238)
    pdf.cell(0, 12, "PersonaSkill AI", ln=True, align="C")

    pdf.ln(4)

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Your Career Intelligence Report", ln=True, align="C")

    pdf.ln(14)

    pdf.set_draw_color(67, 97, 238)
    pdf.set_line_width(0.8)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())

    pdf.ln(14)

    # Persona title — emoji removed
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 12, persona_clean, ln=True, align="C")

    pdf.ln(6)

    # Summary — emoji removed
    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 8, summary_clean, align="C")

    pdf.ln(10)

    # Secondary — emoji removed
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, f"Secondary Strength: {secondary_clean}", ln=True, align="C")

    pdf.ln(14)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(12)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, f"Generated on: {date.today().strftime('%B %d, %Y')}", ln=True, align="C")
    pdf.ln(4)
    pdf.cell(0, 8, "Powered by behavioral pattern analysis", ln=True, align="C")

    # ══════════════════════════════════════
    # PAGE 2 — SCORE BREAKDOWN
    # ══════════════════════════════════════
    pdf.add_page()
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(67, 97, 238)
    pdf.cell(0, 12, "Your Psychometric Scores", ln=True)
    pdf.ln(4)

    pdf.set_draw_color(67, 97, 238)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    score_data = [
        (
            "Analytical & Data", a,
            "Measures your ability to observe details, identify inconsistencies, and analyze patterns."
        ),
        (
            "Operations & Logic", o,
            "Measures your ability to optimize processes, navigate systems, and execute efficiently."
        ),
        (
            "Strategy & AI-Thinking", s,
            "Measures your ability to think ahead, recognize patterns, and make high-impact decisions."
        ),
    ]

    for category, score, description in score_data:
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 9, category, ln=True)

        # BAAD MEIN (safe ASCII only):
        filled = int(score / 10)
        empty  = 10 - filled
        bar    = "[" + ("=" * filled) + ("-" * empty) + "]"
        pdf.set_font("Helvetica", "", 13) 
        pdf.set_text_color(67, 97, 238)
        pdf.cell(0, 8, f"{bar}   {score} / 100", ln=True)

        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(110, 110, 110)
        pdf.multi_cell(0, 6, description)
        pdf.ln(6)

    if is_hybrid:
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(67, 97, 238)
        pdf.cell(0, 8, "Note: You are a Hybrid Thinker!", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6,
            "Your top two scores are within 5 points — "
            "meaning you have rare multi-dimensional thinking ability."
        )

    # ══════════════════════════════════════
    # PAGE 3 — CAREER ROADMAP
    # ══════════════════════════════════════
    pdf.add_page()
    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(67, 97, 238)
    pdf.cell(0, 12, "Your Career Roadmap", ln=True)
    pdf.ln(4)

    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    roadmap_key  = "Hybrid Thinker" if is_hybrid else dominant[0]
    roadmap_data = CAREER_MAP[roadmap_key]

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 9, "Top Career Roles For You", ln=True)
    pdf.ln(3)

    for role, reason in roadmap_data["roles"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 7, f"  {clean_for_pdf(role)}", ln=True)

        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(110, 110, 110)
        pdf.multi_cell(0, 6, f"  {clean_for_pdf(reason)}")
        pdf.ln(3)

    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 9, "Skills to Build Next", ln=True)
    pdf.ln(3)

    for skill in roadmap_data["skills"]:
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(67, 97, 238)
        pdf.cell(0, 7, f"  - {skill}", ln=True)

    pdf.ln(10)
    pdf.set_draw_color(67, 97, 238)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "I", 12)
    pdf.set_text_color(67, 97, 238)
    pdf.multi_cell(0, 8,
        '"Your natural wiring is your biggest career advantage. Now go build on it."'
    )

    # ══════════════════════════════════════
    # FOOTER — page numbers
    # ══════════════════════════════════════
    for i in range(1, pdf.page_no() + 1):
        pdf.page = i
        pdf.set_y(-15)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(180, 180, 180)
        pdf.cell(0, 10,
            f"PersonaSkill AI  |  Page {i}  |  {APP_TITLE} {APP_VERSION}",
            align="C"
        )

    return bytes(pdf.output())

# ─────────────────────────────────────────
# SECTION 7: MAIN HEADER
# ─────────────────────────────────────────
st.title("🧠 PersonaSkill AI")
st.subheader("Discover the skills you were born with — not just the ones you studied for.")
st.divider()

# ─────────────────────────────────────────
# SECTION 8: RENDER QUESTIONS + TRACK ANSWERS
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
# SECTION 9: SIDEBAR (uses live answered_count)
# ─────────────────────────────────────────
with st.sidebar:
    st.header("💡 About")
    st.write(
        "PersonaSkill AI analyzes your everyday behavior patterns "
        "to reveal your hidden natural talents and ideal career paths."
    )
    st.divider()

    st.markdown("**📊 Your Progress**")
    st.progress(answered_count / QUESTION_COUNT)
    st.caption(f"{answered_count} of {QUESTION_COUNT} questions answered")
    st.divider()

    st.warning("⚠️ This is a behavioral insight tool, not a clinical assessment.")
    st.divider()

    st.caption(f"{APP_VERSION} | Built with Streamlit")

# ─────────────────────────────────────────
# SECTION 10: VALIDATION + CALCULATE BUTTON
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
# SECTION 11: RESULTS + ROADMAP (inside if calculate)
# ─────────────────────────────────────────
if calculate:

    # --- Calculate scores ---
    a, o, s = calculate_scores(answers)
    scores, dominant, secondary, is_hybrid = get_dominant_secondary(a, o, s)
    persona = get_persona(dominant[0], dominant[1], is_hybrid)
    summary = PERSONA_SUMMARY[persona]

    # --- Celebration ---
    st.balloons()

    st.divider()
    st.markdown("## 🏆 Your Results")

    # --- 3 Metric Cards ---
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

    # --- Persona Card ---
    st.success(f"""
### {persona}

{summary}

🥈 *Secondary strength: **{secondary[0]}***
    """)

    # ─────────────────────────────────────────
    # SECTION 12: CAREER ROADMAP
    # ─────────────────────────────────────────

    # Pick correct roadmap key
    roadmap_key = "Hybrid Thinker" if is_hybrid else dominant[0]
    roadmap     = CAREER_MAP[roadmap_key]

    with st.expander("🗺️ View Your Career Roadmap", expanded=True):

        st.markdown("### 💼 Top Career Roles For You")
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

    # ─────────────────────────────────────────
    # SECTION 14: PDF DOWNLOAD BUTTON
    # ─────────────────────────────────────────

    st.divider()

    with st.container():
        st.markdown("### 📄 Download Your Full Report")
        st.caption("Get a beautifully formatted 3-page PDF with your scores, persona, and career roadmap.")

        pdf_bytes = generate_pdf(
            persona    = persona,
            summary    = summary,
            a          = a,
            o          = o,
            s          = s,
            dominant   = dominant,
            secondary  = secondary,
            is_hybrid  = is_hybrid
        )

        st.download_button(
            label     = "📥 Download My PDF Report",
            data      = pdf_bytes,
            file_name = "PersonaSkill_AI_Report.pdf",
            mime      = "application/pdf",
            use_container_width=True
        )
    