import os
import time
import subprocess
from pathlib import Path
from gtts import gTTS

BASE_DIR   = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets" / "modules" / "module_1"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# SCRIPT — one entry per scene
# text  : narration for this scene
# video : matching Veo clip filename
# ─────────────────────────────────────────────
SCENES = [
    {
        "id": "scene_1_hook",
        "video": "scene_1_hook_en.mp4",
        "text": (
            "Think about the last time you had to summarize a long report, "
            "draft a message under pressure, or organize a complex list of tasks. "
            "What if you had a smart assistant that could handle the first draft in seconds? "
            "That assistant exists. It is called artificial intelligence. "
            "And it is already in the tools you use every day."
        ),
    },
    {
        "id": "scene_2_what_is_ai",
        "video": "scene_2_what_is_ai_en.mp4",
        "text": (
            "Artificial intelligence is becoming part of everyday work. "
            "It helps professionals save time by summarizing information, "
            "drafting content, organizing ideas, and supporting routine tasks. "
            "But understanding what AI is — and what it is not — is the first step to using it well."
        ),
    },
    {
        "id": "scene_3_what_ai_can_do",
        "video": "scene_3_what_ai_can_do_en.mp4",
        "text": (
            "AI is not a thinking machine. It is a pattern-recognition tool. "
            "It learns from large amounts of existing data and generates outputs "
            "based on what it has seen before. "
            "That means it can be fast, helpful, and consistent — "
            "but it can also be wrong, incomplete, or out of context."
        ),
    },
    {
        "id": "scene_4_ai_limits",
        "video": "scene_4_ai_limits_en.mp4",
        "text": (
            "AI literacy — the ability to understand, evaluate, and use AI tools effectively — "
            "is becoming one of the most important professional skills of our time. "
            "Not just for tech teams. For everyone."
        ),
    },
    {
        "id": "scene_5_sarah",
        "video": "scene_5_sarah_en.mp4",
        "text": (
            "Let's take a concrete example. "
            "Sarah is a project coordinator. After every team meeting, "
            "she spends 20 to 30 minutes writing up the notes, "
            "listing the action items, and sending a summary to the team. "
            "One day, she tries an AI tool. She pastes the meeting transcript "
            "and asks it to extract the key decisions and next steps. "
            "In 10 seconds, she has a first draft. "
            "But she does not send it immediately. She reads through it. "
            "She corrects one item that was misattributed. "
            "She adds context the AI could not have known. Then she sends it. "
            "The result? The same quality output — in a fraction of the time. "
            "Sarah did not stop thinking. She started thinking at a higher level."
        ),
    },
    {
        "id": "scene_6_takeaway",
        "video": "scene_6_takeaway_en.mp4",
        "text": (
            "Here is what to remember from this module. "
            "AI is a practical workplace tool. "
            "It can support your productivity, accelerate your work, "
            "and reduce cognitive load on repetitive tasks. "
            "But it must always be used with human judgment and responsibility. "
            "AI does not replace your expertise. "
            "It extends it — when you know how to use it well."
        ),
    },
    {
        "id": "scene_7_cta",
        "video": "scene_7_cta_en.mp4",
        "text": (
            "Before moving to the next module, take two minutes to do this. "
            "Think about your daily work. Identify one task — just one — "
            "where AI could help you get to a first draft faster. "
            "It could be summarizing, drafting, organizing, or planning. "
            "Write it down. That task is your starting point. "
            "In the next module, we will explore generative AI — "
            "and you will start to see exactly how that task could be done."
        ),
    },
]

# ─────────────────────────────────────────────
# STEP 1 — Generate voice-over per scene
# ─────────────────────────────────────────────
def generate_voiceover(scene: dict) -> Path:
    audio_path = ASSETS_DIR / f"{scene['id']}_en.mp3"

    if audio_path.exists():
        print(f"  ⏭  Audio exists, skipping: {audio_path.name}")
        return audio_path

    print(f"  🎙  Generating audio: {scene['id']}")
    tts = gTTS(text=scene["text"], lang="en", slow=False)
    tts.save(str(audio_path))
    print(f"  ✅  Audio saved: {audio_path.name}")
    return audio_path


# ─────────────────────────────────────────────
# STEP 2 — Merge video + audio per scene
# ─────────────────────────────────────────────
def merge_scene(scene: dict, audio_path: Path) -> Path:
    video_path  = ASSETS_DIR / scene["video"]
    output_path = ASSETS_DIR / f"{scene['id']}_merged_en.mp4"

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    if output_path.exists():
        print(f"  ⏭  Merged exists, skipping: {output_path.name}")
        return output_path

    print(f"  🎬  Merging video + audio: {scene['id']}")

    # Step 1: get audio duration
    probe = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ], capture_output=True, text=True, check=True)
    audio_duration = float(probe.stdout.strip())

    # Step 2: get video duration
    probe_v = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path)
    ], capture_output=True, text=True, check=True)
    video_duration = float(probe_v.stdout.strip())

    # Step 3: calculate speed factor to stretch video to audio length
    speed = video_duration / audio_duration  # <1 = slow down, >1 = speed up

    print(f"    Audio: {audio_duration:.1f}s | Video: {video_duration:.1f}s | Speed: {speed:.3f}x")

    # Step 4: loop video if audio is much longer, then slow/speed to match exactly
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",       # loop video indefinitely
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
        "-t", str(audio_duration),  # cut exactly at audio duration
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  ✅  Merged: {output_path.name}")
    return output_path


# ─────────────────────────────────────────────
# STEP 3 — Concatenate all merged scenes
# ─────────────────────────────────────────────
def concatenate_scenes(merged_paths: list[Path]) -> Path:
    final_path  = ASSETS_DIR / "module_1_final_en.mp4"
    concat_file = ASSETS_DIR / "concat_list.txt"

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
    concat_file.unlink()  # clean up temp file

    print(f"  ✅  Final video saved: {final_path.name}")
    print(f"  📁  Location: {final_path.resolve()}")
    return final_path


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print(f"\n{'='*55}")
    print(f"  Module 1 — Assemble Video [EN]")
    print(f"  Assets dir: {ASSETS_DIR}")
    print(f"{'='*55}\n")

    merged_paths = []

    for scene in SCENES:
        print(f"\n── {scene['id']} ──")
        try:
            # Step 1: voice-over
            audio_path = generate_voiceover(scene)
            # Step 2: merge with video
            merged_path = merge_scene(scene, audio_path)
            merged_paths.append(merged_path)
        except Exception as e:
            print(f"  ❌  Failed: {scene['id']} — {e}")

    if merged_paths:
        # Step 3: final concat
        final = concatenate_scenes(merged_paths)
        print(f"\n{'='*55}")
        print(f"  Done! Open your final video:")
        print(f"  {final.resolve()}")
        print(f"{'='*55}\n")
    else:
        print("\n❌ No scenes were processed. Check errors above.")


if __name__ == "__main__":
    main()