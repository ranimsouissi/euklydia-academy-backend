import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(api_key=api_key)

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # project root
OUTPUT_DIR = BASE_DIR / "assets" / "modules" / "module_1"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────────
# SCENES — Module 1: AI Foundations for the Workplace
# Each scene maps to one Veo prompt + output filename
# ─────────────────────────────────────────────
NO_TEXT = (
    " No visible text, no readable words, no writing on screens, "
    "no text overlays, no captions, no labels."
)

SCENES = [
    {
        "id": "scene_1_hook",
        "label": "Scene 1 — Hook: AI is already here",
        "prompt": (
            "Close-up of professional hands typing on a laptop keyboard in a bright "
            "modern open-space office. Fast-paced montage cuts: a glowing laptop screen "
            "with blurred interface, a person organizing colorful sticky notes on a glass "
            "wall, a smartphone with a glowing notification light. Natural daylight, "
            "clean minimal aesthetic, cinematic 4K quality." + NO_TEXT
        ),
    },
    {
        "id": "scene_2_what_is_ai",
        "label": "Scene 2 — What is AI at work?",
        "prompt": (
            "A professional woman in her 30s sitting at a clean desk, typing on a laptop. "
            "The screen emits a soft blue glow suggesting AI activity but no readable content. "
            "Slow zoom toward her focused face. Soft natural light from a window on the left. "
            "Modern minimalist office setting. Calm and focused atmosphere. "
            "Cinematic quality, 4K." + NO_TEXT
        ),
    },
    {
        "id": "scene_3_what_ai_can_do",
        "label": "Scene 3 — What AI can do",
        "prompt": (
            "A series of clean workplace scenes showing professionals working productively: "
            "a person nodding while looking at a glowing laptop screen, another typing "
            "confidently, a project manager reviewing colorful charts on a monitor, "
            "a professional smiling at organized documents. Bright modern offices, "
            "diverse professionals, upbeat and productive atmosphere. "
            "4K cinematic, smooth transitions." + NO_TEXT
        ),
    },
    {
        "id": "scene_4_ai_limits",
        "label": "Scene 4 — The limits of AI",
        "prompt": (
            "A professional man carefully reviewing printed documents on his desk, "
            "using a pen to annotate blank paper. His expression is focused and "
            "slightly skeptical. Close-up on hands holding a pen over paper. "
            "Neutral office background, warm desk lamp light. "
            "Thoughtful and careful atmosphere. 4K cinematic quality." + NO_TEXT
        ),
    },
    {
        "id": "scene_5_sarah",
        "label": "Scene 5 — Role example: Sarah before and after AI",
        "prompt": (
            "A project coordinator woman at her desk, first looking slightly overwhelmed "
            "surrounded by stacks of papers and sticky notes, rubbing her temples. "
            "Then smooth transition to the same woman on the same desk, "
            "sitting upright confidently, smiling while looking at her glowing laptop screen, "
            "making a small hand gesture of approval. Same person, same office, "
            "natural warm light. Cinematic 4K quality." + NO_TEXT
        ),
    },
    {
        "id": "scene_6_takeaway",
        "label": "Scene 6 — Takeaway: The key message",
        "prompt": (
            "A confident professional standing near a large window in a modern office, "
            "looking out with a calm and determined expression. Slow pull-back camera "
            "movement revealing a bright, organized workspace with plants and clean desk. "
            "Warm golden light. Inspiring and empowering atmosphere. "
            "4K cinematic." + NO_TEXT
        ),
    },
    {
        "id": "scene_7_cta",
        "label": "Scene 7 — Call to Action",
        "prompt": (
            "A clean minimal desk with a blank open notebook and a pen, "
            "a hand reaching to write something. Soft focus background of a modern office. "
            "Warm natural light, calm and motivating atmosphere. "
            "Close-up on the notebook and hand. 4K cinematic quality." + NO_TEXT
        ),
    },
]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def generate_scene(scene: dict, lang: str = "en") -> Path:
    """Generate one video scene and save it to disk."""
    output_path = OUTPUT_DIR / f"{scene['id']}_{lang}.mp4"

    if output_path.exists():
        print(f"  ⏭  Already exists, skipping: {output_path.name}")
        return output_path

    print(f"\n🎬  Generating: {scene['label']}")
    print(f"    Prompt: {scene['prompt'][:80]}...")

    operation = client.models.generate_videos(
        model="veo-3.1-fast-generate-preview",
        source=types.GenerateVideosSource(prompt=scene["prompt"]),
    )

    # Poll until done
    while not operation.done:
        print("    ⏳ Waiting for generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(str(output_path))

    print(f"    ✅ Saved: {output_path.name}")
    return output_path


def run_module(lang: str = "en", scenes: list = None):
    """Generate all scenes for a given language."""
    targets = scenes or SCENES
    print(f"\n{'='*55}")
    print(f"  Module 1 — AI Foundations for the Workplace [{lang.upper()}]")
    print(f"  Output dir: {OUTPUT_DIR}")
    print(f"  Scenes to generate: {len(targets)}")
    print(f"{'='*55}")

    results = []
    failed = []

    for scene in targets:
        try:
            path = generate_scene(scene, lang=lang)
            results.append(path)
        except Exception as e:
            print(f"  ❌ Failed: {scene['id']} — {e}")
            failed.append(scene["id"])
        # Respect rate limits between calls
        time.sleep(3)

    print(f"\n{'='*55}")
    print(f"  Done. {len(results)} generated, {len(failed)} failed.")
    if failed:
        print(f"  Failed scenes: {', '.join(failed)}")
    print(f"{'='*55}\n")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Veo videos for Module 1 — Euklydia Academy"
    )
    parser.add_argument(
        "--lang",
        choices=["en", "fr"],
        default="en",
        help="Language version to generate (default: en)",
    )
    parser.add_argument(
        "--scene",
        type=str,
        default=None,
        help="Generate a single scene by ID (e.g. scene_1_hook). Omit to generate all.",
    )
    args = parser.parse_args()

    if args.scene:
        target = next((s for s in SCENES if s["id"] == args.scene), None)
        if not target:
            available = ", ".join(s["id"] for s in SCENES)
            raise ValueError(f"Scene '{args.scene}' not found. Available: {available}")
        run_module(lang=args.lang, scenes=[target])
    else:
        run_module(lang=args.lang)