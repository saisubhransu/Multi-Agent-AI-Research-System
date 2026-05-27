import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink:      #0e0e0e;
    --paper:    #f5f0e8;
    --cream:    #ede8dc;
    --accent:   #c84b31;
    --muted:    #7a7060;
    --border:   #d4cfc3;
    --step1:    #2d6a4f;
    --step2:    #1d4e89;
    --step3:    #6b3fa0;
    --step4:    #c84b31;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--paper) !important;
    color: var(--ink) !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(circle at 15% 20%, rgba(200,75,49,0.06) 0%, transparent 50%),
        radial-gradient(circle at 85% 75%, rgba(45,106,79,0.06) 0%, transparent 50%);
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--cream) !important; }

/* ── Typography ── */
h1, h2, h3 {
    font-family: 'Instrument Serif', Georgia, serif !important;
    color: var(--ink) !important;
}

p, div, span, label {
    font-family: 'DM Sans', sans-serif !important;
}

code, pre {
    font-family: 'DM Mono', monospace !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}

.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.6rem;
}

.hero-title {
    font-family: 'Instrument Serif', Georgia, serif;
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    font-weight: 400;
    line-height: 1.1;
    color: var(--ink);
    margin: 0 0 0.8rem;
}

.hero-title em {
    font-style: italic;
    color: var(--accent);
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: var(--muted);
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #fff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(200,75,49,0.1) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #b0a898 !important;
}

/* ── Button ── */
.stButton > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2rem !important;
    transition: background 0.2s, transform 0.1s !important;
    box-shadow: 3px 3px 0 var(--accent) !important;
    width: 100%;
}

.stButton > button:hover {
    background: var(--accent) !important;
    transform: translate(-1px, -1px) !important;
    box-shadow: 4px 4px 0 var(--ink) !important;
}

.stButton > button:active {
    transform: translate(1px, 1px) !important;
    box-shadow: 2px 2px 0 var(--accent) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    box-shadow: 2px 2px 0 var(--border);
    transition: box-shadow 0.2s;
}

.step-card.active {
    border-color: var(--accent);
    box-shadow: 3px 3px 0 var(--accent);
    animation: pulse-border 1.5s ease-in-out infinite;
}

.step-card.done {
    border-color: #2d6a4f;
    box-shadow: 2px 2px 0 #2d6a4f;
}

@keyframes pulse-border {
    0%, 100% { box-shadow: 3px 3px 0 var(--accent); }
    50%       { box-shadow: 5px 5px 0 var(--accent); }
}

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.5rem;
}

.step-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 2px;
    font-weight: 500;
}

.step-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.15rem;
    color: var(--ink);
    margin: 0;
}

.step-desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--muted);
    margin: 0;
}

/* ── Result panels ── */
.result-panel {
    background: var(--cream);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
    margin-top: 1rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    line-height: 1.7;
    color: #2a2520;
    max-height: 320px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

.result-panel::-webkit-scrollbar { width: 4px; }
.result-panel::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Final report ── */
.report-container {
    background: #fff;
    border: 1.5px solid var(--ink);
    border-radius: 6px;
    box-shadow: 5px 5px 0 var(--ink);
    padding: 2rem 2.4rem;
    margin-top: 2rem;
}

.report-title {
    font-family: 'Instrument Serif', serif;
    font-size: 1.8rem;
    color: var(--ink);
    margin-bottom: 0.3rem;
}

.report-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
}

.report-body {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    line-height: 1.8;
    color: #1a1714;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Critic panel ── */
.critic-container {
    background: #fff9f5;
    border: 1.5px solid var(--step4);
    border-radius: 6px;
    box-shadow: 4px 4px 0 var(--step4);
    padding: 1.6rem 2rem;
    margin-top: 1.5rem;
}

/* ── Status row ── */
.status-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    color: var(--muted);
    margin-bottom: 2rem;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: blink 1.2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}

