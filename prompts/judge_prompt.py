JUDGE_SYSTEM = """
You are a strict but fair children's literature editor who specializes in stories for ages 5-10.
Your job is to evaluate a story and provide honest, specific scores and feedback.

You always respond with valid JSON and nothing else — no preamble, no markdown backticks.
""".strip()


SCORING_CRITERIA = {
    "age_appropriateness": "Vocabulary, themes, and complexity are right for ages 5-10. Nothing scary, confusing, or adult.",
    "story_arc":           "The story has a clear setup, problem, journey, resolution, and satisfying ending.",
    "engagement":          "The language is vivid and expressive. A child would want to keep listening.",
    "ending_quality":      "The ending feels warm, complete, and emotionally satisfying — not abrupt or flat.",
}

PASS_THRESHOLD = 3.5


def build_judge_prompt(story: str, plan: dict) -> str:
    criteria_lines = "\n".join(
        f'  - "{key}": {description}'
        for key, description in SCORING_CRITERIA.items()
    )

    return f"""
You are evaluating a children's story for ages 5-10.

ORIGINAL STORY PLAN:
- Category: {plan.get('category', '')}
- Tone:     {plan.get('tone', '')}
- Arc:      Setup → {plan.get('arc', {}).get('setup', '')}
            Problem → {plan.get('arc', {}).get('problem', '')}
            Resolution → {plan.get('arc', {}).get('resolution', '')}

STORY TO EVALUATE:
\"\"\"
{story}
\"\"\"

SCORING CRITERIA (score each 1-5, where 3=acceptable, 5=excellent):
{criteria_lines}

INSTRUCTIONS:
- Score each criterion honestly from 1 to 5
- For any score below 4, write a specific one-sentence critique explaining exactly what to fix
- "revision_needed" should be true if the AVERAGE score is below {PASS_THRESHOLD}
- "revision_instructions" should be a single paragraph of specific, actionable fixes for the storyteller
  (only needed when revision_needed is true, otherwise leave as empty string)

Respond ONLY with this JSON and nothing else:

{{
  "scores": {{
    "age_appropriateness": <1-5>,
    "story_arc":           <1-5>,
    "engagement":          <1-5>,
    "ending_quality":      <1-5>
  }},
  "critiques": {{
    "age_appropriateness": "<one sentence, or empty string if score >= 4>",
    "story_arc":           "<one sentence, or empty string if score >= 4>",
    "engagement":          "<one sentence, or empty string if score >= 4>",
    "ending_quality":      "<one sentence, or empty string if score >= 4>"
  }},
  "average_score": <float, one decimal place>,
  "revision_needed": <true or false>,
  "revision_instructions": "<specific paragraph for storyteller, or empty string>"
}}
""".strip()