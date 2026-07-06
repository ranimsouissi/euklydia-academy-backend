# app/services/recommendation_service.py
"""
Adaptive Recommendation Service
=================================
Étend sequencing_service avec 3 features :

Feature 1 — Section à revoir dans le module actuel
    → Selon mastery + KPI after + difficulté déclarée
    → Retourne : section précise (tutorials / execution_content / use_case…)

Feature 2 — Plan de micro-sessions hebdomadaire
    → Lit time_available_per_week depuis user_profiles
    → Calcule nb sessions × durée selon modules restants

Feature 3 — Détection stagnation + suggestion reset
    → Execution Task non soumise depuis STAGNATION_DAYS_THRESHOLD jours
    → KPI after stagnant sur STAGNATION_MODULES_THRESHOLD modules consécutifs
    → Retourne une alerte + message de reset

Endpoint principal : GET /recommendation/full
"""

import json
from datetime import datetime, timezone, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from openai import OpenAI

from app.core.config import settings
from app.services.sequencing_service import get_learner_roadmap, generate_next_recommendation

# ─────────────────────────────────────────────
# Seuils configurables (modifiables facilement)
# ─────────────────────────────────────────────
STAGNATION_DAYS_THRESHOLD    = 7   # jours sans Execution Task soumise
STAGNATION_MODULES_THRESHOLD = 2   # modules consécutifs avec KPI after stagnant
MASTERY_REVIEW_THRESHOLD     = 0.6 # mastery < 60% → section à revoir
SESSION_DURATION_MINUTES     = 45  # durée d'une micro-session en minutes
HOURS_PER_MODULE             = 2   # estimation heures nécessaires par module


def _get_client() -> OpenAI:
    return OpenAI(api_key=settings.OPENAI_API_KEY)


# ══════════════════════════════════════════════════════════
# FEATURE 1 — Section à revoir dans le module actuel
# ══════════════════════════════════════════════════════════

def get_section_to_review(
    db:                Session,
    user_id:           int,
    current_module_id: int
) -> dict:
    """
    Analyse le module actuel et recommande la section précise à revoir.

    Logique de priorité :
    1. Execution Task non soumise → soumettre d'abord
    2. KPI after absent → mesurer le KPI
    3. Difficulté déclarée élevée → revoir Tutorials
    4. Mastery < seuil → revoir Execution Content
    5. Mastery suffisante → rien à revoir dans ce module
    """
    roadmap = get_learner_roadmap(db, user_id)
    modules = roadmap["modules"]

    current = next(
        (m for m in modules if m["id"] == current_module_id), None
    )
    if not current:
        return {"section": None, "reason": "Module introuvable", "action": None}

    mastery        = float(current.get("mastery_score") or 0)
    kpi_after      = current.get("kpi_after")
    task_submitted = current.get("execution_task_submitted", False)
    difficulty     = (current.get("execution_task_difficulty") or "").lower()

    # Règle 1 — Execution Task non soumise
    if not task_submitted:
        return {
            "section":        "execution_task",
            "section_label":  "Execution Task",
            "reason":         "Tu n'as pas encore soumis ton Execution Task. C'est l'étape clé pour valider ce module.",
            "action":         "submit_execution_task",
            "expected_result": "Valider ta mise en pratique et débloquer la mesure de KPI."
        }

    # Règle 2 — KPI after absent
    if not kpi_after:
        return {
            "section":        "kpi_measurement",
            "section_label":  "KPI Measurement",
            "reason":         "Tu n'as pas encore mesuré ton KPI après. C'est essentiel pour évaluer ta progression.",
            "action":         "measure_kpi",
            "expected_result": "Obtenir une mesure concrète de l'impact de ta pratique."
        }

    # Règle 3 — Difficulté élevée → revoir Tutorials
    if difficulty in ("élevée", "haute", "difficile", "high", "hard", "très difficile"):
        return {
            "section":        "tutorials",
            "section_label":  "Tutorials",
            "reason":         "Tu as déclaré une difficulté élevée sur l'Execution Task. Reprends les tutoriels pas à pas.",
            "action":         "review_tutorials",
            "expected_result": "Mieux maîtriser les outils et techniques avant de retenter."
        }

    # Règle 4 — Mastery insuffisante → revoir Execution Content
    if mastery < MASTERY_REVIEW_THRESHOLD:
        return {
            "section":        "execution_content",
            "section_label":  "Execution Content",
            "reason":         f"Ta mastery est de {round(mastery * 100)}% — en dessous du seuil recommandé (60%). Revois les templates et workflows.",
            "action":         "review_execution_content",
            "expected_result": "Consolider les bases avant de passer au module suivant."
        }

    # Règle 5 — Tout est bon
    return {
        "section":        None,
        "section_label":  None,
        "reason":         f"Bonne maîtrise ({round(mastery * 100)}%) — tu peux avancer au module suivant.",
        "action":         "proceed_next_module",
        "expected_result": "Progresser dans ton parcours."
    }


