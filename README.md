<div align="center">

<img src="https://img.shields.io/badge/Backboard_Challenges-May_2026-6366f1?style=for-the-badge" />

# ResearchMind

### A multi-agent AI research pipeline with cross-session memory

*Type a topic. Three AIs collaborate. Get a polished research brief.*  
*Come back tomorrow — it remembers everything.*

<br/>

[![MIT License](https://img.shields.io/badge/License-MIT-2563eb?style=flat-square)](./LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-2563eb?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-ff4b4b?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Backboard SDK](https://img.shields.io/badge/Backboard_SDK-1.5.13-10b981?style=flat-square)](https://backboard.io)

<br/>

[Live Demo](#live-demo) · [Quick Start](#quick-start) · [How It Works](#how-it-works) · [Architecture](#architecture)

</div>

---

## Overview

ResearchMind is a multi-model AI pipeline built on the Backboard SDK. It decomposes any research topic into focused subtasks, processes each independently, and synthesizes the findings into a structured research brief — while persisting what you have researched across sessions so it never covers the same ground twice.

> **Built for the Backboard Challenges Hackathon · May 1–22, 2026**

---

## Live Demo

🚀 **[researchmind-production.railway.app](https://researchmind-production-04c7.up.railway.app)**

---

## How It Works

```
Input Topic
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  Stage 1 — Planner          (Gemini 2.5 Flash)      │
│  Reads memory → generates 3–5 focused subtasks      │
│  Skips anything already researched in past sessions │
└──────────────────────┬──────────────────────────────┘
                       │  subtasks[]
                       ▼
┌─────────────────────────────────────────────────────┐
│  Stage 2 — Summarizer       (Gemini 2.5 Flash)      │
│  Processes each subtask independently               │
│  Extracts 5–8 key facts per subtask                 │
└──────────────────────┬──────────────────────────────┘
                       │  findings[]
                       ▼
┌─────────────────────────────────────────────────────┐
│  Stage 3 — Synthesizer      (Claude Haiku)          │
│  Reads all findings                                 │
│  Writes polished research brief with headers        │
└──────────────────────┬──────────────────────────────┘
                       │  brief
                       ▼
            Research Brief Output
                       │
                       ▼
         Saved to Planner Cross-Session Memory
```

---

## Architecture

| Agent | Model | Responsibility |
|---|---|---|
| **Planner** | Gemini 2.5 Flash | Decomposes topic into subtasks. Reads memory to avoid repeating past research. |
| **Summarizer** | Gemini 2.5 Flash | Processes each subtask independently. Returns 5–8 key facts per subtask. |
| **Synthesizer** | Claude Haiku | Synthesizes all findings into a structured, polished research brief. |

### Backboard Features Used

| Feature | Usage |
|---|---|
| Multi-assistant architecture | 3 permanent assistants with distinct system prompts and roles |
| Multi-model routing | Gemini Flash for speed at scale, Claude Haiku for synthesis quality |
| Persistent cross-session memory | Planner stores topic + subtasks + conclusions after every session |
| Cross-thread memory recall | New sessions automatically skip previously covered subtasks |

---

## Quick Start

**1. Clone**
```bash
git clone https://github.com/Amulya631/ResearchMind.git
cd ResearchMind
```

**2. Install dependencies**
```bash
pip install backboard-sdk streamlit python-dotenv
```

**3. Configure environment**

Create a `.env` file in the project root:
```env
BACKBOARD_API_KEY=your-backboard-api-key
```

**4. Create assistants** *(run once — idempotent, safe to re-run)*
```bash
python assistants.py
```

**5. Run**
```bash
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Project Structure

```
ResearchMind/
├── app.py            Streamlit UI — live stage tracking, memory panel, download
├── assistants.py     Creates / reuses the 3 Backboard assistants (idempotent)
├── pipeline.py       Core pipeline logic — Planner → Summarizer → Synthesizer
├── requirements.txt  Python dependencies
├── .env              API key — never committed
└── .gitignore
```

---

## Requirements

```
backboard-sdk>=1.5.0
streamlit>=1.32.0
python-dotenv>=1.0.0
```

---

## The Cross-Session Memory Feature

This is what separates ResearchMind from a standard chatbot.

After every pipeline run, the Planner stores:
- The topic researched
- Every subtask covered
- Key conclusions from the brief

On the next run, the Planner reads this memory before generating subtasks — so it never repeats research. Close the app, restart your machine, come back days later — the context is still there.

---

## License

MIT License — see [LICENSE](./LICENSE) for full terms.

Copyright © 2026 Batila Amulya

---

<div align="center">

Built with [Backboard](https://backboard.io) · [Streamlit](https://streamlit.io) · [Google Gemini](https://deepmind.google/gemini) · [Anthropic Claude](https://anthropic.com)

**[Batila Amulya](https://linkedin.com/in/batila-amulya-5y448832b)** · GCP Cloud Engineer & Gen AI

</div>