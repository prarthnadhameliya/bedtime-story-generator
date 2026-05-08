# Bedtime Story Generator

An AI-powered bedtime story generator for children ages 5-10, built with a 
multi-agent pipeline using GPT-3.5-turbo.

## System Architecture

Three agents work together in a pipeline:

- **Agent 1 — Classifier**: Takes the user's request, detects the story 
  category (adventure, friendship, funny, moral, bedtime), and builds a 
  structured story plan with characters, setting, and a full 5-beat arc.

- **Agent 2 — Storyteller**: Writes the story from the plan using 
  category-specific craft instructions. Runs at higher temperature (0.8) 
  for creative output.

- **Agent 3 — LLM Judge**: Scores the story on 4 dimensions (age-appropriateness, 
  story arc, engagement, ending quality) each 1-5. If the average falls below 
  3.5, it sends specific revision notes back to the Storyteller. Max 2 loops.

## Surprise Feature — Mood Detection

Before asking for a story, the app asks the child how they are feeling 
(happy / sad / scared / excited). The mood is passed into the classifier 
and shapes the tone of the entire story. A sad child gets an extra warm, 
comforting story. An excited child gets a lively adventure.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"
python3 main.py
```

## Project Structure

```
├── main.py                  # Orchestrator + pipeline
├── models.py                # call_model wrappers
├── agents/
│   ├── classifier.py        # Agent 1
│   ├── storyteller.py       # Agent 2
│   └── judge.py             # Agent 3
├── prompts/
│   ├── classifier_prompt.py
│   ├── storyteller_prompt.py
│   └── judge_prompt.py
└── requirements.txt
```



# Hippocratic AI Coding Assignment
Welcome to the [Hippocratic AI](https://www.hippocraticai.com) coding assignment

## Instructions
The attached code is a simple python script skeleton. Your goal is to take any simple bedtime story request and use prompting to tell a story appropriate for ages 5 to 10.
- Incorporate a LLM judge to improve the quality of the story
- Provide a block diagram of the system you create that illustrates the flow of the prompts and the interaction between judge, storyteller, user, and any other components you add
- Do not change the openAI model that is being used. 
- Please use your own openAI key, but do not include it in your final submission.
- Otherwise, you may change any code you like or add any files

---

## Rules
- This assignment is open-ended
- You may use any resources you like with the following restrictions
   - They must be resources that would be available to you if you worked here (so no other humans, no closed AIs, no unlicensed code, etc.)
   - Allowed resources include but not limited to Stack overflow, random blogs, chatGPT et al
   - You have to be able to explain how the code works, even if chatGPT wrote it
- DO NOT PUSH THE API KEY TO GITHUB. OpenAI will automatically delete it

---

## What does "tell a story" mean?
It should be appropriate for ages 5-10. Other than that it's up to you. Here are some ideas to help get the brain-juices flowing!
- Use story arcs to tell better stories
- Allow the user to provide feedback or request changes
- Categorize the request and use a tailored generation strategy for each category

---

## How will I be evaluated
Good question. We want to know the following:
- The efficacy of the system you design to create a good story
- Are you comfortable using and writing a python script
- What kinds of prompting strategies and agent design strategies do you use
- Are the stories your tool creates good?
- Can you understand and deconstruct a problem
- Can you operate in an open-ended environment
- Can you surprise us

---

## Other FAQs
- How long should I spend on this? 
No more than 2-3 hours
- Can I change what the input is? 
Sure
- How long should the story be?
You decide