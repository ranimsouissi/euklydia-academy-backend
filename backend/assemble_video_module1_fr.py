import os
import time
import subprocess
from pathlib import Path
from gtts import gTTS

BASE_DIR   = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets" / "modules" / "module_1"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# SCENES — Module 1 version française
# On réutilise les vidéos _en.mp4 existantes
# ─────────────────────────────────────────────
SCENES = [
    {
        "id": "scene_1_hook",
        "video": "scene_1_hook_en.mp4",
        "text": (
            "Pensez à la dernière fois que vous avez dû résumer un long rapport, "
            "rédiger un message dans l'urgence, ou organiser une liste de tâches complexe. "
            "Et si vous aviez un assistant capable de produire une première version en quelques secondes ? "
            "Cet assistant existe. On l'appelle l'intelligence artificielle. "
            "Et il est déjà intégré dans les outils que vous utilisez au quotidien."
        ),
    },
    {
        "id": "scene_2_what_is_ai",
        "video": "scene_2_what_is_ai_en.mp4",
        "text": (
            "L'intelligence artificielle s'impose progressivement dans le monde du travail. "
            "Elle aide les professionnels à gagner du temps en résumant des informations, "
            "en rédigeant du contenu, en organisant des idées et en prenant en charge des tâches répétitives. "
            "Mais comprendre ce qu'est l'IA — et ce qu'elle n'est pas — "
            "est la première étape pour bien l'utiliser."
        ),
    },
    {
        "id": "scene_3_what_ai_can_do",
        "video": "scene_3_what_ai_can_do_en.mp4",
        "text": (
            "L'IA n'est pas une machine qui pense. C'est un outil de reconnaissance de patterns. "
            "Elle apprend à partir de grandes quantités de données existantes "
            "et génère des réponses basées sur ce qu'elle a déjà vu. "
            "Cela signifie qu'elle peut être rapide, utile et cohérente — "
            "mais aussi incorrecte, incomplète ou hors contexte."
        ),
    },
    {
        "id": "scene_4_ai_limits",
        "video": "scene_4_ai_limits_en.mp4",
        "text": (
            "La culture de l'IA — la capacité à comprendre, évaluer et utiliser efficacement "
            "les outils d'intelligence artificielle — devient l'une des compétences professionnelles "
            "les plus importantes de notre époque. "
            "Pas seulement pour les équipes tech. Pour tout le monde."
        ),
    },
    {
        "id": "scene_5_sarah",
        "video": "scene_5_sarah_en.mp4",
        "text": (
            "Prenons un exemple concret. "
            "Sarah est coordinatrice de projet. Après chaque réunion d'équipe, "
            "elle passe 20 à 30 minutes à rédiger les notes, "
            "lister les actions à mener et envoyer un récapitulatif à l'équipe. "
            "Un jour, elle essaie un outil d'IA. Elle colle la transcription de la réunion "
            "et demande à l'outil d'extraire les décisions clés et les prochaines étapes. "
            "En dix secondes, elle obtient une première version. "
            "Mais elle ne l'envoie pas immédiatement. Elle la relit. "
            "Elle corrige un élément mal attribué. "
            "Elle ajoute du contexte que l'IA ne pouvait pas connaître. Puis elle envoie. "
            "Le résultat ? Le même niveau de qualité — en une fraction du temps. "
            "Sarah n'a pas arrêté de réfléchir. Elle a commencé à réfléchir à un niveau supérieur."
        ),
    },
    {
        "id": "scene_6_takeaway",
        "video": "scene_6_takeaway_en.mp4",
        "text": (
            "Voici ce qu'il faut retenir de ce module. "
            "L'IA est un outil professionnel concret. "
            "Elle peut soutenir votre productivité, accélérer votre travail "
            "et réduire la charge cognitive liée aux tâches répétitives. "
            "Mais elle doit toujours être utilisée avec jugement et responsabilité. "
            "L'IA ne remplace pas votre expertise. "
            "Elle la prolonge — quand vous savez comment l'utiliser correctement."
        ),
    },
    {
        "id": "scene_7_cta",
        "video": "scene_7_cta_en.mp4",
        "text": (
            "Avant de passer au module suivant, prenez deux minutes pour faire ceci. "
            "Pensez à votre travail quotidien. Identifiez une tâche — une seule — "
            "où l'IA pourrait vous aider à obtenir une première version plus rapidement. "
            "Il peut s'agir d'un résumé, d'une rédaction, d'une organisation ou d'une planification. "
            "Notez-la. Cette tâche est votre point de départ."
        ),
    },
]

