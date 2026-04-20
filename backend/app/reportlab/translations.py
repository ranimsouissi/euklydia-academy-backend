# backend/app/reportlab/translations.py
from __future__ import annotations
from typing import Dict

_TRANSLATIONS: Dict[str, Dict[str, str]] = {

    "en": {
        # Header
        "academy_name":     "EUKLYDIA ACADEMY",
        "report_title":     "Executive AI Maturity Report",

        # Page 1
        "leader":                  "Leader",
        "role_label":              "Role",
        "global_score":            "Global Score",
        "high_priority_gaps":      "High Priority Gaps",
        "strengths":               "Strengths",
        "executive_summary":       "Executive Summary",
        "strategic_risk_overview": "Strategic Risk Overview",

        # Page 2
        "capability_insights":     "Capability Insights",
        "capability_insights_sub": "Targeted insights on the highest-priority capability gaps.",
        "no_insights":             "No insights available",
        "no_insights_sub":         "LLM narrative is disabled or returned no capability insights.",
        "why_it_matters":          "Why it matters",
        "risk":                    "Risk",
        "business_leverage":       "Business leverage",
        "quick_win":               "Quick win (max. 2 weeks)",

        # Page 3
        "ai_maturity_breakdown":     "AI Maturity Breakdown",
        "ai_maturity_breakdown_sub": "Capabilities ranked by gap priority (higher = bigger capability gap).",
        "capability_maturity_top4":  "Capability Maturity (Top 4)",
        "col_capability":            "Capability",
        "col_score":                 "Score",
        "col_gap_priority":          "Gap Priority",
        "col_business_risk":         "Business risk",

        # Page 4
        "roadmap_title":   "90-Day Recommended Roadmap",
        "roadmap_sub":     "Phased plan to close gaps and operationalize measurement.",
        "phase_labels":    ["0-30 days", "30-60 days", "60-90 days"],
        "objective":       "Objective",
        "key_actions":     "Key actions",
        "success_metrics": "Success metrics",
        "expected_impact": "Expected impact",

        # Page 5
        "page5_title":    "Assessment Validity & Next Steps",
        "page5_sub":      "Your report is valid for 90 days. Plan your next development cycle.",
        "validity_label": "Valid for",
        "validity_value": "90 days",
        "next_assessment": "Next assessment:",
        "note_title":     "Report Validity & Next Steps",
        "note_body": (
            "This report reflects your AI capability maturity at the time of the assessment. "
            "The recommended 90-day roadmap is designed to close your priority skill gaps "
            "and build sustainable AI adoption across your role.\n\n"
            "This report is valid for 90 days. After this period, your skills and context "
            "will have evolved - a new assessment is strongly recommended to measure progress, "
            "update priorities, and generate a fresh roadmap aligned with your next development cycle."
        ),
        "cta_label": "Next step: retake the assessment after your 90-day cycle.",

        # Footer
        "page": "Page",
    },

    "fr": {
        # Header
        "academy_name":     "EUKLYDIA ACADEMY",
        "report_title":     "Rapport Executif de Maturite IA",

        # Page 1
        "leader":                  "Leader",
        "role_label":              "Role",
        "global_score":            "Score Global",
        "high_priority_gaps":      "Ecarts Prioritaires",
        "strengths":               "Points Forts",
        "executive_summary":       "Synthese Executive",
        "strategic_risk_overview": "Apercu des Risques Strategiques",

        # Page 2
        "capability_insights":     "Analyse des Capacites",
        "capability_insights_sub": "Insights cibles sur les ecarts de competences les plus prioritaires.",
        "no_insights":             "Aucun insight disponible",
        "no_insights_sub":         "La narrative LLM est desactivee ou n'a retourne aucun insight.",
        "why_it_matters":          "Pourquoi c'est important",
        "risk":                    "Risque",
        "business_leverage":       "Levier metier",
        "quick_win":               "Action rapide (max. 2 semaines)",

        # Page 3
        "ai_maturity_breakdown":     "Analyse de Maturite IA",
        "ai_maturity_breakdown_sub": "Capacites classees par priorite d'ecart (plus = ecart plus important).",
        "capability_maturity_top4":  "Maturite des Capacites (Top 4)",
        "col_capability":            "Capacite",
        "col_score":                 "Score",
        "col_gap_priority":          "Priorite",
        "col_business_risk":         "Risque metier",

        # Page 4
        "roadmap_title":   "Feuille de Route sur 90 Jours",
        "roadmap_sub":     "Plan phase pour combler les ecarts et operationnaliser la mesure.",
        "phase_labels":    ["0-30 jours", "30-60 jours", "60-90 jours"],
        "objective":       "Objectif",
        "key_actions":     "Actions cles",
        "success_metrics": "Indicateurs de succes",
        "expected_impact": "Impact attendu",

        # Page 5
        "page5_title":    "Validite et Prochaines Etapes",
        "page5_sub":      "Votre rapport est valable 90 jours. Planifiez votre prochain cycle.",
        "validity_label": "Valable",
        "validity_value": "90 jours",
        "next_assessment": "Prochain assessment :",
        "note_title":     "Validite du Rapport et Prochaines Etapes",
        "note_body": (
            "Ce rapport reflete votre niveau de maturite IA au moment de l'assessment. "
            "La feuille de route sur 90 jours est concue pour combler vos ecarts de "
            "competences prioritaires et ancrer l'IA dans votre quotidien professionnel.\n\n"
            "Ce rapport est valable 90 jours. A l'issue de cette periode, vos competences "
            "et votre contexte auront evolue. Un nouvel assessment est vivement recommande "
            "pour mesurer vos progres, actualiser vos priorites et generer une nouvelle "
            "feuille de route adaptee a votre prochain cycle de developpement."
        ),
        "cta_label": "Prochaine etape : refaire l'assessment apres votre cycle de 90 jours.",

        # Footer
        "page": "Page",
    },
}


def get_t(language: str = "en") -> Dict[str, str]:
    lang = str(language or "en").lower().strip()
    return _TRANSLATIONS.get(lang, _TRANSLATIONS["en"])