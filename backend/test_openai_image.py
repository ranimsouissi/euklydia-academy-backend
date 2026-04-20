from openai import OpenAI
import base64
import os
from datetime import datetime

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY est introuvable dans les variables d’environnement.")

client = OpenAI(api_key=api_key)

prompt = """
Create a clean, professional educational infographic for a learning platform.

Title: "AI in the Workplace"

Style:
- minimalist
- white or very light background
- soft green color palette (professional, not flashy)
- flat design icons
- clean layout, well spaced, not crowded
- modern typography, easy to read

Structure:
The infographic must be divided into 4 clearly separated boxes (grid layout 2x2).

Top left:
Title: "What is AI"
Text:
"AI in the workplace refers to systems that help analyze data, generate content, and automate tasks."

Top right:
Title: "What AI can do"
Bullet points:
- automate repetitive tasks
- generate content
- analyze data

Bottom left:
Title: "What AI cannot do"
Bullet points:
- fully understand context
- replace human judgment
- guarantee perfect accuracy

Bottom right:
Title: "How to use AI effectively"
Bullet points:
- combine AI with human thinking
- review outputs
- use AI as a support tool

Design rules:
- each section inside a clean rounded box
- consistent spacing between sections
- include simple icons for each section (AI chip, checklist, warning, lightbulb)
- short readable text (no long paragraphs)
- no text mistakes
- no random topics (no recruitment, no marketing, no unrelated content)
- no clutter

Make it look like a professional training infographic used in a corporate learning platform.
Ensure all text is accurate, correctly placed, and logically consistent.
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1024x1024"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

filename = f"infographic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

with open(filename, "wb") as f:
    f.write(image_bytes)

print(f"Image générée : {filename}")