# ─────────────────────────────────────────────
# STEP 1 — Générer la voix off FR
# ─────────────────────────────────────────────
def generate_voiceover(scene: dict) -> Path:
    audio_path = ASSETS_DIR / f"{scene['id']}_fr.mp3"

    if audio_path.exists():
        print(f"  ⏭  Audio exists, skipping: {audio_path.name}")
        return audio_path

    print(f"  🎙  Generating audio: {scene['id']}")
    tts = gTTS(text=scene["text"], lang="fr", slow=False)
    tts.save(str(audio_path))
    print(f"  ✅  Audio saved: {audio_path.name}")
    return audio_path


# ─────────────────────────────────────────────
# STEP 2 — Merger vidéo + audio
# ─────────────────────────────────────────────
def merge_scene(scene: dict, audio_path: Path) -> Path:
    video_path  = ASSETS_DIR / scene["video"]
    output_path = ASSETS_DIR / f"{scene['id']}_merged_fr.mp4"

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    if output_path.exists():
        print(f"  ⏭  Merged exists, skipping: {output_path.name}")
        return output_path

    print(f"  🎬  Merging video + audio: {scene['id']}")

    # Get audio duration
    probe = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ], capture_output=True, text=True, check=True)
    audio_duration = float(probe.stdout.strip())

    # Get video duration
    probe_v = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ], capture_output=True, text=True, check=True)
    video_duration = float(probe_v.stdout.strip())

    speed = video_duration / audio_duration
    print(f"    Audio: {audio_duration:.1f}s | Video: {video_duration:.1f}s | Speed: {speed:.3f}x")

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-filter_complex",
        f"[0:v]setpts={1/speed}*PTS,"
        f"scale=1920:1080:force_original_aspect_ratio=decrease,"
        f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v]",
        "-map", "[v]",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-t", str(audio_duration),
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  ✅  Merged: {output_path.name}")
    return output_path


# ─────────────────────────────────────────────
# STEP 3 — Concaténer toutes les scènes
# ─────────────────────────────────────────────
def concatenate_scenes(merged_paths: list) -> Path:
    final_path  = ASSETS_DIR / "module_1_final_fr.mp4"
    concat_file = ASSETS_DIR / "concat_list_fr.txt"

    print(f"\n  🔗  Concatenating {len(merged_paths)} scenes...")

    with open(concat_file, "w") as f:
        for p in merged_paths:
            f.write(f"file '{p.resolve()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(final_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    concat_file.unlink()

    print(f"  ✅  Final video saved: {final_path.name}")
    print(f"  📁  Location: {final_path.resolve()}")
    return final_path


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print(f"\n{'='*55}")
    print(f"  Module 1 — Assemble Video [FR]")
    print(f"  Assets dir: {ASSETS_DIR}")
    print(f"{'='*55}\n")

    merged_paths = []
    failed = []

    for scene in SCENES:
        print(f"\n── {scene['id']} ──")
        try:
            audio_path  = generate_voiceover(scene)
            merged_path = merge_scene(scene, audio_path)
            merged_paths.append(merged_path)
        except Exception as e:
            print(f"  ❌  Failed: {scene['id']} — {e}")
            failed.append(scene["id"])

    if merged_paths:
        final = concatenate_scenes(merged_paths)
        print(f"\n{'='*55}")
        print(f"  Done! Open your final video:")
        print(f"  {final.resolve()}")
        print(f"{'='*55}\n")
    else:
        print("\n❌ No scenes were processed. Check errors above.")


if __name__ == "__main__":
    main()