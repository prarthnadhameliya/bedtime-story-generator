import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def call_model(prompt: str, system: str = "", max_tokens: int = 3000, temperature: float = 0.1) -> str:
    """
    Low-temperature model call. Good for classification, judging, structured output.
    System prompt is optional — used to give the model a role or strict instructions.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]


def call_model_creative(prompt: str, system: str = "", max_tokens: int = 3000) -> str:
    """
    Higher-temperature model call (0.8). Used by the Storyteller for creative output.
    Same interface as call_model but warmer — more varied, less robotic sentences.
    """
    return call_model(prompt, system=system, max_tokens=max_tokens, temperature=0.8)