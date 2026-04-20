import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

found = False
for model in client.models.list():
    name = getattr(model, "name", "")
    if "veo" in name.lower():
        found = True
        print(name)

if not found:
    print("No Veo model found.")