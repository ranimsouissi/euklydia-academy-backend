"""
Pipeline de génération vidéo — Leçon 1.1
"C'est quoi l'AI pour un commercial ?"
Module 1 — AI Sales Specialist Fondations
Durée cible : 8 min
"""

import os
import time
import base64
import wave
import subprocess
import json
from google import genai
from google.genai import types

# ── Configuration ─────────────────────────────────────────────────────────────
API_KEY = "AIzaSyDgKjt4uRE4P45lOoupc_I0O8QPIYBjZBg"
TEMP_DIR = r"C:\Users\Ranim\euklydia\backend\videos\temp"
OUTPUT_DIR = r"C:\Users\Ranim\euklydia\backend\videos\output"
LESSON_ID = "lesson_1_1"
LESSON_TITLE = "C'est quoi l'AI pour un commercial ?"

client = genai.Client(api_key=API_KEY)

# ── Script de la leçon ────────────────────────────────────────────────────────
SEQUENCES = [
    {
        "id": 1,
        "duree": 8,
        "titre": "Introduction",
        "narration": "Bienvenue sur Euklydia Academy. Aujourd'hui, une question simple mais fondamentale : qu'est-ce que l'intelligence artificielle pour un commercial ? Et pourquoi vous devez la maîtriser maintenant.",
        "visuel_prompt": "Un commercial tunisien moderne dans un bureau élégant à Tunis, regardant son écran d'ordinateur avec des graphiques de ventes en hausse. Lumière naturelle, atmosphère professionnelle et dynamique.",
        "style": "realiste",
        "texte_overlay": "C'est quoi l'AI pour un commercial ?",
    },
    {
        "id": 2,
        "duree": 8,
        "titre": "Le constat",
        "narration": "En 2025, les commerciaux qui utilisent l'AI concluent 35% de deals supplémentaires. Ceux qui ne l'utilisent pas perdent du terrain chaque jour. La question n'est plus 'faut-il adopter l'AI' mais 'comment l'adopter intelligemment'.",
        "visuel_prompt": "Infographie animée moderne montrant deux barres de progression — une verte montant rapidement étiquetée 'Avec AI +35%', une grise stagnante étiquetée 'Sans AI'. Design épuré, fond blanc, style business professionnel.",
        "style": "graphique",
        "texte_overlay": "+35% de deals avec l'AI",
    },
    {
        "id": 3,
        "duree": 8,
        "titre": "Définition simple",
        "narration": "L'intelligence artificielle, c'est simplement un outil qui analyse des données, détecte des patterns et vous aide à prendre de meilleures décisions. Pour un commercial, c'est comme avoir un assistant ultra-rapide qui travaille 24h sur 24.",
        "visuel_prompt": "Animation claire et moderne d'un cerveau digital connecté à des icônes commerciales — emails, graphiques, contacts clients, calendrier. Couleurs teal et blanc, style tech professionnel.",
        "style": "animation",
        "texte_overlay": "L'AI = votre assistant intelligent 24/7",
    },
    {
        "id": 4,
        "duree": 8,
        "titre": "Ce que l'AI fait pour vous",
        "narration": "Concrètement, l'AI peut identifier vos prospects les plus chauds, rédiger vos emails de prospection, analyser vos données CRM et prédire quels clients vont acheter. Des tâches qui vous prennent des heures — l'AI les fait en secondes.",
        "visuel_prompt": "Interface HubSpot CRM moderne sur un écran d'ordinateur, montrant un tableau de bord avec scores de leads, pipeline de ventes coloré, et notifications intelligentes. Bureau moderne à Tunis.",
        "style": "interface",
        "texte_overlay": "Prospection • CRM • Emails • Prédictions",
    },
    {
        "id": 5,
        "duree": 8,
        "titre": "Exemple MENA concret",
        "narration": "Prenons un exemple concret. Karim, commercial B2B à Casablanca, utilisait 3 heures par jour à qualifier ses prospects manuellement. Après avoir adopté HubSpot AI, il qualifie 200 prospects en 20 minutes et se concentre sur les deals à fort potentiel.",
        "visuel_prompt": "Commercial marocain professionnel dans un bureau moderne à Casablanca, utilisant un laptop avec interface CRM. Il sourit en regardant ses résultats. Décor business nord-africain contemporain.",
        "style": "realiste",
        "texte_overlay": "Karim — Casablanca : 3h → 20 min",
    },
    {
        "id": 6,
        "duree": 8,
        "titre": "Marché MENA et AI",
        "narration": "Le marché MENA est en pleine transformation digitale. Les Émirats Arabes Unis, l'Arabie Saoudite, le Maroc et la Tunisie investissent massivement dans l'AI. Les entreprises qui adoptent l'AI Sales aujourd'hui seront les leaders de demain dans la région.",
        "visuel_prompt": "Carte stylisée de la région MENA avec des points lumineux connectés — Tunis, Casablanca, Dubai, Riyadh, Le Caire. Lignes de connexion digitales, fond sombre avec éclairages teal. Style tech moderne.",
        "style": "animation",
        "texte_overlay": "MENA : la révolution AI Sales est en marche",
    },
    {
        "id": 7,
        "duree": 8,
        "titre": "L'AI n'est pas une menace",
        "narration": "Attention — l'AI ne remplace pas le commercial. Elle remplace les tâches répétitives. La négociation, la relation de confiance, l'empathie, la compréhension culturelle du marché MENA — ce sont des compétences humaines irremplaçables. L'AI vous libère du temps pour ce qui compte vraiment.",
        "visuel_prompt": "Poignée de main professionnelle entre deux hommes d'affaires dans un bureau moderne du Golfe, symbolisant la confiance et la relation humaine. Fond lumineux, ambiance chaleureuse et professionnelle.",
        "style": "realiste",
        "texte_overlay": "L'AI libère votre temps pour la relation humaine",
    },
    {
        "id": 8,
        "duree": 8,
        "titre": "Les 3 piliers AI Sales",
        "narration": "Retenez ces 3 piliers fondamentaux. Premier pilier : l'AI analyse, vous décidez. Deuxième pilier : l'AI automatise les tâches répétitives. Troisième pilier : l'AI personnalise à grande échelle. Ce sont les bases sur lesquelles repose toute votre formation.",
        "visuel_prompt": "Infographie moderne avec 3 colonnes colorées étiquetées — 'Analyser', 'Automatiser', 'Personnaliser'. Design épuré professionnel, couleurs teal, violet et ambre. Style présentation business.",
        "style": "graphique",
        "texte_overlay": "3 piliers : Analyser • Automatiser • Personnaliser",
    },
    {
        "id": 9,
        "duree": 8,
        "titre": "Ce que vous allez apprendre",
        "narration": "Dans ce module Fondations, vous allez maîtriser les bases de l'AI Sales : comprendre les outils disponibles, apprendre à utiliser ChatGPT pour vos emails, découvrir le CRM AI, et appliquer l'éthique de l'AI dans votre contexte MENA.",
        "visuel_prompt": "Écran d'ordinateur montrant un plan de formation structuré avec des étapes numérotées et des icônes d'outils AI — ChatGPT, HubSpot, Apollo. Bureau moderne, commercial focalisé sur son apprentissage.",
        "style": "interface",
        "texte_overlay": "Module 1 : Les fondations de l'AI Sales",
    },
    {
        "id": 10,
        "duree": 8,
        "titre": "Conclusion et call to action",
        "narration": "L'AI Sales n'est pas le futur — c'est le présent. Les commerciaux qui la maîtrisent aujourd'hui ont un avantage compétitif considérable sur le marché MENA. Vous êtes au bon endroit pour acquérir ces compétences. Passons maintenant à la leçon suivante : les outils AI essentiels du commercial.",
        "visuel_prompt": "Commercial tunisien confiant debout devant une fenêtre panoramique avec vue sur Tunis, tenant un tablet montrant des métriques de ventes positives. Lumière dorée, atmosphère de succès et motivation.",
        "style": "realiste",
        "texte_overlay": "Prêt à devenir un AI Sales Specialist ?",
    },
]


