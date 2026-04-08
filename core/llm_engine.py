import json
import os
from groq import Groq
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv() 

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not set")

client = Groq(api_key=api_key)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_mapping(source_info, target_schema):
    prompt = f"""
You are a data migration expert.

Source schema:
{json.dumps(source_info, indent=2)}

Target schema:
{json.dumps(target_schema, indent=2)}

Tasks:
1. Map source → target columns
2. Suggest transformations
3. Provide confidence (0–1)
4. Return STRICT JSON only

Format:
{{
  "mapping": {{}},
  "transformations": {{}},
  "confidence": 0.0,
  "warnings": []
}}
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        raise ValueError(f"Invalid JSON from LLM:\n{content}")