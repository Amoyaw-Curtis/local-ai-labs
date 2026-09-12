from tools import ACTIONS

PARAM_ALIASES = {
    "file_path": "path",
    "filepath": "path",
    "filename": "path",
    "file": "path",
    "command": "cmd",
    "target_text": "find_text",
    "old_text": "find_text",
    "new_text": "replace_text",
}

def normalize_args(args: dict) -> dict:
    if not isinstance(args, dict):
        return args
    normalized = {}
    for k, v in args.items():
        key = PARAM_ALIASES.get(k, k)
        normalized[key] = v
    return normalized

def execute_step(step: dict):
    desc = step.get("description", "")
    action = step.get("action")
    raw_args = step.get("args", {})

    print("\n=== Step ===")
    print("Description:", desc)
    print("Action:", action)
    print("Args:", raw_args)

    if action not in ACTIONS:
        result = f"ERROR: Unknown action {action}"
        print("Result:", result)
        print("-" * 40)
        return result

    fn = ACTIONS[action]
    args = normalize_args(raw_args)

    try:
        if isinstance(args, dict):
            try:
                result = fn(**args)
            except TypeError:
                result = fn(*args.values())
        elif isinstance(args, list):
            result = fn(*args)
        else:
            result = fn(args)
    except Exception as e:
        result = f"ERROR executing {action}: {e}"

    print("Result:", result)
    print("-" * 40)
    return result