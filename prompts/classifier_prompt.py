CLASSIFIER_SYSTEM = """
You are a children's story planner. Your job is to analyze a story request
and produce a structured story plan for a bedtime story appropriate for ages 5-10.

You always respond with valid JSON and nothing else — no preamble, no markdown backticks.
""".strip()


def build_classifier_prompt(user_request: str, mood: str = "") -> str:
    mood_instruction = ""
    if mood:
        mood_instruction = f"""
The child is feeling {mood} tonight. Adjust the story's tone and content accordingly:
- happy    → keep the energy joyful and playful
- sad      → make the story extra warm, comforting, and reassuring
- scared   → avoid anything spooky, keep the story gentle and safe
- excited  → match their energy with a lively, fast-paced story
"""

    return f"""
A child has requested this story: "{user_request}"
{mood_instruction}
Your job:
1. Classify the story into exactly ONE of these categories:
   - adventure   (journeys, quests, exploration)
   - friendship  (bonds, teamwork, loyalty)
   - funny       (silly, absurd, comedic)
   - moral       (a clear life lesson at the end)
   - bedtime     (calm, gentle, soothing — helps wind down)

2. Build a story plan with the following structure.

Respond ONLY with this JSON and nothing else:

{{
  "category": "<one of the five categories>",
  "title": "<a creative story title>",
  "characters": [
    {{"name": "<name>", "description": "<one short sentence>"}},
    {{"name": "<name>", "description": "<one short sentence>"}}
  ],
  "setting": "<where and when the story takes place, one sentence>",
  "arc": {{
    "setup": "<introduce characters and the world, one sentence>",
    "problem": "<the challenge or conflict they face, one sentence>",
    "journey": "<how they tackle the challenge, one sentence>",
    "resolution": "<how it resolves, one sentence>",
    "ending": "<the warm/satisfying final moment, one sentence>"
  }},
  "tone": "<2-3 words describing the feeling, e.g. warm and whimsical>",
  "vocabulary_guidance": "<one sentence about word choice for ages 5-10>"
}}
""".strip()