def generer_audio(sequence: dict, output_path: str) -> str:
    """Génère l'audio TTS pour une séquence."""
    print(f"  🎙️ Génération audio séquence {sequence['id']}...")

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=sequence["narration"],
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

    audio_part = response.candidates[0].content.parts[0].inline_data
    audio_data = audio_part.data

    if isinstance(audio_data, str):
        audio_bytes = base64.b64decode(audio_data)
    else:
        audio_bytes = audio_data

    # Sauvegarder en WAV
    wav_path = output_path.replace(".mp3", ".wav")
    with wave.open(wav_path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(24000)
        wav_file.writeframes(audio_bytes)

    # Convertir en MP3
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path,
        "-codec:a", "libmp3lame", "-qscale:a", "2",
        output_path
    ], capture_output=True)

    os.remove(wav_path)
    print(f"  ✅ Audio généré : {os.path.basename(output_path)}")
    return output_path


def generer_visuel(sequence: dict, output_path: str) -> str:
    """Génère le visuel Veo pour une séquence."""
    print(f"  🎬 Génération visuel séquence {sequence['id']}...")

    operation = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt=sequence["visuel_prompt"],
        config=types.GenerateVideosConfig(
            aspect_ratio="16:9",
            number_of_videos=1,
        ),
    )

    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)

    for video in operation.response.generated_videos:
        client.files.download(file=video.video)
        video.video.save(output_path)

    print(f"  ✅ Visuel généré : {os.path.basename(output_path)}")
    return output_path


