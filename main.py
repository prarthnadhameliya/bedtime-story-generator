import os
from agents.classifier import run_classifier
from agents.storyteller import run_storyteller, run_user_revision
from agents.judge import run_judge

"""
Before submitting the assignment, describe here in a few sentences what you would have built next 
if you spent 2 more hours on this project:

I would have added a voice narration feature using the OpenAI TTS API so the story 
could be read aloud to the child directly. I would also have added a simple web UI 
using Streamlit so parents can type the request, watch the judge scorecard update 
in real time, and save favorite stories to a local file. Finally I would have added 
a "story memory" feature - if the child loved a character from a previous story, 
they could ask for that character to return in the next one.
"""

MAX_JUDGE_LOOPS = 2
MOODS = ["happy", "sad", "scared", "excited"]


def print_story(story: str) -> None:
    print("\n" + "═" * 50)
    print(story)
    print("═" * 50)


def ask_mood() -> str:
    print("\nBefore we begin — how are you feeling tonight?")
    print("  1. happy 😄")
    print("  2. sad 😢")
    print("  3. scared 😨")
    print("  4. excited 🤩")
    print("  (press Enter to skip)")

    choice = input("\nYour choice (1-4): ").strip()

    mood_map = {"1": "happy", "2": "sad", "3": "scared", "4": "excited"}
    mood = mood_map.get(choice, "")

    if mood:
        responses = {
            "happy":   "Wonderful! Let's keep that joy going 🌟",
            "sad":     "I'm sorry you're feeling sad. This story will be extra cozy 🤗",
            "scared":  "No worries — this story will be warm and safe, I promise 🌙",
            "excited": "Ooh, let's channel that energy into an amazing adventure! ⚡",
        }
        print(responses[mood])

    return mood


def run_pipeline(user_input: str, mood: str = "") -> None:
    # ─── Step 1: Classify and plan ───────────────────
    plan = run_classifier(user_input, mood=mood)

    # ─── Step 2: Write + judge loop ──────────────────
    story = run_storyteller(plan)

    for attempt in range(MAX_JUDGE_LOOPS):
        judge_result = run_judge(story, plan)

        if judge_result["passed"]:
            break

        if attempt < MAX_JUDGE_LOOPS - 1:
            print(f"\n[Pipeline] Attempt {attempt + 1} failed. Requesting revision...")
            story = run_storyteller(plan, feedback=judge_result["revision_instructions"])
        else:
            print(f"\n[Pipeline] Max revision attempts reached. Using best version.")

    # ─── Step 3: Print the approved story ────────────
    print("\n✨ Here is your story! ✨")
    print_story(story)

    # ─── Step 4: User feedback loop ──────────────────
    while True:
        print("\nWould you like any changes to the story?")
        user_feedback = input("Your feedback (or press Enter to finish): ").strip()

        if not user_feedback:
            print("\n🌙 Sweet dreams! Goodnight! 🌙")
            break

        story = run_user_revision(plan, story, user_feedback)
        print_story(story)


def main():
    print("\n🌟 Welcome to the Bedtime Story Generator! 🌟")
    print("─" * 50)

    mood = ask_mood()

    user_input = input("\nWhat kind of story would you like to hear? ").strip()

    if not user_input:
        print("No story request provided. Goodnight!")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return

    run_pipeline(user_input, mood=mood)


if __name__ == "__main__":
    main()