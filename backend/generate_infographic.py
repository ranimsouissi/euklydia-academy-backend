import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "assets" / "modules" / "module_5"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

output_path = OUTPUT_DIR / "infographic_v2_clean.png"

prompt = """
Create a professional infographic for an AI training module.

TITLE:
Responsible AI in Practice

SUBTITLE:
Guidelines for Ethical AI Use

CONTENT:

1. Why Responsible AI Matters
- AI is powerful — but comes with real risks
- Misuse can lead to privacy, bias, and ethical issues
- Responsible use protects people, trust, and organizations

2. Key Risks to Watch
- Sharing sensitive or confidential data
- Biased or unfair AI outputs
- Misleading or incorrect content
- Over-reliance without human verification

3. How to Use AI Responsibly
- Never input confidential data
- Always review outputs for accuracy and fairness
- Use AI as a support tool, not a decision-maker
- Apply human judgment before acting

4. Real-World Example
HR Specialist: Reviews AI-generated insights carefully and avoids sharing employee data to ensure fairness and compliance

5. Think Before You Act
Where in your daily work could AI introduce privacy or fairness risks?

DESIGN STYLE:
- Clean white background (MANDATORY)
- Modern SaaS-style design (Notion / Stripe / OpenAI style)
- Card-based layout with soft shadows
- Strong visual hierarchy
- Plenty of spacing (not crowded)

COLOR SYSTEM:
- Dark green for titles
- Bright green for highlights
- Subtle light background variations per section (very light tones only)
- No dark or full green background

VISUAL STRUCTURE:
- Each section should be visually distinct (not identical cards)
- Use modern, minimal icons
- Make the layout vertical and easy to scan

ACTION BOX:
- Make the final section visually dominant
- Use a strong green gradient only in this section
- Add depth (shadow or glow)

AVOID:
- Highlighted text blocks (no green text markers)
- Flat or repetitive layout
- Canva-style template look
- Too much text in one block

GOAL:
Create a premium, high-end infographic suitable for an executive AI training platform.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt],
    config=types.GenerateContentConfig(
        image_config=types.ImageConfig(aspect_ratio="4:5")
    )
)

saved = False
for candidate in response.candidates:
    for part in candidate.content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            print("Saved:", output_path.resolve())
            saved = True
            break
    if saved:
        break

if not saved:
    print("No image returned.")