# ══════════════════════════════════════════════════════════
# FEATURE 2 — Plan de micro-sessions hebdomadaire
# ══════════════════════════════════════════════════════════

def get_weekly_session_plan(
    db:      Session,
    user_id: int
) -> dict:
    """
    Génère un plan de micro-sessions basé sur :
    - time_available_per_week (depuis user_profiles)
    - Nombre de modules restants (non complétés)

    Retourne :
    - sessions_per_week : nb de sessions recommandées par semaine
    - session_duration_min : durée de chaque session
    - estimated_weeks : nb de semaines pour terminer le parcours
    - plan_description : texte lisible pour l'apprenant
    """
    roadmap        = get_learner_roadmap(db, user_id)
    time_available = roadmap.get("time_available_per_week")  # en heures
    modules        = roadmap["modules"]

    # Modules restants (non complétés, uniques par id)
    seen     = set()
    remaining = []
    for m in modules:
        if m["id"] not in seen and m.get("module_status") != "completed":
            seen.add(m["id"])
            remaining.append(m)

    modules_remaining_count = len(remaining)

    # Pas de temps déclaré → message d'invitation à renseigner
    if not time_available:
        return {
            "has_plan":               False,
            "modules_remaining":      modules_remaining_count,
            "plan_description":       "Renseigne ton temps disponible par semaine dans ton profil pour obtenir un plan personnalisé.",
            "sessions_per_week":      None,
            "session_duration_min":   None,
            "estimated_weeks":        None,
            "cta":                    "update_profile"
        }

    # Calcul du plan
    total_hours_needed  = modules_remaining_count * HOURS_PER_MODULE
    session_duration_h  = SESSION_DURATION_MINUTES / 60
    sessions_possible   = int(time_available / session_duration_h)
    sessions_per_week   = max(1, min(sessions_possible, 5))  # entre 1 et 5 sessions/semaine

    if sessions_per_week > 0:
        hours_per_week    = sessions_per_week * session_duration_h
        estimated_weeks   = round(total_hours_needed / hours_per_week) if hours_per_week > 0 else None
    else:
        estimated_weeks   = None

    # Message lisible
    if modules_remaining_count == 0:
        plan_description = "Félicitations — tu as complété tous les modules de ton parcours !"
    elif estimated_weeks and estimated_weeks <= 1:
        plan_description = (
            f"Avec {time_available}h/semaine, tu peux terminer tes {modules_remaining_count} modules restants "
            f"en {sessions_per_week} session(s) de {SESSION_DURATION_MINUTES} min cette semaine."
        )
    else:
        plan_description = (
            f"Avec {time_available}h disponibles par semaine : "
            f"{sessions_per_week} session(s) de {SESSION_DURATION_MINUTES} min — "
            f"{modules_remaining_count} modules restants — "
            f"objectif en ~{estimated_weeks} semaine(s)."
        )

    return {
        "has_plan":             True,
        "modules_remaining":    modules_remaining_count,
        "time_available_hours": time_available,
        "sessions_per_week":    sessions_per_week,
        "session_duration_min": SESSION_DURATION_MINUTES,
        "estimated_weeks":      estimated_weeks,
        "plan_description":     plan_description,
        "cta":                  None
    }


