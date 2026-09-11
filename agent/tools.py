import os
import re
import subprocess

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "project"))

def _resolve_path(path: str) -> str:
    if os.path.isabs(path):
        return path
    return os.path.join(PROJECT_DIR, path)

def strip_ansi(text: str) -> str:
    ansi_regex = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_regex.sub("", text)

def read_file(path: str):
    full_path = _resolve_path(path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as e:
        return f"ERROR reading {path}: {e}"

def write_file(path: str, content: str):
    full_path = _resolve_path(path)
    try:
        dirname = os.path.dirname(full_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Wrote file: {path}"
    except Exception as e:
        return f"ERROR writing {path}: {e}"

def replace_in_file(path: str, find_text: str, replace_text: str):
    full_path = _resolve_path(path)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"

    content_norm = content.replace("\r\n", "\n")
    find_norm = find_text.replace("\r\n", "\n").strip()
    replace_norm = replace_text.replace("\r\n", "\n")

    if find_norm not in content_norm:
        return f"ERROR: Could not find exact text block in {path}. Ensure find_text matches verbatim."

    updated = content_norm.replace(find_norm, replace_norm, 1)

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(updated)
        return f"Successfully updated {path}"
    except Exception as e:
        return f"ERROR writing replacement to {path}: {e}"

def run_command(cmd: str, timeout: int = 30):
    try:
        output = subprocess.check_output(
            cmd,
            shell=True,
            text=True,
            cwd=PROJECT_DIR,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        return {"ok": True, "output": strip_ansi(output)}
    except subprocess.TimeoutExpired:
        return {"ok": False, "output": f"Command timed out after {timeout} seconds: {cmd}"}
    except subprocess.CalledProcessError as e:
        return {"ok": False, "output": strip_ansi(e.output)}
    except Exception as e:
        return {"ok": False, "output": f"ERROR: {e}"}

def run_tests():
    # Pass --yes to avoid npx interactive prompts and --run explicitly to Vitest
    return run_command("npx --yes tsc --noEmit && npx vitest run --reporter verbose")

ACTIONS = {
    "read_file": read_file,
    "write_file": write_file,
    "replace_in_file": replace_in_file,
    "run_command": run_command,
    "run_tests": run_tests,
}