def get_audio_duration(audio_path: str) -> float:
    """Retourne la durée d'un fichier audio en secondes."""
    result = subprocess.run([
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", audio_path
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data["streams"][0]["duration"])


def assembler_sequence(sequence: dict, video_path: str, audio_path: str, output_path: str) -> str:
    """Assemble vidéo + audio + texte overlay pour une séquence."""
    print(f"  🔧 Assemblage séquence {sequence['id']}...")

    audio_duration = get_audio_duration(audio_path)

    # Texte overlay en bas de la vidéo
    texte = sequence["texte_overlay"].replace("'", "\\'")
    fontsize = 36
    box_color = "black@0.6"

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",        # Boucler la vidéo si audio plus long
        "-i", video_path,
        "-i", audio_path,
        "-t", str(audio_duration),   # Durée = durée de l'audio
        "-vf", (
            f"scale=1920:1080,"
            f"drawtext=text='{texte}'"
            f":fontsize={fontsize}"
            f":fontcolor=white"
            f":x=(w-text_w)/2"
            f":y=h-80"
            f":box=1"
            f":boxcolor={box_color}"
            f":boxborderw=10"
        ),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-map", "0:v:0",
        "-map", "1:a:0",
        output_path
    ]

    subprocess.run(cmd, capture_output=True)
    print(f"  ✅ Séquence assemblée : {os.path.basename(output_path)}")
    return output_path


def concatener_sequences(sequence_paths: list, output_path: str) -> str:
    """Concatène toutes les séquences en une vidéo finale."""
    print(f"\n🎞️ Concaténation de {len(sequence_paths)} séquences...")

    # Créer fichier liste pour FFmpeg
    liste_path = os.path.join(TEMP_DIR, "liste_sequences.txt")
    with open(liste_path, "w") as f:
        for path in sequence_paths:
            f.write(f"file '{path}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", liste_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_path
    ]

    subprocess.run(cmd, capture_output=True)
    print(f"✅ Vidéo finale : {output_path}")
    return output_path


def generer_video_lecon():
    """Pipeline principal de génération vidéo."""
    print("=" * 60)
    print(f"🚀 Génération vidéo : {LESSON_TITLE}")
    print(f"   {len(SEQUENCES)} séquences à générer")
    print("=" * 60)

    sequences_assemblees = []

    for seq in SEQUENCES:
        print(f"\n📍 Séquence {seq['id']}/10 — {seq['titre']}")

        audio_path = os.path.join(TEMP_DIR, f"{LESSON_ID}_seq{seq['id']}_audio.mp3")
        video_path = os.path.join(TEMP_DIR, f"{LESSON_ID}_seq{seq['id']}_video.mp4")
        assembled_path = os.path.join(TEMP_DIR, f"{LESSON_ID}_seq{seq['id']}_final.mp4")

        # Générer audio
        generer_audio(seq, audio_path)

        # Générer visuel
        generer_visuel(seq, video_path)

        # Assembler séquence
        assembler_sequence(seq, video_path, audio_path, assembled_path)

        sequences_assemblees.append(assembled_path)

        print(f"  ✅ Séquence {seq['id']} complète")

    # Concaténer toutes les séquences
    output_final = os.path.join(OUTPUT_DIR, f"{LESSON_ID}_final.mp4")
    concatener_sequences(sequences_assemblees, output_final)

    print("\n" + "=" * 60)
    print("🎉 VIDÉO GÉNÉRÉE AVEC SUCCÈS !")
    print(f"   Fichier : {output_final}")
    print("=" * 60)

    return output_final


if __name__ == "__main__":
    generer_video_lecon()