# ══════════════════════════════════════════════════════════
# FEATURE 3 — Détection stagnation + suggestion reset
# ══════════════════════════════════════════════════════════

def _get_last_execution_task_date(db: Session, user_id: int) -> Optional[datetime]:
    """Retourne la date de la dernière Execution Task soumise."""
    row = db.execute(text("""
        SELECT updated_at
        FROM user_module_progress
        WHERE user_id = :uid
          AND execution_task_submitted = true
        ORDER BY updated_at DESC
        LIMIT 1
    """), {"uid": user_id}).fetchone()

    if row and row.updated_at:
        dt = row.updated_at
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    return None


def _get_consecutive_stagnant_kpi_count(db: Session, user_id: int) -> int:
    """
    Compte les modules consécutifs (les plus récents) où le KPI after
    est absent ou identique au KPI before → stagnation.
    """
    rows = db.execute(text("""
        SELECT m.kpi_before_fr, ump.kpi_after
        FROM user_module_progress ump
        JOIN modules m ON m.id = ump.module_id
        WHERE ump.user_id = :uid
          AND ump.execution_task_submitted = true
        ORDER BY ump.updated_at DESC
        LIMIT 5
    """), {"uid": user_id}).fetchall()

    consecutive = 0
    for row in rows:
        kpi_after = (row.kpi_after or "").strip()
        # KPI stagnant = absent, vide, ou identique au before
        if not kpi_after or kpi_after == (row.kpi_before_fr or "").strip():
            consecutive += 1
        else:
            break  # dès qu'un KPI est renseigné et différent → on arrête

    return consecutive


def detect_stagnation(db: Session, user_id: int) -> dict:
    """
    Détecte la stagnation selon 2 signaux :
    1. Execution Task non soumise depuis X jours
    2. KPI after stagnant sur N modules consécutifs

    Retourne :
    - is_stagnating : bool
    - signals : liste des signaux détectés
    - reset_message : message d'encouragement + plan de reset
    - days_since_last_task : int ou None
    - stagnant_modules_count : int
    """
    now = datetime.now(timezone.utc)

    # Signal 1 — jours depuis dernière Execution Task
    last_task_date      = _get_last_execution_task_date(db, user_id)
    days_since_last     = None
    signal_days         = False

    if last_task_date:
        days_since_last = (now - last_task_date).days
        signal_days     = days_since_last >= STAGNATION_DAYS_THRESHOLD
    else:
        # Aucune task soumise → vérifier si inscrit depuis > X jours
        reg_row = db.execute(text(
            "SELECT created_at FROM users WHERE id = :uid"
        ), {"uid": user_id}).fetchone()
        if reg_row and reg_row.created_at:
            created = reg_row.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            days_since_last = (now - created).days
            signal_days     = days_since_last >= STAGNATION_DAYS_THRESHOLD

    # Signal 2 — modules consécutifs avec KPI stagnant
    stagnant_count  = _get_consecutive_stagnant_kpi_count(db, user_id)
    signal_kpi      = stagnant_count >= STAGNATION_MODULES_THRESHOLD

    # Résultat
    signals = []
    if signal_days:
        signals.append({
            "type":    "no_execution_task",
            "message": f"Aucune Execution Task soumise depuis {days_since_last} jours."
        })
    if signal_kpi:
        signals.append({
            "type":    "stagnant_kpi",
            "message": f"KPI after non amélioré sur {stagnant_count} modules consécutifs."
        })

    is_stagnating = len(signals) > 0

    reset_message = None
    if is_stagnating:
        if signal_days and signal_kpi:
            reset_message = (
                f"Tu sembles bloqué depuis {days_since_last} jours et ton KPI n'a pas progressé "
                f"sur tes derniers modules. Pas d'inquiétude — reprends par une seule section courte "
                f"(15 min) pour te remettre en mouvement. Petite action, grand impact."
            )
        elif signal_days:
            reset_message = (
                f"Ça fait {days_since_last} jours sans activité. "
                f"Reprends avec une session courte de 15 min sur l'Execution Task du module en cours."
            )
        else:
            reset_message = (
                f"Ton KPI n'a pas progressé sur tes {stagnant_count} derniers modules. "
                f"Revois les Tutorials — parfois un seul outil bien maîtrisé change tout."
            )

    return {
        "is_stagnating":          is_stagnating,
        "signals":                signals,
        "days_since_last_task":   days_since_last,
        "stagnant_modules_count": stagnant_count,
        "reset_message":          reset_message
    }


