# Chapter 2: Your First AI Feature – Structured NPCs

Now that your baseline app runs, let’s add a real feature: generate an NPC with a strict JSON shape. You’ll learn how to ask the model for “JSON only” and safely parse it.

## What you’ll build
- A `/generate_npc` endpoint that returns a JSON object with fields like `name`, `race`, and `backstory`.
- A frontend action that calls the endpoint and prints a nicely formatted card.

## Step 1: Set your API key
Create `.env` in `chapter2/`:
```
GOOGLE_API_KEY="YOUR_API_KEY"
```

## Step 2: Run
```
docker-compose up --build
```
Open `http://localhost:8501`.

## Step 3: Try a prompt
Type: “Generate an Orc blacksmith NPC.” You should see a JSON-shaped response rendered in the UI.

## Diagram
```mermaid
flowchart TD
    A[User prompt] --> B[FastAPI /generate_npc]
    B --> C[Model (JSON only)]
    C --> D[Parse response.text as JSON]
    D --> E[Return dict]
    E --> F[Streamlit renders NPC card]
```

## How it works (backend)
- `backend/services/npc_generator.py`: Builds a prompt and calls the model with `response_mime_type="application/json"`. We then clean and `json.loads()` the result.
- `backend/api/endpoints.py`: Exposes `/generate_npc` and returns the structured dict to the client.

## Exercises
- Add a new NPC field (e.g., `inventory`) and update the prompt to include it.
- Validate the returned JSON on the client and show a helpful error if a key is missing.

## Troubleshooting
- If you see parsing errors, ensure the prompt clearly says “Output ONLY the JSON object”.

## Theory background
- Structured outputs: LLMs are stochastic; asking for JSON reduces ambiguity and makes outputs machine-usable. It’s still best-effort—be explicit and defensive.
- Prompt engineering: Put the JSON requirements near the end; include exact keys and examples when needed. Keep wording unambiguous.
- Parsing: Treat model output as untrusted. Strip fences like ```json, handle escapes, and catch `json.JSONDecodeError`.

## Milestone checks
- Milestone 1: `/generate_npc` returns a JSON object in HTTP tools like curl or Postman.
- Milestone 2: Streamlit renders readable NPC fields.

## Common pitfalls
- Missing API key in `.env`.
- Overly vague prompts leading to narrative text instead of JSON.

## Knowledge check
- Why do we ask the model for `response_mime_type="application/json"`?
- Name two ways JSON parsing can fail and how we guard against them.

## Code sketch
```python
# backend/services/npc_generator.py (shape)
from google.genai import types
from backend.services.llm import client, json_generation_config, CHAT_MODEL

def generate_npc_details(prompt: str) -> dict:
    contents = f"""
    Generate a JSON object with keys: name, race, vocation, personality, backstory.
    Output ONLY the JSON object.
    Prompt: {prompt}
    """
    resp = client.models.generate_content(
        model=CHAT_MODEL,
        contents=contents,
        config=json_generation_config,
    )
    # parse resp.text safely...
```

## References
- Gemini Structured Output: https://ai.google.dev/gemini-api/docs/structured-output
- Prompt engineering guide: https://ai.google.dev/gemini-api/docs/prompting
- Python `json` library: https://docs.python.org/3/library/json.html
- Error handling in Python: https://docs.python.org/3/tutorial/errors.html

