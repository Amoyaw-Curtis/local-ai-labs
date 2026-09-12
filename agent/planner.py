from llm import ask_llm, extract_json

def plan_step(goal: str, history: list[dict]):
    history_str = ""
    for idx, item in enumerate(history, 1):
        history_str += f"\n[Step {idx}]\nAction: {item['action']}\nArgs: {item['args']}\nResult:\n{item['result']}\n"

    prompt = f"""
You are an autonomous coding agent working inside a project repository to fix failing Vitest tests.

Goal:
{goal}

History of actions taken so far:
{history_str}

Tools:
- read_file: {{"path": "<relative_path>"}}
- replace_in_file: {{"path": "<relative_path>", "find_text": "<verbatim text>", "replace_text": "<new replacement text>"}}
- write_file: {{"path": "<relative_path>", "content": "<entire file content>"}}
- run_tests: {{}}

Rules:
1. NEVER modify test files inside `tests/` or configuration files. The tests define correct behavior.
2. ONLY inspect and modify application source files inside `src/`.
3. Test timeouts indicate hanging promises or uninvoked callbacks, not slow test execution. Never increase timeouts.
4. Prefer `replace_in_file` for targeted changes. `find_text` must match the file source verbatim.
5. If you haven't read the failing component in `src/`, read it before attempting an edit.
6. When all tests pass, set "done": true.

Format response strictly as a single JSON object:
{{
  "description": "short description of your next step",
  "action": "read_file" | "replace_in_file" | "write_file" | "run_tests",
  "args": {{}},
  "done": false
}}
"""
    raw = ask_llm(prompt)
    return extract_json(raw)