import time
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyDgKjt4uRE4P45lOoupc_I0O8QPIYBjZBg")

operation = client.models.generate_videos(
    model="veo-3.0-generate-001",
    prompt="Un commercial tunisien utilise un ordinateur portable pour prospecter des clients avec l'aide de l'intelligence artificielle. Style professionnel, bureau moderne.",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        number_of_videos=1,
    ),
)

print("Génération en cours...")
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)
    print("En attente...")

for video in operation.response.generated_videos:
    client.files.download(file=video.video)
    video.video.save("test_output.mp4")
    print("✅ Vidéo sauvegardée : test_output.mp4")