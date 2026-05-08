from models import call_model_creative
from prompts.storyteller_prompt import STORYTELLER_SYSTEM, build_storyteller_prompt


def run_storyteller(plan: dict, feedback: str = "") -> str:
    """
    Generates a story from the plan.
    
    - First call:          feedback="" → clean first draft
    - Judge revision:      feedback=judge's revision_instructions → targeted rewrite
    - User feedback pass:  feedback=user's request → one final revision
    
    Returns the story as a plain string.
    """
    if not feedback:
        print("\n[Storyteller] Writing your story...")
    else:
        print("\n[Storyteller] Revising the story based on feedback...")

    prompt = build_storyteller_prompt(plan, feedback=feedback)
    story = call_model_creative(prompt, system=STORYTELLER_SYSTEM)

    return story.strip()


def run_user_revision(plan: dict, story: str, user_feedback: str) -> str:
    """
    Handles the user feedback loop after the story has been approved by the judge.
    Passes the existing story AND the user's note as combined feedback
    so the storyteller knows what already exists and what to change.
    """
    combined_feedback = f"""
The story has already been written. Here it is for reference:

{story}

The user has requested these specific changes:
"{user_feedback}"

Rewrite the full story incorporating these changes. Keep everything else the same.
""".strip()

    return run_storyteller(plan, feedback=combined_feedback)