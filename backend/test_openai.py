import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

resp = client.responses.create(
    model="gpt-4.1",
    input="Reply with a valid JSON object: {\"ok\": true}"
)

print(resp.output_text)