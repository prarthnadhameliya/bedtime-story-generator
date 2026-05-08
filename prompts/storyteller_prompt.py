STORYTELLER_SYSTEM = """
You are a warm, imaginative children's story author who specializes in bedtime stories
for kids ages 5 to 10. You write vivid, engaging stories with clear story arcs.

Your stories:
- Use simple but expressive language appropriate for ages 5-10
- Have a clear beginning, middle, and end
- End on a warm, satisfying note
- Are between 300-500 words long
""".strip()


CATEGORY_INSTRUCTIONS = {
    "adventure": """
- Use vivid action words to make the journey feel exciting (dashed, leaped, discovered)
- Build tension gradually — the problem should feel genuinely tricky before it's solved
- Make the setting feel alive and full of wonder
- The hero should earn the resolution through courage or cleverness, not luck
""".strip(),

    "friendship": """
- Show the friendship through actions and dialogue, not just by saying they are friends
- Include a moment where the friendship is tested or proven
- The resolution should feel warm and reinforce the value of loyalty or teamwork
- Use gentle, inclusive language
""".strip(),

    "funny": """
- Use comic timing — short punchy sentences for punchlines, longer ones to build up
- Lean into absurd, silly details (a dragon who sneezes glitter, a cloud made of popcorn)
- Repeat a running joke or silly detail at least twice
- End with one final joke or a fun twist that pays off the setup
""".strip(),

    "moral": """
- Let the moral emerge naturally from events — never state it bluntly until the very end
- The main character should make a mistake or face a genuine dilemma
- Show consequences clearly so the lesson feels earned
- Close with one gentle, memorable sentence that captures the lesson
""".strip(),

    "bedtime": """
- Use slow, soft, rhythmic sentences — this story should make eyelids heavy
- Describe cozy, peaceful sensory details (warm blankets, soft moonlight, quiet sounds)
- Avoid any tension or conflict that might excite or worry a child
- End with the character drifting to sleep or settling into calm contentment
""".strip(),
}


def build_storyteller_prompt(plan: dict, feedback: str = "") -> str:
    """
    Builds the storyteller prompt from the classifier's plan.
    Optionally accepts judge feedback or user feedback for revision passes.
    """
    category = plan.get("category", "adventure")
    category_instructions = CATEGORY_INSTRUCTIONS.get(category, "")

    characters_text = "\n".join(
        f"  - {c['name']}: {c['description']}"
        for c in plan.get("characters", [])
    )

    arc = plan.get("arc", {})

    feedback_block = ""
    if feedback:
        feedback_block = f"""
REVISION NOTES — please address these specific issues in your rewrite:
{feedback}

""".strip() + "\n\n"

    return f"""
Write a children's bedtime story using this plan. Follow every detail closely.

CATEGORY: {category}
TITLE: {plan.get('title', 'A Magical Story')}
TONE: {plan.get('tone', 'warm and whimsical')}

CHARACTERS:
{characters_text}

SETTING: {plan.get('setting', '')}

STORY ARC TO FOLLOW:
  Setup:      {arc.get('setup', '')}
  Problem:    {arc.get('problem', '')}
  Journey:    {arc.get('journey', '')}
  Resolution: {arc.get('resolution', '')}
  Ending:     {arc.get('ending', '')}

VOCABULARY GUIDANCE: {plan.get('vocabulary_guidance', '')}

CATEGORY-SPECIFIC WRITING RULES:
{category_instructions}

{feedback_block}Write the full story now. Start with the title on the first line.
Do not include any commentary before or after the story.
""".strip()