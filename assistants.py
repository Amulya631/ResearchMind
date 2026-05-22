import asyncio
import os
from dotenv import load_dotenv
from backboard import BackboardClient

load_dotenv()

# ─── Helper: find existing assistant by name or create/update it ──────────
async def get_or_create_assistant(client, name, system_prompt, force_update=False):
    existing = await client.list_assistants()
    for a in existing:
        if a.name == name:
            if force_update:
                # Delete old and recreate with new prompt
                await client.delete_assistant(assistant_id=a.assistant_id)
                print(f"  Deleted old assistant: {name} (prompt updated)")
            else:
                print(f"  Reusing existing assistant: {name} ({a.assistant_id})")
                return a.assistant_id

    created = await client.create_assistant(
        name=name,
        system_prompt=system_prompt,
    )
    print(f"  Created assistant: {name} ({created.assistant_id})")
    return created.assistant_id


async def setup_assistants(force_update=False):
    client = BackboardClient(api_key=os.environ['BACKBOARD_API_KEY'], timeout=180.0)

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
        force_update=False,  # Planner prompt unchanged — never recreate
    )

    # ── Assistant 2: Summarizer ──────────────────────────────────────────
    summarizer_id = await get_or_create_assistant(
        client,
        name="ResearchMind Summarizer",
        system_prompt=(
            "You are an academic research summarizer. Given a specific research subtask, "
            "provide 5 to 8 key facts or findings about it. "
            "STRICT RULES:\n"
            "1. Every single fact MUST include an APA citation immediately after it.\n"
            "2. Citation format: (Author Last Name, Year, *Publication/Journal Name*)\n"
            "3. If you cannot cite a verifiable source for a fact, do not include that fact.\n"
            "4. Use real authors, real publication years, and real journal/book names.\n"
            "5. At the end of your response, add a '## Sources' section listing all "
            "cited works in full APA format.\n\n"
            "Output format example:\n"
            "- Pink dolphins have unfused cervical vertebrae allowing 90-degree head turns. "
            "(Werth, 2000, *Marine Mammal Science*)\n\n"
            "## Sources\n"
            "Werth, A. J. (2000). Feeding in marine mammals. *Marine Mammal Science*, 16(3), 487-510."
        ),
        force_update=force_update,
    )

    # ── Assistant 3: Synthesizer ─────────────────────────────────────────
    synthesizer_id = await get_or_create_assistant(
        client,
        name="ResearchMind Synthesizer",
        system_prompt=(
            "You are an expert research analyst. You will be given findings "
            "from a structured research pipeline where every fact has an APA citation. "
            "Write a polished, well-structured research brief with:\n"
            "1. An executive summary (3-4 sentences).\n"
            "2. Key findings by subtopic (use clear headers). "
            "Preserve all inline citations (Author, Year) from the findings.\n"
            "3. Implications and open questions.\n"
            "4. A consolidated '## References' section at the end — collect ALL unique "
            "citations from the findings and list them in full APA format, "
            "alphabetically by author last name.\n\n"
            "Be precise and confident. Never drop citations — they are essential for "
            "academic use."
        ),
        force_update=force_update,
    )

    return client, planner_id, summarizer_id, synthesizer_id


if __name__ == "__main__":
    import sys
    force = "--update" in sys.argv
    client, p, s, sy = asyncio.run(setup_assistants(force_update=force))
    print(f"\nAll assistants ready:")
    print(f"  Planner:     {p}")
    print(f"  Summarizer:  {s}")
    print(f"  Synthesizer: {sy}")