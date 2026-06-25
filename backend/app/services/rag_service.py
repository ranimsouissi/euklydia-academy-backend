# app/services/rag_service.py
import json
from typing import Optional

from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.models.coaching_session import CoachingSession, Event

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY manquant dans .env")
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def embed_text(text_input: str) -> list[float]:
    client = _get_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text_input
    )
    return response.data[0].embedding


# ── Remplace get_module_lesson_ids ───────────────────────────
def get_module_chunk_ids(
    db:           Session,
    module_id:    int,
    section_type: str
) -> list[int]:
    """
    Récupère les IDs des chunks RAG
    filtrés par module_id et section_type.
    Remplace get_module_lesson_ids — accès direct via module_id.
    """
    result = db.execute(
        text(
            "SELECT id FROM content_chunks "
            "WHERE module_id = :module_id "
            "AND section_type = :section_type "
            "AND is_active = true"
        ),
        {"module_id": module_id, "section_type": section_type}
    )
    return [row[0] for row in result]


def search_chunks(
    db:           Session,
    module_id:    int,
    section_type: str,        # gardé pour compatibilité de signature
    embedding:    list[float],
    top_k:        int = 4
) -> list[dict]:
    """
    Recherche les chunks RAG les plus pertinents pour un module.
    Structure réelle : source_type='module' + source_id=module_id
    """
    vector_str = "[" + ",".join(map(str, embedding)) + "]"

    result = db.execute(
        text(
            "SELECT id AS chunk_id, chunk_text, citation_ref, "
            "embedding <=> CAST(:vec AS vector) AS distance "
            "FROM content_chunks "
            "WHERE source_type = 'module' "
            "AND source_id = :module_id "
            "ORDER BY distance ASC LIMIT :top_k"
        ),
        {
            "vec":       vector_str,
            "module_id": module_id,
            "top_k":     top_k
        }
    )
    rows = [dict(row._mapping) for row in result]

    relevant_rows = [r for r in rows if float(r.get("distance", 1.0)) < 0.7]
    return relevant_rows if relevant_rows else []


def get_session_history(db: Session, session_id: int) -> list[dict]:
    session = db.query(CoachingSession).filter(
        CoachingSession.id == session_id
    ).first()
    if session and session.messages:
        return session.messages if isinstance(session.messages, list) else []
    return []


