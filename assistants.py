import asyncio
import os
from dotenv import load_dotenv
from backboard import BackboardClient

load_dotenv()

# ─── Helper: find existing assistant by name or create a new one ──────────
async def get_or_create_assistant(client, name, system_prompt):
    existing = await client.list_assistants()
    for a in existing:
        if a.name == name:
            print(f"  Reusing existing assistant: {name} ({a.assistant_id})")
            return a.assistant_id
    created = await client.create_assistant(
        name=name,
        system_prompt=system_prompt,
    )
    print(f"  Created assistant: {name} ({created.assistant_id})")
    return created.assistant_id


async def setup_assistants():
    client = BackboardClient(api_key=os.environ['BACKBOARD_API_KEY'], timeout=120.0)

    # ── Assistant 1: Planner ─────────────────────────────────────────────
    planner_id = await get_or_create_assistant(
        client,
        name="ResearchMind Planner",
        system_prompt=(
            "You are a research planner. Given a topic, break it into exactly "
            "3 to 5 specific research subtasks. Before generating subtasks, "
            "check your memory for any past research on this topic and exclude "
            "subtasks that have already been covered. "
            "Output ONLY a valid JSON array of strings. No explanation, "
            "no markdown, no preamble. Example output: "
            '["Subtask one", "Subtask two", "Subtask three"]'
        ),
    )

    # ── Assistant 2: Summarizer ──────────────────────────────────────────
    summarizer_id = await get_or_create_assistant(
        client,
        name="ResearchMind Summarizer",
        system_prompt=(
            "You are a research summarizer. Given a specific research subtask, "
            "provide 5 to 8 key facts or findings about it. "
            "Be specific, cite figures and dates where relevant. "
            "Format your output as a clean markdown list starting with '- '. "
            "No preamble, no conclusion, just the facts."
        ),
    )

    # ── Assistant 3: Synthesizer ─────────────────────────────────────────
    synthesizer_id = await get_or_create_assistant(
        client,
        name="ResearchMind Synthesizer",
        system_prompt=(
            "You are an expert research analyst. You will be given findings "
            "from a structured research pipeline. "
            "Write a polished, well-structured research brief with: "
            "1. An executive summary (3-4 sentences). "
            "2. Key findings by subtopic (use clear headers). "
            "3. Implications and open questions. "
            "Be precise and confident."
        ),
    )

    return client, planner_id, summarizer_id, synthesizer_id


if __name__ == "__main__":
    client, p, s, sy = asyncio.run(setup_assistants())
    print(f"\nAll assistants ready:")
    print(f"  Planner:     {p}")
    print(f"  Summarizer:  {s}")
    print(f"  Synthesizer: {sy}")