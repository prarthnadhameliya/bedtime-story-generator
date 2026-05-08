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



