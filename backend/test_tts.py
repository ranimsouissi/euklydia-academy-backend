# test_tts.py
from google import genai
from google.genai import types
import base64
import struct
import wave
import io

client = genai.Client(api_key="AIzaSyDgKjt4uRE4P45lOoupc_I0O8QPIYBjZBg")

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Bonjour, bienvenue sur Euklydia Academy. Dans cette leçon, nous allons découvrir comment l'intelligence artificielle transforme le métier de commercial.",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Kore",
                )
            )
        ),
    ),
)

# Récupérer les données audio
audio_part = response.candidates[0].content.parts[0].inline_data
audio_data = audio_part.data

if isinstance(audio_data, str):
    audio_bytes = base64.b64decode(audio_data)
else:
    audio_bytes = audio_data

# ✅ Créer un fichier WAV correct avec header PCM
with wave.open("test_audio.wav", "wb") as wav_file:
    wav_file.setnchannels(1)      # Mono
    wav_file.setsampwidth(2)      # 16-bit = 2 bytes
    wav_file.setframerate(24000)  # 24000 Hz
    wav_file.writeframes(audio_bytes)

print("✅ Audio WAV sauvegardé : test_audio.wav")

# Convertir en MP3 avec FFmpeg
import subprocess
subprocess.run([
    "ffmpeg", "-y",
    "-i", "test_audio.wav",
    "test_audio.mp3"
], capture_output=True)
print("✅ Audio MP3 sauvegardé : test_audio.mp3")