/* ── Expander tweaks ── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    background: var(--cream) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Metric cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}

.metric-card {
    flex: 1;
    min-width: 120px;
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    text-align: center;
}

.metric-num {
    font-family: 'Instrument Serif', serif;
    font-size: 2rem;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 0.2rem;
}

.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

STEPS = [
    {
        "num": "01",
        "title": "Search Agent",
        "desc": "Finds recent, reliable information across the web",
        "color": "#2d6a4f",
        "bg": "#edf7f2",
        "key": "search_result",
    },
    {
        "num": "02",
        "title": "Reader Agent",
        "desc": "Scrapes and extracts deep content from top sources",
        "color": "#1d4e89",
        "bg": "#edf2fb",
        "key": "scraped_content",
    },
    {
        "num": "03",
        "title": "Writer Agent",
        "desc": "Synthesises research into a structured report",
        "color": "#6b3fa0",
        "bg": "#f5f0fb",
        "key": "report",
    },
    {
        "num": "04",
        "title": "Critic Agent",
        "desc": "Reviews the report for quality, gaps and accuracy",
        "color": "#c84b31",
        "bg": "#fdf1ee",
        "key": "feedback",
    },
]


def badge(num: str, color: str, bg: str) -> str:
    return (
        f'<span class="step-badge" '
        f'style="background:{bg};color:{color};border:1px solid {color}20">'
        f'Step {num}</span>'
    )


def render_step_card(step: dict, state_key: str, status: str) -> None:
    """status: 'waiting' | 'active' | 'done'"""
    css_class = {"waiting": "step-card", "active": "step-card active", "done": "step-card done"}[status]

    icon = {"waiting": "○", "active": "◉", "done": "●"}[status]
    icon_color = {"waiting": "#b0a898", "active": step["color"], "done": "#2d6a4f"}[status]

    st.markdown(f"""
    <div class="{css_class}">
        <div class="step-header">
            {badge(step["num"], step["color"], step["bg"])}
            <span style="font-size:1rem;color:{icon_color}">{icon}</span>
            <p class="step-title">{step["title"]}</p>
        </div>
        <p class="step-desc">{step["desc"]}</p>
    </div>
    """, unsafe_allow_html=True)

    if status == "done" and state_key in st.session_state.get("pipeline_state", {}):
        content = st.session_state["pipeline_state"][state_key]
        with st.expander("View output", expanded=False):
            st.markdown(
                f'<div class="result-panel">{content}</div>',
                unsafe_allow_html=True,
            )


def run_pipeline_with_ui(topic: str, placeholders: list) -> dict:
    state = {}

    # ── Step 1: Search ─────────────────────────────────────────────────────────
    with placeholders[0]:
        render_step_card(STEPS[0], "search_result", "active")
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_result"] = search_result["messages"][-1].content
    with placeholders[0]:
        render_step_card(STEPS[0], "search_result", "done")

    # ── Step 2: Reader ─────────────────────────────────────────────────────────
    with placeholders[1]:
        render_step_card(STEPS[1], "scraped_content", "active")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result["messages"][-1].content
    with placeholders[1]:
        render_step_card(STEPS[1], "scraped_content", "done")

    # ── Step 3: Writer ─────────────────────────────────────────────────────────
    with placeholders[2]:
        render_step_card(STEPS[2], "report", "active")
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    with placeholders[2]:
        render_step_card(STEPS[2], "report", "done")

    # ── Step 4: Critic ─────────────────────────────────────────────────────────
    with placeholders[3]:
        render_step_card(STEPS[3], "feedback", "active")
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    with placeholders[3]:
        render_step_card(STEPS[3], "feedback", "done")

    return state


# ── Layout ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <p class="hero-label">Multi-Agent Research System</p>
    <h1 class="hero-title">Research<em>Mind</em></h1>
    <p class="hero-sub">
        Four specialised AI agents work in sequence — searching, reading,
        writing, and critiquing — to deliver a thorough research report on
        any topic.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        "topic",
        label_visibility="collapsed",
        placeholder="Enter a research topic — e.g. 'Quantum computing in 2025'",
        key="topic_input",
    )
with col_btn:
    run = st.button("Run Pipeline", key="run_btn")

st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)

# ── Main columns: pipeline tracker | results ──────────────────────────────────
left, right = st.columns([2, 3], gap="large")

with left:
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:0.7rem;'
        'letter-spacing:0.2em;text-transform:uppercase;color:#7a7060;'
        'margin-bottom:1rem">Pipeline Stages</p>',
        unsafe_allow_html=True,
    )

    placeholders = [st.empty() for _ in STEPS]

    # Default rendering (waiting state)
    if "pipeline_state" not in st.session_state:
        for i, step in enumerate(STEPS):
            with placeholders[i]:
                render_step_card(step, step["key"], "waiting")
    else:
        for i, step in enumerate(STEPS):
            with placeholders[i]:
                render_step_card(step, step["key"], "done")

with right:
    results_placeholder = st.empty()

    if "pipeline_state" not in st.session_state:
        results_placeholder.markdown(
            '<div style="text-align:center;padding:5rem 2rem;color:#b0a898;">'
            '<p style="font-family:\'Instrument Serif\',serif;font-size:1.6rem;'
            'margin-bottom:0.5rem">Awaiting research topic</p>'
            '<p style="font-family:\'DM Sans\',sans-serif;font-size:0.9rem">'
            'Enter a topic and click Run Pipeline to begin.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

# ── Run ───────────────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        results_placeholder.empty()

        with right:
            st.markdown(
                f'<div class="status-row">'
                f'<span class="status-dot"></span>'
                f'Researching <strong style="color:#0e0e0e;margin:0 4px">{topic}</strong>'
                f'— pipeline running…'
                f'</div>',
                unsafe_allow_html=True,
            )

        start = time.time()

        # Reset step cards to waiting
        for i, step in enumerate(STEPS):
            with placeholders[i]:
                render_step_card(step, step["key"], "waiting")

        pipeline_state = run_pipeline_with_ui(topic, placeholders)
        st.session_state["pipeline_state"] = pipeline_state
        st.session_state["pipeline_topic"] = topic

        elapsed = time.time() - start

        # ── Show results in right column ───────────────────────────────────────
        with right:
            # Metrics
            word_count = len(pipeline_state.get("report", "").split())
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="metric-num">{elapsed:.0f}s</div>
                    <div class="metric-label">Total time</div>
                </div>
                <div class="metric-card">
                    <div class="metric-num">{word_count:,}</div>
                    <div class="metric-label">Report words</div>
                </div>
                <div class="metric-card">
                    <div class="metric-num">4</div>
                    <div class="metric-label">Agents run</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Final report
            st.markdown(f"""
            <div class="report-container">
                <p class="report-label">Research Report</p>
                <p class="report-title">{topic}</p>
                <div class="report-body">{pipeline_state.get("report", "")}</div>
            </div>
            """, unsafe_allow_html=True)

            # Critic feedback
            st.markdown(f"""
            <div class="critic-container">
                <p style="font-family:'DM Mono',monospace;font-size:0.65rem;
                          letter-spacing:0.2em;text-transform:uppercase;
                          color:#c84b31;margin-bottom:0.6rem">
                    Critic Review
                </p>
                <p style="font-family:'Instrument Serif',serif;font-size:1.2rem;
                          margin-bottom:0.8rem;color:#0e0e0e">
                    Quality Assessment
                </p>
                <div class="report-body">{pipeline_state.get("feedback", "")}</div>
            </div>
            """, unsafe_allow_html=True)

        st.success(f"Pipeline completed in {elapsed:.1f}s — report ready above.")

# ── Restore previous results on rerun ─────────────────────────────────────────
elif "pipeline_state" in st.session_state:
    ps = st.session_state["pipeline_state"]
    topic_used = st.session_state.get("pipeline_topic", "")
    word_count = len(ps.get("report", "").split())

    with right:
        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="metric-num">{word_count:,}</div>
                <div class="metric-label">Report words</div>
            </div>
            <div class="metric-card">
                <div class="metric-num">4</div>
                <div class="metric-label">Agents run</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="report-container">
            <p class="report-label">Research Report</p>
            <p class="report-title">{topic_used}</p>
            <div class="report-body">{ps.get("report", "")}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="critic-container">
            <p style="font-family:'DM Mono',monospace;font-size:0.65rem;
                      letter-spacing:0.2em;text-transform:uppercase;
                      color:#c84b31;margin-bottom:0.6rem">
                Critic Review
            </p>
            <p style="font-family:'Instrument Serif',serif;font-size:1.2rem;
                      margin-bottom:0.8rem;color:#0e0e0e">
                Quality Assessment
            </p>
            <div class="report-body">{ps.get("feedback", "")}</div>
        </div>
        """, unsafe_allow_html=True)