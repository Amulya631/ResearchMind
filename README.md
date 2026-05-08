# 🔬 ResearchMind

> A multi-model AI research pipeline that compounds knowledge across sessions.

Built for the **Backboard Challenges Hackathon · May 1–22, 2026**

![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Backboard](https://img.shields.io/badge/Backboard_SDK-1.5.13-green)

---

## What It Does

Type a research topic. Three AI agents pass the baton and produce a polished, structured research brief in minutes.

Close the app, come back a week later — it **remembers exactly where you left off**.

---

## How It Works

```
You → Planner → Summarizer (x3-5) → Synthesizer → Research Brief
                                                         ↓
                                              Saved to Cross-Session Memory
```

| Agent | Model | Job |
|-------|-------|-----|
| 🗂 **Planner** | Gemini 2.5 Flash | Breaks topic into 3–5 subtasks. Checks memory to skip already-covered ground. |
| 📋 **Summarizer** | Gemini 2.5 Flash | Extracts 5–8 key facts per subtask |
| ✍️ **Synthesizer** | Claude Haiku | Reads all findings, writes a polished research brief |

---

## Backboard Features Used

- **Multi-assistant architecture** — 3 permanent assistants with distinct roles
- **Multi-model routing** — Gemini Flash for speed, Claude Haiku for quality synthesis
- **Persistent cross-session memory** — Planner stores conclusions after every run
- **Inline findings synthesis** — findings passed directly to Synthesizer as structured content

---

## Demo

![ResearchMind Demo](https://github.com/Amulya631/ResearchMind/raw/main/demo.png)

**The killer feature:** Click "Memory" after a cold restart — the app recalls every topic you've ever researched, with subtasks covered and key conclusions.

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/Amulya631/ResearchMind.git
cd ResearchMind
```

**2. Install dependencies**
```bash
pip install backboard-sdk streamlit python-dotenv
```

**3. Add your API key**

Create a `.env` file in the project root:
```
BACKBOARD_API_KEY=your-key-here
```

**4. Create the assistants (run once)**
```bash
python assistants.py
```

**5. Launch the app**
```bash
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Project Structure

```
ResearchMind/
├── app.py           ← Streamlit UI with live pipeline tracking
├── assistants.py    ← Creates/reuses the 3 Backboard assistants
├── pipeline.py      ← Multi-stage pipeline logic
├── .env             ← Your API key (never committed)
├── .gitignore
└── requirements.txt
```

---

## Requirements

```
backboard-sdk>=1.5.0
streamlit>=1.32.0
python-dotenv>=1.0.0
```

---

## Live Demo

🚀 [researchmind-production.railway.app](https://researchmind-production.railway.app)

---

## License

MIT License — see [LICENSE](./LICENSE) for details.

Copyright (c) 2026 Batila Amulya

---

## Built By

**Batila Amulya** · GCP Cloud Engineer & Gen AI enthusiast  
[LinkedIn](https://linkedin.com/in/batila-amulya-5y448832b) · [GitHub](https://github.com/Amulya631)