import json
import re
# pyrefly: ignore [missing-import]
from mlx_lm import load, generate

MODEL_NAME = "mlx-community/Qwen2.5-Coder-7B-Instruct-4bit"
model, tokenizer = load(MODEL_NAME)

def format_prompt(prompt: str) -> str:
    return (
        "<|im_start|>system\n"
        "You are a helpful coding agent. "
        "Always respond with EXACTLY one valid JSON object. No explanation text outside JSON.\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"{prompt}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

def ask_llm(prompt: str) -> str:
    formatted = format_prompt(prompt)
    return generate(
        model,
        tokenizer,
        formatted,
        max_tokens=512
    )

def extract_json(text: str):
    # Strip markdown ```json ... ``` wrappers if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE)
    
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        print("RAW MODEL OUTPUT:\n", text)
        raise ValueError("Model did not return JSON.")
    return json.loads(match.group(0))