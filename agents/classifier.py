import json
from models import call_model
from prompts.classifier_prompt import CLASSIFIER_SYSTEM, build_classifier_prompt


def clean_json_response(raw: str) -> str:
    """
    Strips common LLM artifacts before JSON parsing:
    - Markdown code fences (```json ... ```)
    - Leading/trailing whitespace
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        # drop first line (```json or ```) and last line (```)
        cleaned = "\n".join(lines[1:-1]).strip()
    return cleaned


def run_classifier(user_request: str, mood: str = "") -> dict:
    """
    Takes the raw user story request and optional mood.
    Returns a structured plan dict.
    """
    print("\n[Classifier] Analyzing your request and building a story plan...")

    prompt = build_classifier_prompt(user_request, mood=mood)
    raw_response = call_model(prompt, system=CLASSIFIER_SYSTEM)

    try:
        cleaned = clean_json_response(raw_response)
        plan = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"[Classifier] Failed to parse story plan from model response.\n"
            f"Raw response was:\n{raw_response}\n"
            f"JSON error: {e}"
        )

    required_keys = ["category", "title", "characters", "setting", "arc", "tone"]
    missing = [k for k in required_keys if k not in plan]
    if missing:
        raise ValueError(
            f"[Classifier] Story plan is missing required keys: {missing}\n"
            f"Got: {list(plan.keys())}"
        )

    print(f"[Classifier] Category detected: '{plan['category']}'")
    print(f"[Classifier] Story title: '{plan['title']}'")
    print(f"[Classifier] Tone: {plan['tone']}")

    return plan