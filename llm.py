import os
import json
from groq import Groq
from toolbox import WorkspaceToolbox
from typing import Any
from config import API_KEY, DEFAULT_MODEL

client = Groq(api_key=API_KEY)

def llm_decide(
    goal: str,
    toolbox: WorkspaceToolbox,
    history: list[dict[str, str]],
    step: int,
    max_steps: int,
    model: str,
) -> dict[str, Any]:
    history_text = json.dumps(history[-8:], indent=2)
    prompt = f"""
You are an autonomous coding agent working inside a local workspace.
Your job is to complete the user's goal by choosing exactly one action at a time.

Rules:
- Always return exactly one JSON object.
- JSON keys must be: action, payload, reasoning.
- reasoning must be short.
- Use tools to inspect files before making assumptions.
- Keep file paths relative to the workspace.
- If the goal is complete, use the finish action.
- Do not invent tool results.
- Prefer small, reversible file edits.

Goal:
{goal}

Step:
{step} of {max_steps}

Scratch Notes:
{toolbox.get_notes()}

Recent History:
{history_text}

{toolbox.describe_tools()}

Valid response examples:
{{"action":"list_files","payload":{{"path":".","recursive":true,"limit":50}},"reasoning":"Inspect the workspace first."}}
{{"action":"read_file","payload":{{"path":"app.py"}},"reasoning":"Read the main file."}}
{{"action":"write_file","payload":{{"path":"todo.txt","content":"hello"}},"reasoning":"Create an output file."}}
{{"action":"finish","payload":{{"response":"Task completed successfully."}},"reasoning":"The goal is complete."}}

Return only JSON.
""".strip()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        timeout=45,
    )
    text = response.choices[0].message.content
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        raise ValueError(f"Model returned non-JSON output: {text}")