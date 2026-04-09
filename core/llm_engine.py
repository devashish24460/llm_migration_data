# import json
# import os
# from xml.parsers.expat import model
# from groq import Groq
# from dotenv import load_dotenv
# import os
# from groq import Groq

# load_dotenv() 

# api_key = os.getenv("GROQ_API_KEY")
# if not api_key:
#     raise RuntimeError("GROQ_API_KEY not set")

# client = Groq(api_key=api_key)
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def generate_mapping(source_info, target_schema):
#     prompt = f"""
# You are a data migration expert.

# Source schema:
# {json.dumps(source_info, indent=2)}

# Target schema:
# {json.dumps(target_schema, indent=2)}

# Tasks:
# 1. Map source → target columns
# 2. Suggest transformations
# 3. Provide confidence (0–1)
# 4. Return STRICT JSON only

# Format:
# {{
#   "mapping": {{}},
#   "transformations": {{}},
#   "confidence": 0.0,
#   "warnings": []
# }}
# """

#     response = client.chat.completions.create(
#         model=os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0
#     )

#     content = response.choices[0].message.content

#     try:
#         return json.loads(content)
#     except:
#         raise ValueError(f"Invalid JSON from LLM:\n{content}")


import json
import os
import re
from groq import Groq

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Fallback models (order matters)
MODELS = [
    os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    "llama-3.1-8b-instant"
]


# -------------------------------
# Extract JSON safely
# -------------------------------
def extract_json(content: str):
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return match.group()


# -------------------------------
# Call LLM with fallback
# -------------------------------
def call_llm(prompt: str):
    last_error = None

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"[LLM ERROR] Model {model} failed: {e}")
            last_error = e
            continue

    raise Exception(f"All models failed. Last error: {last_error}")


# -------------------------------
# Main function
# -------------------------------
def generate_mapping(source_info, target_schema):

    base_prompt = f"""
You are a strict JSON generator.

DO NOT output anything except valid JSON.
NO explanations, NO markdown, NO extra text.

Return ONLY this structure:

{{
  "mapping": {{}},
  "transformations": {{}},
  "confidence": 0.0,
  "warnings": []
}}

Rules:
- Use double quotes
- No trailing commas
- Must be valid JSON parsable by json.loads()

Source schema:
{json.dumps(source_info, indent=2)}

Target schema:
{json.dumps(target_schema, indent=2)}
"""

    # -------------------------------
    # First attempt
    # -------------------------------
    content = call_llm(base_prompt)

    try:
        return json.loads(extract_json(content))
    except Exception as e:
        print("[PARSE ERROR - FIRST ATTEMPT]", e)

    # -------------------------------
    # Retry with correction prompt
    # -------------------------------
    fix_prompt = f"""
Fix the following output into STRICT valid JSON.

ONLY return JSON. No explanation.

Bad output:
{content}
"""

    content2 = call_llm(fix_prompt)

    try:
        return json.loads(extract_json(content2))
    except Exception as e:
        print("[PARSE ERROR - SECOND ATTEMPT]", e)
        raise ValueError(f"LLM failed after retry:\n{content2}")