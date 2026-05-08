import asyncio
import json
import os
import re
import tempfile
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
        model_name="gemini-1.5-flash",
        memory="Auto",
        stream=False,
    )

    # SDK returns messages as dicts — use ["role"] and ["content"], not .role / .content
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

    # ── STAGE 2: Summarizer processes each subtask ───────────────────────
    print("  Stage 2: Summarizing each subtask...")
    all_findings = []

    for i, subtask in enumerate(subtasks):
        print(f"    [{i+1}/{len(subtasks)}] {subtask}")
        sum_thread = await client.create_thread(summarizer_id)
        response = await client.add_message(
            thread_id=sum_thread.thread_id,
            content=f"Research subtask: {subtask}",
            llm_provider="google",
            model_name="gemini-1.5-flash",
            stream=False,
        )
        summary = next(
            (m["content"] for m in reversed(response.messages) if m["role"] == "assistant"),
            "",
        )
        all_findings.append(f"## {subtask}\n\n{summary}")

    # ── STAGE 3: Synthesizer writes the final research brief ─────────────
    # Pass findings inline in message content — avoids RAG/upload issues
    print("  Stage 3: Synthesizing final report...")
    findings_text = "# Research Findings: " + query + "\n\n" + "\n\n---\n\n".join(all_findings)

    synth_thread = await client.create_thread(synthesizer_id)
    brief_response = await client.add_message(
        thread_id=synth_thread.thread_id,
        content=(
            f"Write a polished research brief on: '{query}'.\n\n"
            f"Here are the research findings:\n\n{findings_text}"
        ),
        llm_provider="anthropic",
        model_name="claude-haiku-4-5-20251001",
        stream=False,
    )

    brief = next(
        (m["content"] for m in reversed(brief_response.messages) if m["role"] == "assistant"),
        "",
    )


    #