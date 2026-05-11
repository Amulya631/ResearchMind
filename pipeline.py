import asyncio
import json
import os
import re
from dotenv import load_dotenv
from backboard import BackboardClient

load_dotenv()


async def run_pipeline(client, query, planner_id, summarizer_id, synthesizer_id):
    print(f"\nStarting pipeline for: '{query}'")

    # ── STAGE 1: Planner breaks query into subtasks ──────────────────────
    print("  Stage 1: Planning subtasks...")
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

    print(f"  Subtasks: {subtasks}")

    # ── STAGE 2: Summarizer processes each subtask (with citations) ───────
    print("  Stage 2: Summarizing each subtask with citations...")
    all_findings = []

    for i, subtask in enumerate(subtasks):
        print(f"    [{i+1}/{len(subtasks)}] {subtask}")
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

    # ── STAGE 3: Synthesizer writes the final research brief ─────────────
    print("  Stage 3: Synthesizing final report with bibliography...")
    findings_text = (
        f"# Research Findings: {query}\n\n"
        + "\n\n---\n\n".join(all_findings)
    )

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

    # ── SAVE TO PLANNER MEMORY ────────────────────────────────────────────
    await client.add_memory(
        assistant_id=planner_id,
        content=(
            f"Completed research on: '{query}'.\n"
            f"Subtasks covered: {', '.join(subtasks)}.\n"
            f"Key conclusions: {brief[:600]}"
        ),
        metadata={"topic": query, "type": "research_session"},
    )
    print("  Conclusions saved to memory for next session")

    return brief


# ── Standalone test ───────────────────────────────────────────────────────
if __name__ == "__main__":
    from assistants import setup_assistants

    async def main():
        client, planner_id, summarizer_id, synthesizer_id = await setup_assistants()
        brief = await run_pipeline(
            client,
            query="quantum computing breakthroughs in 2025",
            planner_id=planner_id,
            summarizer_id=summarizer_id,
            synthesizer_id=synthesizer_id,
        )
        print("\n" + "=" * 60)
        print(brief)
        await client.aclose()

    asyncio.run(main())