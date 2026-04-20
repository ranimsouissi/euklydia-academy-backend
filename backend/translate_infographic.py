"""
translate_infographic.py
Génère les versions EN et FR des infographies avec Pillow.
Design riche : icônes, accents colorés, takeaway encadré, séparateur.

Usage:
    python translate_infographic.py --module 1 --lang en
    python translate_infographic.py --module 1 --lang fr
    python translate_infographic.py --module 1 --lang both
    python translate_infographic.py --all --lang both
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import urllib.request

BASE_DIR    = Path(__file__).resolve().parent
FONTS_DIR   = BASE_DIR / "assets" / "fonts"
OUTPUT_BASE = BASE_DIR / "assets" / "modules"

# ─────────────────────────────────────────────
# COULEURS
# ─────────────────────────────────────────────
BG           = "#F5F7F6"
DARK_GREEN   = "#1F6F5F"
MEDIUM_GREEN = "#22A06B"
LIGHT_GREEN  = "#E8F5F0"
BODY         = "#2B2B2B"
BODY_LIGHT   = "#555555"
WHITE        = "#FFFFFF"
BORDER       = "#D4E8E0"

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ─────────────────────────────────────────────
# POLICES
# ─────────────────────────────────────────────

FONT_FILES = {
    "regular": "Inter-Regular.otf",
    "bold":    "Inter-Bold.otf",
}
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"

def ensure_fonts():
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}
    for key, fname in FONT_FILES.items():
        dest = FONTS_DIR / fname
        if not dest.exists():
            print(f"  📥 Téléchargement {fname}...")
            urllib.request.urlretrieve(FONT_URL, dest)
        paths[key] = str(dest)
    return paths

# ─────────────────────────────────────────────
# CONTENU EN
# ─────────────────────────────────────────────

MODULES_EN = {
    1: {
        "badge":    "MODULE 1 · BEGINNER",
        "badge_color": MEDIUM_GREEN,
        "title":    "AI Foundations for the Workplace",
        "subtitle": "Understanding what AI is, how it supports work,\nand why human judgment still matters",
        "sections": [
            {"icon": "🧠", "label": "What AI Is",
             "content": "AI helps professionals process information,\ngenerate content, and support everyday tasks."},
            {"icon": "⚡", "label": "AI vs. Traditional Automation",
             "content": "Traditional automation: fixed rules, repetitive tasks, predictable output.\nAI: adaptive learning, complex problem-solving, creative generation."},
            {"icon": "💼", "label": "Common Workplace Uses",
             "content": "· Summarizing notes\n· Drafting emails\n· Organizing information\n· Generating ideas"},
            {"icon": "👤", "label": "Human Judgment Still Matters",
             "content": "AI makes mistakes. People must review outputs,\napply context, and make final decisions."},
            {"icon": "🎯", "label": "Why AI Literacy Matters + Action",
             "content": "AI is becoming a core workplace skill.\nProfessionals must understand both its benefits and limits.\n→ Identify 1 task in your daily work where AI could help you today."},
        ],
        "takeaway": "AI boosts productivity, but human judgment\nis essential for responsible use.",
        "footer":   "euklydia.com · #AILiteracy",
    },
    2: {
        "badge":    "MODULE 2 · BEGINNER",
        "badge_color": MEDIUM_GREEN,
        "title":    "Understanding Generative AI",
        "subtitle": "What it is, what it can create,\nand how to use it responsibly at work",
        "sections": [
            {"icon": "✨", "label": "What Generative AI Is",
             "content": "A tool that produces content from an instruction:\ntext, summaries, ideas, and plans."},
            {"icon": "📝", "label": "What It Can Generate",
             "content": "· Texts and emails\n· Document summaries\n· Ideas and action plans"},
            {"icon": "🔄", "label": "How It Differs from Traditional AI",
             "content": "Traditional AI automates.\nGenerative AI creates and transforms content."},
            {"icon": "⚠️", "label": "Limits to Know",
             "content": "It can produce errors or approximations.\nAlways verify before using."},
            {"icon": "🎯", "label": "Key Takeaway + Action",
             "content": "Generative AI speeds up creation — but human validation remains essential.\n→ Identify 1 type of content generative AI could help you draft at work."},
        ],
        "takeaway": "Generative AI is powerful, but every output\nneeds human review before use.",
        "footer":   "euklydia.com · #GenerativeAI",
    },
    3: {
        "badge":    "MODULE 3 · BEGINNER",
        "badge_color": MEDIUM_GREEN,
        "title":    "Prompting Essentials",
        "subtitle": "How to write clear instructions\nthat get useful results from AI tools",
        "sections": [
            {"icon": "💬", "label": "What a Prompt Is",
             "content": "An instruction given to an AI tool\nto get a precise and useful result."},
            {"icon": "🧩", "label": "The 3 Elements of a Good Prompt",
             "content": "1. Clear task — what do you want to get?\n2. Useful context — who, what, why?\n3. Expected format — list, email, summary?"},
            {"icon": "📋", "label": "Practical Example",
             "content": "Weak: \"Write an email.\"\nStrong: \"Write a 3-sentence client follow-up email, professional tone.\""},
            {"icon": "🔁", "label": "If the Result Is Not Good",
             "content": "Rephrase, add context, specify the format. Iterate."},
            {"icon": "🎯", "label": "Key Takeaway + Action",
             "content": "A good prompt = task + context + format.\n→ Take a real work request and rewrite it as a structured prompt."},
        ],
        "takeaway": "Better prompts lead to better AI outputs —\nalways be specific.",
        "footer":   "euklydia.com · #Prompting",
    },
    4: {
        "badge":    "MODULE 4 · INTERMEDIATE",
        "badge_color": DARK_GREEN,
        "title":    "Evaluating AI Responses",
        "subtitle": "How to critically review AI outputs\nbefore using them at work",
        "sections": [
            {"icon": "🔍", "label": "Why Review Matters",
             "content": "AI can produce incorrect, vague, or irrelevant responses.\nReview is mandatory."},
            {"icon": "✅", "label": "The 4 Evaluation Criteria",
             "content": "1. Accuracy — is the information correct?\n2. Relevance — does it answer the request?\n3. Clarity — is it readable and understandable?\n4. Completeness — is anything missing?"},
            {"icon": "🚨", "label": "Warning Signs",
             "content": "· Response is too generic\n· Information cannot be verified\n· Tone or format is inappropriate"},
            {"icon": "✏️", "label": "When to Correct",
             "content": "As soon as there is any doubt about accuracy or relevance.\nNever use without review."},
            {"icon": "🎯", "label": "Key Takeaway + Action",
             "content": "Always review before using. Human judgment is non-negotiable.\n→ Take a recent AI response and evaluate it using the 4 criteria."},
        ],
        "takeaway": "AI saves time, but only humans can validate\nquality and context.",
        "footer":   "euklydia.com · #AIEvaluation",
    },
    5: {
        "badge":    "MODULE 5 · BEGINNER",
        "badge_color": MEDIUM_GREEN,
        "title":    "Responsible AI in Practice",
        "subtitle": "How to use AI safely, ethically,\nand with the right level of human oversight",
        "sections": [
            {"icon": "🛡️", "label": "Why It Matters",
             "content": "Misused AI can expose sensitive data\nor produce biased and unfair results."},
            {"icon": "⚠️", "label": "The 3 Main Risks",
             "content": "1. Confidentiality — never share sensitive data with AI tools\n2. Bias — outputs can be unfair or inaccurate\n3. Over-reliance — never replace human judgment"},
            {"icon": "✅", "label": "Good Practices",
             "content": "· Anonymize data before use\n· Check results for fairness and neutrality\n· Keep human control over decisions"},
            {"icon": "🚫", "label": "When to Limit AI Use",
             "content": "HR decisions, personal data, legal or sensitive contexts."},
            {"icon": "🎯", "label": "Key Takeaway + Action",
             "content": "Use AI with discernment, not blindly.\n→ Identify 1 situation in your work where AI use should be supervised."},
        ],
        "takeaway": "Responsible AI use means protecting data,\nchecking for bias, and keeping humans in control.",
        "footer":   "euklydia.com · #ResponsibleAI",
    },
    6: {
        "badge":    "MODULE 6 · INTERMEDIATE",
        "badge_color": DARK_GREEN,
        "title":    "Using AI in Daily Workflows",
        "subtitle": "How to integrate AI into everyday tasks\nto save time and work smarter",
        "sections": [
            {"icon": "🔄", "label": "What a Workflow Is",
             "content": "A sequence of tasks performed regularly\nin a professional context."},
            {"icon": "💡", "label": "Where AI Adds Value",
             "content": "· Repetitive and time-consuming tasks\n· Drafting, summarizing, organizing\n· Preparation and planning"},
            {"icon": "📊", "label": "A 3-Step Method",
             "content": "1. Identify a recurring task\n2. Test AI on that task\n3. Review, adjust, repeat"},
            {"icon": "👔", "label": "Real-World Example",
             "content": "Project manager: summarizes meetings\n→ lists actions → reviews before sharing."},
            {"icon": "🎯", "label": "Key Takeaway + Action",
             "content": "AI creates value when integrated in a practical and repeatable way.\n→ List 3 recurring tasks where AI could help you starting this week."},
        ],
        "takeaway": "AI in your workflow means working smarter —\nnot harder.",
        "footer":   "euklydia.com · #AIWorkflow",
    },
}

# ─────────────────────────────────────────────
# CONTENU FR
# ─────────────────────────────────────────────

MODULES_FR = {
    1: {
        "badge":    "MODULE 1 · DÉBUTANT",
        "badge_color": MEDIUM_GREEN,
        "title":    "Les Fondamentaux de l'IA au Travail",
        "subtitle": "Comprendre ce qu'est l'IA, comment elle soutient le travail\net pourquoi le jugement humain reste essentiel",
        "sections": [
            {"icon": "🧠", "label": "Qu'est-ce que l'IA ?",
             "content": "L'IA aide les professionnels à traiter l'information,\ngénérer du contenu et soutenir les tâches quotidiennes."},
            {"icon": "⚡", "label": "IA vs Automatisation classique",
             "content": "Automatisation : règles fixes, tâches répétitives, résultats prévisibles.\nIA : apprentissage adaptatif, résolution complexe, génération créative."},
            {"icon": "💼", "label": "Usages courants au travail",
             "content": "· Résumer des notes\n· Rédiger des emails\n· Organiser des informations\n· Générer des idées"},
            {"icon": "👤", "label": "Le jugement humain reste essentiel",
             "content": "L'IA peut se tromper. Les professionnels doivent relire,\ncontextualiser et prendre les décisions finales."},
            {"icon": "🎯", "label": "Pourquoi la culture IA est importante + Action",
             "content": "L'IA devient une compétence clé au travail.\nLes professionnels doivent en comprendre les bénéfices et les limites.\n→ Identifie 1 tâche quotidienne où l'IA pourrait t'aider aujourd'hui."},
        ],
        "takeaway": "L'IA booste la productivité, mais le jugement humain\nreste indispensable pour un usage responsable.",
        "footer":   "euklydia.com · #AILiteracy",
    },
    2: {
        "badge":    "MODULE 2 · DÉBUTANT",
        "badge_color": MEDIUM_GREEN,
        "title":    "Comprendre l'IA Générative",
        "subtitle": "Ce qu'elle est, ce qu'elle peut créer,\net comment l'utiliser de façon responsable",
        "sections": [
            {"icon": "✨", "label": "Qu'est-ce que l'IA générative ?",
             "content": "Un outil capable de produire du contenu à partir d'une instruction :\ntexte, résumés, idées, plans."},
            {"icon": "📝", "label": "Ce qu'elle peut générer",
             "content": "· Textes et emails\n· Résumés de documents\n· Idées et plans d'action"},
            {"icon": "🔄", "label": "Différence avec l'IA classique",
             "content": "L'IA classique automatise.\nL'IA générative crée et transforme du contenu."},
            {"icon": "⚠️", "label": "Limites à connaître",
             "content": "Elle peut produire des erreurs ou des approximations.\nToujours vérifier avant d'utiliser."},
            {"icon": "🎯", "label": "À retenir + Action",
             "content": "L'IA générative accélère la création — mais la validation reste humaine.\n→ Identifie 1 type de contenu que l'IA pourrait t'aider à rédiger."},
        ],
        "takeaway": "L'IA générative est puissante, mais chaque résultat\ndoit être relu avant utilisation.",
        "footer":   "euklydia.com · #GenerativeAI",
    },
    3: {
        "badge":    "MODULE 3 · DÉBUTANT",
        "badge_color": MEDIUM_GREEN,
        "title":    "L'Essentiel du Prompting",
        "subtitle": "Comment rédiger des instructions claires\npour obtenir de bons résultats avec l'IA",
        "sections": [
            {"icon": "💬", "label": "Qu'est-ce qu'un prompt ?",
             "content": "Une instruction donnée à un outil d'IA\npour obtenir un résultat précis et utile."},
            {"icon": "🧩", "label": "Les 3 éléments d'un bon prompt",
             "content": "1. Tâche claire — que veux-tu obtenir ?\n2. Contexte utile — qui, quoi, pourquoi ?\n3. Format attendu — liste, email, résumé ?"},
            {"icon": "📋", "label": "Exemple pratique",
             "content": "Faible : \"Écris un email.\"\nFort : \"Écris un email de relance client, ton professionnel, 3 phrases max.\""},
            {"icon": "🔁", "label": "Si le résultat n'est pas bon",
             "content": "Reformule, ajoute du contexte, précise le format. Itère."},
            {"icon": "🎯", "label": "À retenir + Action",
             "content": "Un bon prompt = tâche + contexte + format.\n→ Prends une vraie demande et reformule-la en prompt structuré."},
        ],
        "takeaway": "De meilleurs prompts donnent de meilleurs résultats —\nsois toujours précis.",
        "footer":   "euklydia.com · #Prompting",
    },
    4: {
        "badge":    "MODULE 4 · INTERMÉDIAIRE",
        "badge_color": DARK_GREEN,
        "title":    "Évaluer les Réponses de l'IA",
        "subtitle": "Comment relire et valider les résultats de l'IA\navant de les utiliser au travail",
        "sections": [
            {"icon": "🔍", "label": "Pourquoi vérifier ?",
             "content": "L'IA peut produire des réponses incorrectes, floues ou inadaptées.\nLa vérification est obligatoire."},
            {"icon": "✅", "label": "Les 4 critères d'évaluation",
             "content": "1. Exactitude — l'information est-elle correcte ?\n2. Pertinence — répond-elle bien à la demande ?\n3. Clarté — est-ce lisible et compréhensible ?\n4. Complétude — manque-t-il quelque chose ?"},
            {"icon": "🚨", "label": "Signaux d'alerte",
             "content": "· Réponse trop générale\n· Informations invérifiables\n· Ton ou format inadapté"},
            {"icon": "✏️", "label": "Quand corriger ?",
             "content": "Dès qu'un doute existe. Ne jamais utiliser sans relecture."},
            {"icon": "🎯", "label": "À retenir + Action",
             "content": "Toujours relire avant d'utiliser. Le jugement humain est indispensable.\n→ Prends une réponse IA récente et évalue-la selon les 4 critères."},
        ],
        "takeaway": "L'IA fait gagner du temps, mais seul l'humain\npeut valider la qualité et le contexte.",
        "footer":   "euklydia.com · #AIEvaluation",
    },
    5: {
        "badge":    "MODULE 5 · DÉBUTANT",
        "badge_color": MEDIUM_GREEN,
        "title":    "L'IA Responsable en Pratique",
        "subtitle": "Comment utiliser l'IA de façon sûre, éthique\net avec le bon niveau de supervision humaine",
        "sections": [
            {"icon": "🛡️", "label": "Pourquoi c'est important ?",
             "content": "L'IA mal utilisée peut exposer des données sensibles\nou produire des résultats biaisés."},
            {"icon": "⚠️", "label": "Les 3 risques principaux",
             "content": "1. Confidentialité — ne jamais partager de données sensibles\n2. Biais — les résultats peuvent être injustes ou inexacts\n3. Dépendance — ne jamais remplacer le jugement humain"},
            {"icon": "✅", "label": "Bonnes pratiques",
             "content": "· Anonymiser les données avant usage\n· Vérifier les résultats pour la neutralité\n· Garder un contrôle humain sur les décisions"},
            {"icon": "🚫", "label": "Quand limiter l'usage ?",
             "content": "Décisions RH, données personnelles, contextes légaux ou sensibles."},
            {"icon": "🎯", "label": "À retenir + Action",
             "content": "Utiliser l'IA avec discernement, pas à l'aveugle.\n→ Identifie 1 situation dans ton travail où l'usage de l'IA doit être encadré."},
        ],
        "takeaway": "Un usage responsable de l'IA protège les données,\névite les biais et garde l'humain aux commandes.",
        "footer":   "euklydia.com · #ResponsibleAI",
    },
    6: {
        "badge":    "MODULE 6 · INTERMÉDIAIRE",
        "badge_color": DARK_GREEN,
        "title":    "Utiliser l'IA dans ses Workflows Quotidiens",
        "subtitle": "Comment intégrer l'IA dans les tâches quotidiennes\npour gagner du temps et travailler plus efficacement",
        "sections": [
            {"icon": "🔄", "label": "Qu'est-ce qu'un workflow ?",
             "content": "Une suite de tâches réalisées régulièrement\ndans un contexte professionnel."},
            {"icon": "💡", "label": "Où l'IA apporte de la valeur",
             "content": "· Tâches répétitives et chronophages\n· Rédaction, résumé, organisation\n· Préparation et planification"},
            {"icon": "📊", "label": "Méthode en 3 étapes",
             "content": "1. Identifier une tâche récurrente\n2. Tester l'IA sur cette tâche\n3. Vérifier, ajuster, répéter"},
            {"icon": "👔", "label": "Exemple métier",
             "content": "Chef de projet : résume les réunions\n→ liste les actions → vérifie avant partage."},
            {"icon": "🎯", "label": "À retenir + Action",
             "content": "L'IA crée de la valeur quand elle est intégrée de façon pratique.\n→ Liste 3 tâches récurrentes où l'IA pourrait t'aider dès cette semaine."},
        ],
        "takeaway": "L'IA dans ton workflow, c'est travailler mieux —\npas seulement plus vite.",
        "footer":   "euklydia.com · #AIWorkflow",
    },
}

MODULES_DATA = {"en": MODULES_EN, "fr": MODULES_FR}

# ─────────────────────────────────────────────
# RENDU
# ─────────────────────────────────────────────

def draw_infographic(module_id: int, lang: str, font_paths: dict) -> None:
    data = MODULES_DATA[lang][module_id]
    W, H = 900, 1125

    img  = Image.new("RGB", (W, H), hex_to_rgb(BG))
    draw = ImageDraw.Draw(img)

    # Polices
    sz = {
        "badge":    max(14, int(H * 0.021)),
        "title":    max(22, int(H * 0.036)),
        "subtitle": max(13, int(H * 0.019)),
        "label":    max(14, int(H * 0.023)),
        "body":     max(13, int(H * 0.019)),
        "takeaway": max(13, int(H * 0.021)),
        "footer":   max(12, int(H * 0.017)),
        "icon":     max(18, int(H * 0.028)),
    }
    fb = font_paths["bold"]
    fr = font_paths["regular"]
    fonts = {k: ImageFont.truetype(fb if k in ("badge","title","label") else fr, v)
             for k, v in sz.items()}

    # Essayer de charger une police emoji système
    emoji_font = None
    emoji_candidates = [
        "C:/Windows/Fonts/seguiemj.ttf",   # Windows Segoe UI Emoji
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for ep in emoji_candidates:
        if Path(ep).exists():
            try:
                emoji_font = ImageFont.truetype(ep, sz["icon"])
                break
            except Exception:
                pass
    if emoji_font is None:
        emoji_font = fonts["body"]

    margin   = int(W * 0.06)
    card_pad = int(W * 0.04)
    icon_w   = int(W * 0.07)
    accent_w = 5
    lh_body  = sz["body"] + int(H * 0.006)
    lh_label = sz["label"] + int(H * 0.006)
    pad_v    = int(H * 0.013)
    gap      = int(H * 0.009)
    y        = int(H * 0.028)

    # ── Badge ──
    badge_color = data.get("badge_color", MEDIUM_GREEN)
    bb = draw.textbbox((0, 0), data["badge"], font=fonts["badge"])
    bw = bb[2] - bb[0] + card_pad * 2
    bh = bb[3] - bb[1] + int(H * 0.014)
    bx = (W - bw) // 2
    draw.rounded_rectangle([bx, y, bx + bw, y + bh], radius=16, fill=hex_to_rgb(badge_color))
    draw.text((bx + card_pad, y + int(H * 0.007)), data["badge"], font=fonts["badge"], fill=hex_to_rgb(WHITE))
    y += bh + int(H * 0.016)

    # ── Titre ──
    for line in data["title"].split("\n"):
        bb = draw.textbbox((0, 0), line, font=fonts["title"])
        draw.text(((W - (bb[2] - bb[0])) // 2, y), line, font=fonts["title"], fill=hex_to_rgb(DARK_GREEN))
        y += bb[3] - bb[1] + int(H * 0.005)
    y += int(H * 0.003)

    # ── Séparateur ──
    sep_w = int(W * 0.12)
    draw.rounded_rectangle(
        [(W - sep_w) // 2, y, (W + sep_w) // 2, y + 3],
        radius=2, fill=hex_to_rgb(MEDIUM_GREEN)
    )
    y += int(H * 0.014)

    # ── Sous-titre ──
    for line in data["subtitle"].split("\n"):
        bb = draw.textbbox((0, 0), line, font=fonts["subtitle"])
        draw.text(((W - (bb[2] - bb[0])) // 2, y), line, font=fonts["subtitle"], fill=hex_to_rgb(BODY_LIGHT))
        y += bb[3] - bb[1] + int(H * 0.004)
    y += int(H * 0.016)

    # ── Sections ──
    for section in data["sections"]:
        lines  = section["content"].split("\n")
        card_h = pad_v + lh_label + int(H * 0.004) + len(lines) * lh_body + pad_v

        # Carte blanche avec ombre légère (simulée)
        shadow_offset = 3
        draw.rounded_rectangle(
            [margin + shadow_offset, y + shadow_offset,
             W - margin + shadow_offset, y + card_h + shadow_offset],
            radius=10, fill=(220, 230, 225)
        )
        # Carte principale
        draw.rounded_rectangle(
            [margin, y, W - margin, y + card_h],
            radius=10, fill=hex_to_rgb(WHITE),
            outline=hex_to_rgb(BORDER), width=1,
        )
        # Accent vert gauche
        draw.rounded_rectangle(
            [margin, y, margin + accent_w, y + card_h],
            radius=10, fill=hex_to_rgb(MEDIUM_GREEN)
        )

        # Icône
        icon_x = margin + accent_w + int(W * 0.025)
        icon_y = y + pad_v
        try:
            draw.text((icon_x, icon_y), section["icon"], font=emoji_font, fill=hex_to_rgb(MEDIUM_GREEN), embedded_color=True)
        except Exception:
            draw.text((icon_x, icon_y), "•", font=fonts["label"], fill=hex_to_rgb(MEDIUM_GREEN))

        # Label
        text_x = icon_x + icon_w
        draw.text((text_x, y + pad_v), section["label"], font=fonts["label"], fill=hex_to_rgb(DARK_GREEN))

        # Contenu
        cy = y + pad_v + lh_label + int(H * 0.002)
        for line in lines:
            draw.text((text_x, cy), line, font=fonts["body"], fill=hex_to_rgb(BODY))
            cy += lh_body

        y += card_h + gap

    y += int(H * 0.012)

    # ── Takeaway encadré ──
    takeaway_lines = data["takeaway"].split("\n")
    tk_h = pad_v * 2 + len(takeaway_lines) * (sz["takeaway"] + int(H * 0.006))
    draw.rounded_rectangle(
        [margin, y, W - margin, y + tk_h],
        radius=10, fill=hex_to_rgb(DARK_GREEN)
    )
    ty = y + pad_v
    for line in takeaway_lines:
        bb = draw.textbbox((0, 0), line, font=fonts["takeaway"])
        draw.text(((W - (bb[2] - bb[0])) // 2, ty), line, font=fonts["takeaway"], fill=hex_to_rgb(WHITE))
        ty += bb[3] - bb[1] + int(H * 0.006)
    y += tk_h + int(H * 0.014)

    # ── Footer ──
    bb = draw.textbbox((0, 0), data["footer"], font=fonts["footer"])
    draw.text(((W - (bb[2] - bb[0])) // 2, y), data["footer"], font=fonts["footer"], fill=hex_to_rgb(BODY_LIGHT))

    # ── Logo ──
    logo_path = BASE_DIR / "assets" / "images" / "logo-full.png"
    if logo_path.exists():
        logo  = Image.open(logo_path).convert("RGBA")
        max_w = int(W * 0.22)
        if logo.width > max_w:
            ratio = max_w / logo.width
            logo  = logo.resize((max_w, int(logo.height * ratio)), Image.LANCZOS)
        img.paste(logo, (W - logo.width - int(W * 0.05), H - logo.height - int(H * 0.012)), mask=logo)

    # ── Sauvegarde ──
    out_dir  = OUTPUT_BASE / f"module_{module_id}" / lang
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "infographic_v1.png"
    img.save(out_path, "PNG")
    print(f"  ✅ [{lang.upper()}] Sauvegardée : {out_path.resolve()}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Euklydia — Génération infographies (Pillow)")
    parser.add_argument("--module", type=int, help="Numéro du module (1-6)")
    parser.add_argument("--all",    action="store_true", help="Générer tous les modules")
    parser.add_argument("--lang",   type=str, default="both", choices=["en", "fr", "both"])
    args = parser.parse_args()

    if not args.module and not args.all:
        parser.print_help()
        return

    print("🚀 Euklydia Academy — Génération infographies (Pillow)")
    font_paths = ensure_fonts()
    print("─" * 50)

    modules = list(range(1, 7)) if args.all else [args.module]
    langs   = ["en", "fr"] if args.lang == "both" else [args.lang]

    for mid in modules:
        for lang in langs:
            flag = "🇬🇧" if lang == "en" else "🇫🇷"
            print(f"\n{flag} Module {mid} [{lang.upper()}]...")
            draw_infographic(mid, lang, font_paths)

    print("\n✅ Terminé.")


if __name__ == "__main__":
    main()