# ══════════════════════════════════════════════════════════
# ORCHESTRATION — Endpoint principal /recommendation/full
# ══════════════════════════════════════════════════════════
def save_recommendation(
    db:       Session,
    user_id:  int,
    module_id: int,
    section_review: Optional[str],
    stagnation_alert: bool,
    recommendation_summary: Optional[str]
) -> None:
    """Stocke la recommandation — évite les doublons du même jour."""
    existing = db.execute(text("""
        SELECT id FROM user_recommendations
        WHERE user_id = :user_id
          AND module_id = :module_id
          AND section_review IS NOT DISTINCT FROM :section_review
          AND DATE(created_at) = CURRENT_DATE
        LIMIT 1
    """), {
        "user_id":        user_id,
        "module_id":      module_id,
        "section_review": section_review
    }).fetchone()

    if existing:
        return  # Doublon détecté — ne pas réinsérer

    db.execute(text("""
        INSERT INTO user_recommendations
            (user_id, module_id, section_review, stagnation_alert, recommendation_summary)
        VALUES
            (:user_id, :module_id, :section_review, :stagnation_alert, :recommendation_summary)
    """), {
        "user_id":                user_id,
        "module_id":              module_id,
        "section_review":         section_review,
        "stagnation_alert":       stagnation_alert,
        "recommendation_summary": recommendation_summary
    })
    db.commit()
def get_full_recommendation(
    db:                Session,
    user_id:           int,
    current_module_id: int
) -> dict:
    next_module    = generate_next_recommendation(db, user_id, current_module_id)
    section_review = get_section_to_review(db, user_id, current_module_id)
    session_plan   = get_weekly_session_plan(db, user_id)
    stagnation     = detect_stagnation(db, user_id)

    # Stocker la recommandation pour Agent 1
    section_name = section_review.get("section") if section_review else None
    is_stagnant  = stagnation.get("stagnation_detected", False) if stagnation else False
    summary      = section_review.get("reason") if section_review else None

    save_recommendation(
        db=db,
        user_id=user_id,
        module_id=current_module_id,
        section_review=section_name,
        stagnation_alert=is_stagnant,
        recommendation_summary=summary
    )

    return {
        "next_module":    next_module,
        "section_review": section_review,
        "session_plan":   session_plan,
        "stagnation":     stagnation
    }
def get_recommendation_history(
    db: Session,
    user_id: int,
    limit: int = 5
) -> list[dict]:
    """Retourne les dernières recommandations de l'apprenant."""
    rows = db.execute(text("""
        SELECT ur.id, ur.module_id, m.title_fr AS module_title,
               ur.section_review, ur.stagnation_alert,
               ur.recommendation_summary, ur.created_at
        FROM user_recommendations ur
        JOIN modules m ON m.id = ur.module_id
        WHERE ur.user_id = :user_id
        ORDER BY ur.created_at DESC
        LIMIT :limit
    """), {"user_id": user_id, "limit": limit}).fetchall()

    return [dict(r._mapping) for r in rows]