def get_learner_profile(db: Session, user_id: int) -> dict:
    profile = {
        "global_score": None,
        "level":        None,
        "skills":       [],
        "modules_completed":   [],
        "modules_in_progress": [],
        "pain_points_count":   0,
    }
    try:
        skill_rows = db.execute(
            text(
                "SELECT s.name, uss.score "
                "FROM user_skill_scores uss "
                "JOIN skills s ON s.id = uss.skill_id "
                "WHERE uss.user_id = :user_id ORDER BY uss.score ASC"
            ),
            {"user_id": user_id}
        ).fetchall()

        if skill_rows:
            profile["skills"] = [
                {"name": r.name, "score": r.score} for r in skill_rows
            ]
            scores = [r.score for r in skill_rows if r.score is not None]
            if scores:
                avg = round(sum(scores) / len(scores))
                profile["global_score"] = avg
                profile["level"] = (
                    "AI Novice"       if avg < 50  else
                    "AI Practitioner" if avg < 75  else
                    "AI Leader"
                )

        mod_rows = db.execute(
            text(
                "SELECT m.title_fr, ump.status, ump.progress_percent "
                "FROM user_module_progress ump "
                "JOIN modules m ON m.id = ump.module_id "
                "WHERE ump.user_id = :user_id ORDER BY ump.updated_at DESC"
            ),
            {"user_id": user_id}
        ).fetchall()

        for r in mod_rows:
            if r.status == "completed":
                profile["modules_completed"].append(r.title_fr)
            elif r.status == "in_progress":
                profile["modules_in_progress"].append(
                    {"title": r.title_fr, "progress": r.progress_percent}
                )

        pp_row = db.execute(
            text("SELECT COUNT(*) as cnt FROM pain_points WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        if pp_row:
            profile["pain_points_count"] = pp_row.cnt

        mastery_rows = db.execute(
            text(
                "SELECT s.name, lsm.mastery_score, lsm.mastery_level, "
                "lsm.evidence_count "
                "FROM learner_skill_mastery lsm "
                "JOIN skills s ON s.id = lsm.skill_id "
                "WHERE lsm.user_id = :user_id "
                "ORDER BY lsm.mastery_score ASC"
            ),
            {"user_id": user_id}
        ).fetchall()

        if mastery_rows:
            profile["mastery"] = [
                {
                    "name":          r.name,
                    "mastery_score": round(float(r.mastery_score) * 100),
                    "mastery_level": r.mastery_level,
                    "evidence_count": r.evidence_count,
                }
                for r in mastery_rows
            ]

    except Exception:
        try:
            db.rollback()
        except Exception:
            pass

    return profile


def format_learner_profile(profile: dict) -> str:
    if not profile.get("global_score") and not profile.get("skills"):
        return "Aucun résultat diagnostic disponible — premier accès à la plateforme."

    lines = []

    if profile.get("global_score"):
        lines.append(
            f"Score global : {profile['global_score']}% — "
            f"Niveau : {profile['level']}"
        )

    skills = profile.get("skills", [])
    if skills:
        weak = sorted(skills, key=lambda x: x.get("score") or 0)[:3]
        if weak:
            lines.append(
                "Compétences à renforcer : "
                + ", ".join(f"{s['name']} ({s['score']}%)" for s in weak)
            )
        strengths = sorted(
            skills, key=lambda x: x.get("score") or 0, reverse=True
        )[:2]
        if strengths:
            lines.append(
                "Points forts : "
                + ", ".join(f"{s['name']} ({s['score']}%)" for s in strengths)
            )

    if profile.get("modules_completed"):
        lines.append(
            "Modules complétés : " + ", ".join(profile["modules_completed"])
        )

    if profile.get("modules_in_progress"):
        in_prog = [
            f"{m['title']} ({m['progress']}%)"
            for m in profile["modules_in_progress"]
        ]
        lines.append("En cours : " + ", ".join(in_prog))

    mastery = profile.get("mastery", [])
    if mastery:
        mastery_text = ", ".join(
            f"{m['name']} : {m['mastery_score']}% ({m['mastery_level']})"
            for m in mastery
        )
        lines.append("Mastery actuelle : " + mastery_text)

    return "\n".join(lines) if lines else "Profil en cours de construction."


EUKLYDIA_MODULES = [
    {"id": 403, "title": "Lead Qualification Automation",
     "role": "AI Sales Specialist",
     "keywords": ["qualification", "leads", "BANT", "scoring", "CRM"]},
    {"id": 404, "title": "Personalized Outreach at Scale",
     "role": "AI Sales Specialist",
     "keywords": ["prospection", "email", "outreach", "reply rate", "LinkedIn"]},
    {"id": 405, "title": "Sales Call Preparation",
     "role": "AI Sales Specialist",
     "keywords": ["appel", "briefing", "objections", "closing", "CRM"]},
    {"id": 406, "title": "Content Strategy Optimization",
     "role": "AI Marketing Strategist",
     "keywords": ["contenu", "stratégie éditoriale", "blog", "newsletter"]},
    {"id": 407, "title": "Campaign Performance Optimization",
     "role": "AI Marketing Strategist",
     "keywords": ["campagne", "publicité", "A/B test", "CAC", "performance"]},
    {"id": 408, "title": "Audience Insights & Segmentation",
     "role": "AI Marketing Strategist",
     "keywords": ["audience", "segmentation", "personas", "ciblage"]},
    {"id": 409, "title": "Rapid Concept Generation",
     "role": "AI Designer",
     "keywords": ["design", "concepts", "idéation", "Midjourney"]},
    {"id": 410, "title": "UX Optimization",
     "role": "AI Designer",
     "keywords": ["UX", "expérience utilisateur", "Hotjar", "heuristiques"]},
    {"id": 411, "title": "Design System Automation",
     "role": "AI Designer",
     "keywords": ["design system", "composants", "Figma", "tokens"]},
    {"id": 412, "title": "Project Planning Automation",
     "role": "AI Project Manager",
     "keywords": ["planification", "projet", "Notion", "Asana", "roadmap"]},
    {"id": 413, "title": "Risk Identification",
     "role": "AI Project Manager",
     "keywords": ["risques", "retards", "mitigation", "playbook"]},
    {"id": 414, "title": "Team Productivity Optimization",
     "role": "AI Project Manager",
     "keywords": ["productivité", "équipe", "backlog", "sprint"]},
]

MODULES_CATALOGUE = "\n".join([
    f"- Module {m['id']} : {m['title']} ({m['role']}) "
    f"— mots-clés: {', '.join(m['keywords'][:4])}"
    for m in EUKLYDIA_MODULES
])


def call_llm(
    message:         str,
    chunks:          list[dict],
    history:         list[dict],
    learner_profile: dict = None,
    section_type:    str  = None,   # nouveau — Context Awareness
    kpi_baseline:    str  = None,   # nouveau — Context Awareness
) -> str:
    # ── Garde : aucun chunk pertinent → question hors contexte ──
    if not chunks:
        return (
            "❌ Cette question semble hors du contexte de ce module.\n\n"
            "Le contenu RAG de ce module ne couvre pas ce sujet.\n"
            "Voici quelques pistes :\n"
            "- Reformulez votre question en lien avec le module actuel\n"
            "- Consultez le module Euklydia correspondant\n\n"
            f"CATALOGUE DES MODULES EUKLYDIA :\n{MODULES_CATALOGUE}"
        )

    context = "\n\n".join([
        f"[{c['citation_ref']}] {c['chunk_text']}"
        for c in chunks
        if c.get("citation_ref")
    ])

    learner_context = (
        format_learner_profile(learner_profile)
        if learner_profile
        else "Aucun résultat disponible — premier accès à la plateforme."
    )

    # ── Label de la section en cours ────────────────────────
    section_label = {
        "use_case":          "Use Case — problème business",
        "kpi":               "KPI before/after",
        "execution_content": "Execution Content (Templates, Workflows, Tools)",
        "execution_task":    "Execution Task — application terrain",
        "kpi_measurement":   "KPI Measurement — mesure d'impact"
    }.get(section_type, "Module en cours")

    system_prompt = (
        "Tu es un tuteur expert de la plateforme Euklydia, "
        "une plateforme d'apprentissage IA pour les professionnels "
        "en Afrique du Nord.\n\n"
        f"SECTION EN COURS : {section_label}\n"
        f"KPI BASELINE : {kpi_baseline or 'non renseigné'}\n\n"
        "PROFIL DE L'APPRENANT (résultats passés) :\n"
        f"{learner_context}\n\n"
        "RÔLE PRINCIPAL : Répondre aux questions de l'apprenant "
        "en te basant sur le contenu du module.\n"
        "Utilise le profil ci-dessus pour personnaliser ta réponse.\n"
        "Cite tes sources avec leur référence entre crochets ex: [PR.405.1].\n\n"
        "EXEMPLES CONCRETS (important) :\n"
        "Quand tu expliques un concept, illustre TOUJOURS avec un exemple "
        "concret et pratique :\n"
        "- Utilise des noms et contextes réels du Maghreb\n"
        "- Tire l'exemple directement du contenu du module si disponible\n"
        "- Format : après l'explication théorique, ajoute "
        "'📌 Exemple concret :' suivi d'une situation réelle\n\n"
        "RÔLE SECONDAIRE — PLAN D'ACTION QUOTIDIEN :\n"
        "Si la question révèle un problème business réel :\n"
        "1. Réponds à sa question avec le contenu du module\n"
        "2. Génère un plan d'action concret en 3 étapes :\n"
        "   🗓 Plan d'action pour cette semaine :\n"
        "   Étape 1 — [action concrète, max 30 min]\n"
        "   Étape 2 — [action principale sur ses vraies données]\n"
        "   Étape 3 — [mesure d'impact à J+14]\n"
        "3. Suggère le module le plus pertinent si différent :\n"
        '   "💡 Pour aller plus loin : **[titre]** vous aidera à [bénéfice]."\n\n'
        "RÈGLES DU PLAN D'ACTION :\n"
        "- Génère le plan UNIQUEMENT si la question révèle un vrai problème\n"
        "- Ne génère PAS de plan pour les questions théoriques\n"
        "- Adapte au contexte Maghreb\n\n"
        f"CATALOGUE DES MODULES EUKLYDIA :\n{MODULES_CATALOGUE}\n\n"
        "--- CONTENU DU MODULE ---\n"
        f"{context}\n"
        "------------------------"
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages += history[-6:]
    messages.append({"role": "user", "content": message})

    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content


def save_chat(
    db:               Session,
    session_id:       int,
    user_id:          int,
    module_id:        int,        # remplace lesson_id
    section_type:     str,        # nouveau
    user_message:     str,
    assistant_answer: str,
    history:          list[dict]
):
    updated_history = history + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": assistant_answer}
    ]

    db.query(CoachingSession).filter(
        CoachingSession.id == session_id
    ).update({"messages": updated_history})

    event = Event(
        session_id=session_id,
        module_id=module_id,         # remplace lesson_id
        section_type=section_type,   # nouveau
        user_id=user_id,
        type="question_asked",
        payload={"message_preview": user_message[:100]}
    )
    db.add(event)
    db.commit()


def detect_pain_point(
    db:           Session,
    session_id:   int,
    user_id:      int,
    module_id:    int,        # remplace lesson_id
    section_type: str,        # nouveau
    user_message: str
):
    prompt = (
        "Analyse ce message d'un apprenant en contexte professionnel.\n"
        "S'il révèle une friction ou un problème business réel,\n"
        "retourne un JSON avec ces champs exactement :\n"
        "  {\n"
        '    "summary": "résumé du problème en 1 phrase",\n'
        '    "category": "process|tool|knowledge|time",\n'
        '    "severity": 1|2|3,\n'
        '    "confidence_score": 0.0 à 1.0\n'
        "  }\n\n"
        "Si aucun pain point détecté, retourne exactement : null\n\n"
        f'Message : "{user_message}"\n'
        "Réponds UNIQUEMENT avec le JSON ou null, sans texte autour."
    )

    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200
    )

    raw = (response.choices[0].message.content or "").strip()
    if raw.lower() == "null":
        return

    try:
        data = json.loads(raw)
        db.execute(
            text(
                "INSERT INTO pain_points "
                "(user_id, session_id, module_id, section_type, "
                "summary, category, severity, "
                "confidence_score, raw_message, source, captured_at) "
                "VALUES "
                "(:user_id, :session_id, :module_id, :section_type, "
                ":summary, :category, :severity, "
                ":confidence_score, :raw_message, 'coaching_agent', NOW())"
            ),
            {
                "user_id":          user_id,
                "session_id":       session_id,
                "module_id":        module_id,
                "section_type":     section_type,
                "summary":          data["summary"],
                "category":         data["category"],
                "severity":         data["severity"],
                "confidence_score": data.get("confidence_score", 0.8),
                "raw_message":      user_message[:500]
            }
        )
        event = Event(
            session_id=session_id,
            module_id=module_id,
            section_type=section_type,
            user_id=user_id,
            type="pain_point_detected",
            payload={
                "category": data["category"],
                "severity": data["severity"]
            }
        )
        db.add(event)
        db.commit()
    except (json.JSONDecodeError, KeyError):
        pass