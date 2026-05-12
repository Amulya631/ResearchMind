import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from backboard import BackboardClient
from assistants import setup_assistants
from pipeline import run_pipeline

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp { background: #f0f2f8 !important; }
    #MainMenu, footer, header { visibility: hidden; }

    @media (max-width: 900px) {
        .hero-title { font-size: 1.8rem !important; }
        .stage-card { padding: 0.6rem 0.8rem !important; }
    }

    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] * { color: #374151 !important; }
    [data-testid="stSidebar"] strong { color: #111827 !important; }

    .stApp p, .stApp li, .stApp span, .stApp div { color: #1e293b; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
    }

    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.05;
        background: linear-gradient(135deg, #1e293b 0%, #2563eb 60%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        border-radius: 999px;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.25rem 0.75rem;
        margin-bottom: 0.75rem;
    }
    .hero-sub {
        font-size: 0.82rem;
        color: #64748b;
        margin-top: 0.4rem;
        line-height: 1.5;
    }

    /* ── TOPIC CHIPS ── */
    .chip-label {
        font-size: 0.68rem;
        font-weight: 600;
        color: #94a3b8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    /* Chip buttons — target by key prefix */
    button[kind="secondary"][data-testid*="chip_"],
    div[data-testid="column"] button[key*="chip"] {
        background: #eef2ff !important;
        border: 1.5px solid #c7d2fe !important;
        border-radius: 999px !important;
        color: #4338ca !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        padding: 0.25rem 0.8rem !important;
        min-height: 0 !important;
        height: 32px !important;
        line-height: 1.2 !important;
        box-shadow: none !important;
    }

    .stage-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.5rem;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .stage-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: #e2e8f0;
        border-radius: 3px 0 0 3px;
    }
    .stage-card.active { border-color: #93c5fd; background: #eff6ff; box-shadow: 0 4px 16px rgba(37,99,235,0.10); }
    .stage-card.active::before { background: #2563eb; }
    .stage-card.done { border-color: #a7f3d0; background: #f0fdf4; }
    .stage-card.done::before { background: #10b981; }
    .stage-label { font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #94a3b8; }
    .stage-card.active .stage-label { color: #2563eb; }
    .stage-card.done .stage-label { color: #059669; }
    .stage-name { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; font-size: 0.95rem; color: #1e293b; margin-top: 0.15rem; }
    .stage-model { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #94a3b8; margin-top: 0.2rem; }

    .stTextInput input,
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', monospace !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        caret-color: #2563eb !important;
    }
    .stTextInput input::placeholder { color: #94a3b8 !important; opacity: 1 !important; }
    .stTextInput input:focus { border-color: #2563eb !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important; color: #0f172a !important; }
    .stTextInput label { color: #475569 !important; font-size: 0.82rem !important; font-weight: 600 !important; }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
        border: none !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(37,99,235,0.30) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover { box-shadow: 0 6px 20px rgba(37,99,235,0.40) !important; transform: translateY(-1px) !important; }
    .stButton > button:not([kind="primary"]) {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #475569 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }
    .stButton > button:not([kind="primary"]):hover { border-color: #2563eb !important; color: #2563eb !important; background: #eff6ff !important; }

    .memory-chip {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.45rem;
        font-size: 0.82rem;
        color: #475569;
        border-left: 3px solid #7c3aed;
    }
    .result-header {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        border-bottom: 2px solid #f1f5f9;
        padding-bottom: 0.6rem;
        margin-bottom: 1rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #0f172a !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stMarkdown p, .stMarkdown li { color: #334155 !important; line-height: 1.75 !important; font-size: 0.95rem !important; }
    .stMarkdown strong { color: #1e293b !important; font-weight: 700 !important; }
    hr { border-color: #e2e8f0 !important; margin: 1.2rem 0 !important; }
    [data-testid="stMetric"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 0.8rem 1rem; }
    [data-testid="stMetricValue"] { color: #1e293b !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    .stAlert { border-radius: 12px !important; border-left-width: 4px !important; font-size: 0.88rem !important; }
    [data-testid="stExpander"] { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; }
    [data-testid="stExpanderDetails"] p { color: #334155 !important; }
    .stDownloadButton > button {
        background: #f8fafc !important;
        border: 1.5px solid #2563eb !important;
        color: #2563eb !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }
    .stDownloadButton > button:hover { background: #eff6ff !important; }
    .stSpinner > div { border-top-color: #2563eb !important; }
    .stCaptionContainer p, caption { color: #64748b !important; font-size: 0.78rem !important; }
    .empty-state { text-align: center; padding: 4rem 2rem; }
    .empty-icon { width: 64px; height: 64px; background: linear-gradient(135deg, #eff6ff, #f5f3ff); border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin: 0 auto 1.2rem; border: 1px solid #e2e8f0; }
    .empty-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.05rem; font-weight: 700; color: #1e293b; margin-bottom: 0.4rem; }
    .empty-sub { font-size: 0.83rem; color: #94a3b8; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)


# ── Session state defaults ───────────────────────────────────────────────
if "brief" not in st.session_state:
    st.session_state.brief = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "subtasks" not in st.session_state:
    st.session_state.subtasks = []
if "memories" not in st.session_state:
    st.session_state.memories = None
if "pipeline_stage" not in st.session_state:
    st.session_state.pipeline_stage = 0
if "selected_chip" not in st.session_state:
    st.session_state.selected_chip = ""


# ── Layout ───────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.7], gap="large")

with left:
    st.markdown('<div class="hero-badge">Backboard Challenges 2026</div>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">ResearchMind</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Three AIs. One polished brief.<br>Remembers what you have researched across sessions.</p>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TOPIC SUGGESTION CHIPS ───────────────────────────────────────────
    st.markdown('<div class="chip-label">Try a topic</div>', unsafe_allow_html=True)
    chips = [
        ("⚛ Quantum", "Quantum computing breakthroughs 2025"),
        ("🧬 CRISPR", "CRISPR gene editing in medicine"),
        ("🌊 Climate", "Climate change ocean ecosystems"),
        ("🤖 LLMs", "Large language model architectures"),
        ("⚡ Energy", "Renewable energy storage solutions"),
    ]
    chip_cols = st.columns(len(chips))
    for i, (label, full_topic) in enumerate(chips):
        with chip_cols[i]:
            if st.button(label, key=f"chip_{i}"):
                st.session_state.selected_chip = full_topic

    st.markdown("<br>", unsafe_allow_html=True)

    # ── INPUT — pre-fill from chip if clicked ────────────────────────────
    query = st.text_input(
        "Research topic",
        value=st.session_state.selected_chip,
        placeholder="e.g. quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        start = st.button("▶  Start Research", type="primary", use_container_width=True)
    with col2:
        recall = st.button("🧠 Memory", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── PIPELINE STAGES ──────────────────────────────────────────────────
    stages = [
        (
            "🗂", "Planner", "Gemini Flash · Breaks topic into subtasks", 1,
            "google", "gemini-2.5-flash",
            "Reads your cross-session memory first to avoid repeating past research, "
            "then breaks your topic into 3–5 focused subtasks. "
            "Outputs a JSON array consumed by the next stage."
        ),
        (
            "📋", "Summarizer", "Gemini Flash · Extracts key facts per subtask", 2,
            "google", "gemini-2.5-flash",
            "Processes each subtask independently. "
            "Extracts 5–8 key facts with APA citations after every finding. "
            "Adds a ## Sources section at the end of each subtask summary."
        ),
        (
            "✍️", "Synthesizer", "Claude Haiku · Writes polished report", 3,
            "anthropic", "claude-haiku-4-5-20251001",
            "Reads all findings from the Summarizer. "
            "Writes a structured research brief with executive summary, "
            "key findings by subtopic, implications, open questions, "
            "and a full APA ## References section at the end."
        ),
    ]

    st.markdown('<div class="stage-label">Pipeline stages</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    for icon, name, model_desc, stage_num, provider, model, description in stages:
        css_class = "stage-card"
        if st.session_state.pipeline_stage == stage_num:
            css_class += " active"
        elif st.session_state.pipeline_stage > stage_num:
            css_class += " done"

        status_icon = "●" if st.session_state.pipeline_stage == stage_num else (
            "✓" if st.session_state.pipeline_stage > stage_num else "○"
        )

        st.markdown(f"""
        <div class="{css_class}">
            <div class="stage-label">{status_icon} Stage {stage_num}</div>
            <div class="stage-name">{icon} {name}</div>
            <div class="stage-model">{model_desc}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"About {name}"):
            st.markdown(f"**Model:** `{provider} / {model}`")
            st.markdown(f"**Role:** {description}")

    # Subtasks preview
    if st.session_state.subtasks:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="stage-label">Subtasks identified</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for i, t in enumerate(st.session_state.subtasks):
            st.markdown(f"""
            <div class="memory-chip">
                <span style="color:#4a4a6a;margin-right:0.5rem">{i+1}.</span>{t}
            </div>
            """, unsafe_allow_html=True)

    # Stats
    if st.session_state.brief:
        st.markdown("<br>", unsafe_allow_html=True)
        word_count = len(st.session_state.brief.split())
        m1, m2 = st.columns(2)
        m1.metric("Words", f"{word_count:,}")
        m2.metric("Subtasks", len(st.session_state.subtasks))


# ── RIGHT PANEL ──────────────────────────────────────────────────────────
with right:

    # ── MEMORY RECALL ───────────────────────────────────────────────────
    if recall:
        with st.spinner("Fetching memory from Backboard..."):
            async def fetch_memories():
                client, planner_id, _, _ = await setup_assistants()
                mems = await client.get_memories(planner_id)
                await client.aclose()
                return mems
            st.session_state.memories = asyncio.run(fetch_memories())

    if st.session_state.memories is not None:
        mems = st.session_state.memories
        if mems.memories:
            seen = {}
            for m in mems.memories:
                topic = m.metadata.get("topic", None) if m.metadata else None
                if not topic:
                    continue
                if topic not in seen:
                    seen[topic] = m
            unique_mems = list(seen.values())

            st.markdown(f'<div class="result-header">🧠 Past Research Sessions ({len(unique_mems)} found)</div>', unsafe_allow_html=True)
            for m in unique_mems:
                topic = m.metadata.get("topic", "Unknown topic") if m.metadata else "Unknown topic"
                with st.expander(f"📄 {topic}"):
                    st.markdown(m.content)
                    brief_start = m.content.find("Key conclusions:")
                    if brief_start != -1:
                        st.download_button(
                            label="⬇️ Download brief excerpt",
                            data=m.content,
                            file_name=f"researchmind_{topic[:30].replace(' ', '_')}.txt",
                            mime="text/plain",
                            key=f"dl_{topic[:20]}",
                        )
        else:
            st.info("No past sessions found. Run your first query to build memory.")

    # ── PIPELINE RUN ─────────────────────────────────────────────────────
    if start and not query:
        st.warning("⚠️  Please enter a research topic first.")

    if start and query:
        st.session_state.brief = None
        st.session_state.subtasks = []
        st.session_state.memories = None
        st.session_state.last_query = query
        st.session_state.selected_chip = ""  # reset chip after run

        stage_placeholder = st.empty()

        async def run_with_stages():
            client, planner_id, summarizer_id, synthesizer_id = await setup_assistants()
            import json, re, asyncio as aio

            # STAGE 1
            st.session_state.pipeline_stage = 1
            stage_placeholder.info("🗂  **Stage 1 — Planner:** Breaking your topic into subtasks...")
            plan_thread = await client.create_thread(planner_id)
            plan_response = await client.add_message(
                thread_id=plan_thread.thread_id,
                content=f"Research topic: {query}",
                llm_provider="google",
                model_name="gemini-2.5-flash",
                memory="Auto",
                stream=False,
            )
            reply = next(
                (m["content"] for m in reversed(plan_response.messages) if m["role"] == "assistant"),
                None,
            )
            try:
                subtasks = json.loads(reply)
            except (json.JSONDecodeError, TypeError):
                match = re.search(r'\[.*?\]', reply or "", re.DOTALL)
                subtasks = json.loads(match.group()) if match else [query]
            st.session_state.subtasks = subtasks

            # STAGE 2
            st.session_state.pipeline_stage = 2
            all_findings = []
            for i, subtask in enumerate(subtasks):
                stage_placeholder.info(f"📋  **Stage 2 — Summarizer:** [{i+1}/{len(subtasks)}] {subtask}")
                sum_thread = await client.create_thread(summarizer_id)
                response = await client.add_message(
                    thread_id=sum_thread.thread_id,
                    content=(
                        f"Research subtask: {subtask}\n\n"
                        f"Remember: Every fact must have an APA citation. "
                        f"Include a ## Sources section at the end."
                    ),
                    llm_provider="google",
                    model_name="gemini-2.5-flash",
                    stream=False,
                )
                summary = next(
                    (m["content"] for m in reversed(response.messages) if m["role"] == "assistant"),
                    "",
                )
                all_findings.append(f"## {subtask}\n\n{summary}")

            # STAGE 3
            findings_text = "# Research Findings: " + query + "\n\n" + "\n\n---\n\n".join(all_findings)
            st.session_state.pipeline_stage = 3
            stage_placeholder.info("✍️  **Stage 3 — Synthesizer:** Claude Haiku is writing your report...")
            synth_thread = await client.create_thread(synthesizer_id)
            brief_response = await client.add_message(
                thread_id=synth_thread.thread_id,
                content=(
                    f"Write a polished academic research brief on: '{query}'.\n\n"
                    f"The findings below contain inline APA citations. "
                    f"Preserve all citations in the body and compile a full "
                    f"## References section at the end in alphabetical APA format.\n\n"
                    f"{findings_text}"
                ),
                llm_provider="anthropic",
                model_name="claude-haiku-4-5-20251001",
                stream=False,
            )
            brief = next(
                (m["content"] for m in reversed(brief_response.messages) if m["role"] == "assistant"),
                "",
            )

            await client.add_memory(
                assistant_id=planner_id,
                content=(
                    f"Completed research on: '{query}'.\n"
                    f"Subtasks covered: {', '.join(subtasks)}.\n"
                    f"Key conclusions: {brief[:600]}"
                ),
                metadata={"topic": query, "type": "research_session"},
            )
            await client.aclose()
            return brief

        try:
            brief = asyncio.run(run_with_stages())
            st.session_state.brief = brief
            st.session_state.pipeline_stage = 0
            stage_placeholder.success("✅  Research complete! Conclusions saved to memory.")
        except Exception as e:
            import traceback
            st.session_state.pipeline_stage = 0
            stage_placeholder.error(f"❌  Pipeline error: {e}")
            st.exception(e)
            print(traceback.format_exc())

    # ── DISPLAY BRIEF ────────────────────────────────────────────────────
    if st.session_state.brief:
        st.markdown("---")
        st.markdown('<div class="result-header">📄 Research Brief</div>', unsafe_allow_html=True)
        st.markdown(st.session_state.brief)
        st.markdown("---")

        # ── DOWNLOAD BUTTONS: TXT + PDF ───────────────────────────────
        col_txt, col_pdf, col_note = st.columns([1, 1, 2])
        safe_name = (st.session_state.last_query or query or "research")[:30].replace(' ', '_')

        with col_txt:
            st.download_button(
                label="⬇️  Download .txt",
                data=st.session_state.brief,
                file_name=f"researchmind_{safe_name}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col_pdf:
            # Generate PDF using fpdf2
            try:
                from fpdf import FPDF
                import unicodedata

                def clean(text):
                    # Replace common unicode chars with ascii equivalents
                    replacements = {
                        '—': '-', '–': '-', '‘': "'", '’': "'",
                        '“': '"', '”': '"', '•': '*', '·': '.',
                        '…': '...', ' ': ' ', '−': '-',
                    }
                    for orig, repl in replacements.items():
                        text = text.replace(orig, repl)
                    return ''.join(
                        c if ord(c) < 256 else unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode()
                        for c in text
                    )

                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_margins(20, 20, 20)

                # Title
                pdf.set_font("Helvetica", "B", 20)
                pdf.set_text_color(15, 23, 42)
                pdf.multi_cell(0, 10, clean("ResearchMind — Research Brief"), align="C")
                pdf.ln(2)

                # Topic
                pdf.set_font("Helvetica", "", 11)
                pdf.set_text_color(100, 116, 139)
                topic_line = st.session_state.last_query or query or "Research"
                pdf.multi_cell(0, 7, clean(f"Topic: {topic_line}"), align="C")
                pdf.ln(6)

                # Divider
                pdf.set_draw_color(226, 232, 240)
                pdf.set_line_width(0.5)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(6)

                # Brief content
                for line in st.session_state.brief.split('\n'):
                    line = line.strip()
                    if not line:
                        pdf.ln(3)
                        continue
                    if line.startswith('## '):
                        pdf.set_font("Helvetica", "B", 13)
                        pdf.set_text_color(37, 99, 235)
                        pdf.multi_cell(0, 8, clean(line[3:]))
                        pdf.ln(1)
                    elif line.startswith('### '):
                        pdf.set_font("Helvetica", "B", 11)
                        pdf.set_text_color(51, 65, 85)
                        pdf.multi_cell(0, 7, clean(line[4:]))
                        pdf.ln(1)
                    elif line.startswith('# '):
                        pdf.set_font("Helvetica", "B", 16)
                        pdf.set_text_color(15, 23, 42)
                        pdf.multi_cell(0, 10, clean(line[2:]))
                        pdf.ln(2)
                    elif line.startswith('- ') or line.startswith('* '):
                        pdf.set_font("Helvetica", "", 10)
                        pdf.set_text_color(51, 65, 85)
                        pdf.multi_cell(0, 6, clean("  • " + line[2:]))
                    else:
                        pdf.set_font("Helvetica", "", 10)
                        pdf.set_text_color(71, 85, 105)
                        pdf.multi_cell(0, 6, clean(line))

                # Footer
                pdf.ln(6)
                pdf.set_draw_color(226, 232, 240)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(4)
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(148, 163, 184)
                pdf.cell(0, 5, "Generated by ResearchMind - Backboard Challenges Hackathon 2026", align="C")

                pdf_bytes = bytes(pdf.output())

                st.download_button(
                    label="📄  Download PDF",
                    data=pdf_bytes,
                    file_name=f"researchmind_{safe_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except ImportError:
                st.caption("Install fpdf2 for PDF export")

        with col_note:
            st.caption("💾 Conclusions saved to Planner memory. Click **Memory** to verify.")

    # ── EMPTY STATE ──────────────────────────────────────────────────────
    if not st.session_state.brief and not st.session_state.memories:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔬</div>
            <div class="empty-title">Enter a topic and hit Start Research</div>
            <div class="empty-sub">
                Three AIs collaborate and produce a polished brief.<br>
                Results persist across sessions via Backboard memory.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'Plus Jakarta Sans\',sans-serif;font-weight:800;font-size:1.1rem;color:#0f172a;margin-bottom:0">ResearchMind</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.7rem;color:#64748b;letter-spacing:0.1em;text-transform:uppercase;margin-top:0">Backboard Challenges · May 2026</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown("""
- 🗂 **Planner** (Gemini Flash) — breaks topic into 3–5 subtasks, checks memory to avoid repeats
- 📋 **Summarizer** (Gemini Flash) — extracts 5–8 key facts with APA citations per subtask
- ✍️ **Synthesizer** (Claude Haiku) — synthesizes findings, writes polished brief with references
- 🧠 **Memory** — conclusions saved to Planner after every session
    """)
    st.markdown("---")
    st.markdown("**Backboard features used**")
    st.markdown("""
- Multi-assistant architecture
- Multi-model routing
- Inline findings synthesis
- Persistent cross-session memory
    """)
    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.72rem;color:#94a3b8;">Built with Backboard SDK v1.5.13<br>for the Backboard Challenges Hackathon</p>',
        unsafe_allow_html=True,
    )