"""
Seed des 4 career paths — Euklydia Academy Phase 1
IDs fixes 79-82 pour correspondance avec les seeds de skills/modules.
"""
from sqlalchemy import text
from app.models.career_path import CareerPath


CAREER_PATHS = [
    {
        "id": 79,
        "name": "AI Sales Specialist",
        "description": "Spécialiste AI de la prospection, du scoring de leads et de la personnalisation commerciale.",
    },
    {
        "id": 80,
        "name": "AI Marketing Strategist",
        "description": "Stratège AI du contenu, du SEO et de l'analyse d'audience en contexte Maghreb.",
    },
    {
        "id": 81,
        "name": "AI Designer",
        "description": "Designer AI spécialisé en création visuelle, branding et design adaptatif bilingue FR/EN.",
    },
    {
        "id": 82,
        "name": "AI Project Manager",
        "description": "Chef de projet AI pour la planification, le suivi et la livraison de projets d'IA en entreprise.",
    },
]


def seed_career_paths(db):
    # =============================
    # 0. Anti-doublon — skip si déjà seedé
    # =============================
    existing = db.query(CareerPath).filter(CareerPath.id.in_([79, 80, 81, 82])).count()
    if existing == 4:
        print("⚠️  Career paths déjà seedés (79-82), skip.")
        return

    # =============================
    # 1. Insérer les 4 career paths avec IDs forcés
    # =============================
    for cp_data in CAREER_PATHS:
        existing_cp = db.query(CareerPath).filter(CareerPath.id == cp_data["id"]).first()
        if existing_cp:
            continue
        cp = CareerPath(**cp_data)
        db.add(cp)

    db.flush()

    # =============================
    # 2. Resync la séquence Postgres pour que les prochains IDs > 82
    # =============================
    db.execute(text("SELECT setval('career_paths_id_seq', 82, true);"))

    print("✅ Career paths seedés : AI Sales (79), AI Marketing (80), AI Designer (81), AI Project Manager (82)")