import json
from models import call_model
from prompts.judge_prompt import JUDGE_SYSTEM, PASS_THRESHOLD, build_judge_prompt
from agents.classifier import clean_json_response


def run_judge(story: str, plan: dict) -> dict:
    """
    Evaluates the story against the original plan.

    Returns a dict with:
      - scores:                dict of 4 dimension scores (1-5)
      - critiques:             dict of one-sentence critiques per dimension
      - average_score:         float
      - revision_needed:       bool
      - revision_instructions: str (empty if revision not needed)
      - passed:                bool (True if average_score >= PASS_THRESHOLD)
    """
    print("\n[Judge] Evaluating story quality...")

    prompt = build_judge_prompt(story, plan)
    raw_response = call_model(prompt, system=JUDGE_SYSTEM)

    try:
        cleaned = clean_json_response(raw_response)
        result = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"[Judge] Failed to parse evaluation from model response.\n"
            f"Raw response was:\n{raw_response}\n"
            f"JSON error: {e}"
        )

    # Recalculate average ourselves to verify model's math
    scores = result.get("scores", {})
    if scores:
        recalculated_avg = round(sum(scores.values()) / len(scores), 1)
        result["average_score"] = recalculated_avg

    result["passed"] = result["average_score"] >= PASS_THRESHOLD

    _print_scorecard(result)

    return result


def _print_scorecard(result: dict) -> None:
    """
    Prints a readable scorecard to the terminal so the user
    can see what the judge thought.
    """
    scores    = result.get("scores", {})
    critiques = result.get("critiques", {})
    avg       = result.get("average_score", 0)
    passed    = result.get("passed", False)

    print("\n┌─────────────────────────────────────────┐")
    print("│              Judge Scorecard             │")
    print("├─────────────────────────────────────────┤")

    labels = {
        "age_appropriateness": "Age appropriateness",
        "story_arc":           "Story arc          ",
        "engagement":          "Engagement         ",
        "ending_quality":      "Ending quality     ",
    }

    for key, label in labels.items():
        score    = scores.get(key, "?")
        critique = critiques.get(key, "")
        bar      = "★" * int(score) + "☆" * (5 - int(score))
        print(f"│  {label}  {bar}  ({score}/5)")
        if critique:
            # wrap critique to fit inside the box
            print(f"│    ↳ {critique[:55]}")

    print("├─────────────────────────────────────────┤")
    status = "✅ PASSED" if passed else "❌ NEEDS REVISION"
    print(f"│  Average: {avg}/5   {status:<28}│")
    print("└─────────────────────────────────────────┘")

    if not passed and result.get("revision_instructions"):
        print(f"\n[Judge] Revision notes: {result['revision_instructions']}")