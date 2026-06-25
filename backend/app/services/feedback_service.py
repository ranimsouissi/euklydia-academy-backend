# app/services/feedback_service.py
"""
Execution Task Feedback Service
================================
Génère un feedback post-soumission de l'Execution Task.

Rôle : Adaptive Engine Partie 3 — intervient APRÈS la soumission
       (l'Agent 1 intervient PENDANT l'apprentissage)

Sources de données :
  - kpi_before       : KPI baseline déclaré en début de module
  - kpi_after        : KPI mesuré après l'Execution Task
  - difficulty       : difficulté déclarée par l'apprenant
  - module_title     : titre du module pour contextualiser
  - tutorial_titles  : titres des tutoriels disponibles dans le module

Output :
  - feedback personnalisé
  - suggestion contextuelle (tutoriel précis ou section à revoir si besoin)
  - signal de progression (improving / stagnant / needs_review)
"""
import json
from typing import Optional
from openai import OpenAI
from app.core.config import settings


def _get_client() -> OpenAI:
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_execution_task_feedback(
    module_id:       int,
    module_title:    str,
    kpi_before:      Optional[str],
    kpi_after:       Optional[str],
    difficulty:      Optional[str],
    section_type:    str = "execution_task",
    lang:            str = "fr",
    tutorial_titles: list = []
) -> dict:
    """
    Génère un feedback post-soumission de l'Execution Task.

    Retourne :
    {
        "feedback"           : str,
        "progression_signal" : "improving" | "stagnant" | "needs_review",
        "suggestion"         : str | None,
        "next_step"          : str
    }
    """
    # ── Fallback si données manquantes ──────────────────────
    if not kpi_after:
        return {
            "feedback":            "Soumission enregistrée. Renseignez votre KPI after pour obtenir un feedback personnalisé.",
            "progression_signal":  "stagnant",
            "suggestion":          None,
            "next_step":           "Mesurez votre KPI after et mettez à jour votre soumission."
        }

    # ── Construction de la liste des tutoriels pour le prompt ──
    tutorials_str = (
        ", ".join(f'"{t}"' for t in tutorial_titles)
        if tutorial_titles
        else "aucun tutoriel disponible"
    )

    prompt = (
        f"Tu es le coach pédagogique de la plateforme Euklydia.\n\n"
        f"Module : {module_title}\n"
        f"KPI before (baseline) : {kpi_before or 'non renseigné'}\n"
        f"KPI after (mesuré)    : {kpi_after}\n"
        f"Difficulté déclarée   : {difficulty or 'aucune'}\n"
        f"Tutoriels disponibles : {tutorials_str}\n\n"
        f"En te basant sur ces données, génère UNIQUEMENT ce JSON :\n"
        "{\n"
        '  "feedback": "<feedback personnalisé 2-3 phrases — compare kpi_before et kpi_after, valorise la progression>",\n'
        '  "progression_signal": "<improving|stagnant|needs_review>",\n'
        f'  "suggestion": "<si needs_review ET tutoriels disponibles : cite EXACTEMENT le titre d\'un tutoriel parmi [{tutorials_str}] | si needs_review sans tutoriel : cite une section à revoir | null si improving>",\n'
        '  "next_step": "<une action concrète pour consolider ou améliorer>"\n'
        "}\n\n"
        "Règles :\n"
        "- improving    : KPI after montre une amélioration claire vs before\n"
        "- stagnant     : KPI after similaire au before, peu d'évolution\n"
        "- needs_review : difficulté élevée déclarée OU KPI after insuffisant\n"
        "- Si needs_review ET tutoriels disponibles : suggestion DOIT citer le titre exact d'un tutoriel\n"
        "- Si needs_review sans tutoriels : suggestion cite une section du module à revoir\n"
        "- Si improving : suggestion = null\n"
        "- Adapte le ton au contexte Maghreb — bienveillant et concret\n"
        "- Réponds en français"
    )

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        raw = (response.choices[0].message.content or "").strip()
        if raw.startswith("```"):
            raw = raw.strip("`").strip()
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()
        return json.loads(raw)

    except Exception:
        return {
            "feedback":           "Votre Execution Task a été soumise. Continuez à pratiquer !",
            "progression_signal": "stagnant",
            "suggestion":         "Revoir l'Execution Content avant de passer au module suivant.",
            "next_step":          "Comparez votre KPI before et after et identifiez l'écart."
        }


def generate_pacing_alert(
    modules_without_improvement: int,
    last_difficulty:             Optional[str],
    time_available_per_week:     Optional[int]
) -> Optional[str]:
    """
    Génère une alerte de pacing si l'apprenant enchaîne
    plusieurs modules sans amélioration des KPIs.

    Retourne : message d'alerte | None si pas d'alerte nécessaire
    """
    if modules_without_improvement < 2:
        return None

    prompt = (
        f"Un apprenant Euklydia a complété {modules_without_improvement} "
        f"modules consécutifs sans amélioration significative de ses KPIs.\n"
        f"Difficulté déclarée sur le dernier module : "
        f"{last_difficulty or 'non renseignée'}\n"
        f"Temps disponible par semaine : "
        f"{time_available_per_week or 'non renseigné'} heures\n\n"
        f"Génère un message d'alerte bienveillant (2 phrases max) qui :\n"
        f"1. Reconnaît l'effort de l'apprenant\n"
        f"2. Suggère de consolider avant de continuer\n"
        f"Réponds en français, ton bienveillant et concret."
    )

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    except Exception:
        return (
            "Vous avancez bien ! Avant de continuer, "
            "prenez le temps de consolider les modules précédents "
            "en mesurant vos KPIs réels."
        )