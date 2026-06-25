"""
Seed AI Project Manager — Euklydia Academy v1.0

Contenu pédagogique du diagnostic AI Project Manager :
- 3 skills selon la logique 1 skill = 1 module
- 9 questions QCM (3 par skill : Connaissance / Application / Maîtrise)

Source : PDF "Parcours AI Project Manager v1.0" — Avril 2026 (Ranim Souissi).

Career path : AI Project Manager (id=82).

Idempotent : skip si déjà seedé (pattern aligné sur seed_ai_sales_specialist_diagnostic.py).
"""
from app.models.skill import Skill
from app.models.question import Question


CAREER_PATH_ID = 82  # AI Project Manager


# =============================================================================
# Skills — 3 compétences cœur (logique 1 skill = 1 module)
# =============================================================================
SKILLS = [
    {
        "name": "AI Project Planning",
        "description": (
            "Capacité à utiliser l'IA pour générer rapidement des plans projet "
            "structurés (roadmap, dépendances, jalons) et à les maintenir à jour "
            "de façon semi-automatisée dans Notion, Asana ou ClickUp. Compétence "
            "couvrant 7 axes : structure d'un plan projet professionnel, brief "
            "structuré pour génération IA, utilisation de ChatGPT/Claude pour "
            "roadmap, maîtrise de Notion AI, maîtrise d'Asana ou ClickUp avec "
            "templates IA, bibliothèque de plans templates, et boucle de revue "
            "automatique."
        ),
    },
    {
        "name": "AI Risk Intelligence",
        "description": (
            "Capacité à anticiper les risques projet de manière proactive (au lieu "
            "de réagir une fois le problème survenu) à l'aide de l'IA : détection "
            "des signaux faibles, scoring de probabilité, playbooks de mitigation. "
            "Compétence couvrant 7 axes : framework de gestion des risques du PMI, "
            "session de risk discovery, risk register structuré (probabilité × "
            "impact × mitigation), détection des signaux faibles, playbooks de "
            "mitigation par type de risque, veille continue automatisée, et "
            "communication des risques aux stakeholders."
        ),
    },
    {
        "name": "AI Execution & Productivity",
        "description": (
            "Capacité à optimiser la productivité d'une équipe projet (planification "
            "de sprint, priorisation des tâches, équilibrage de la charge, suivi de "
            "performance) à l'aide de l'IA. Compétence couvrant 7 axes : matrice "
            "Eisenhower et framework RICE, sprint planning IA-augmenté, équilibrage "
            "de la charge, dashboard performance hebdomadaire, détection des "
            "signaux de burn-out, maîtrise de Jira AI ou ClickUp AI, et "
            "rétrospectives data-driven."
        ),
    },
]


# =============================================================================
# Questions — 9 QCM (3 par skill : Connaissance / Application / Maîtrise)
# Les questions sont indexées par position dans SKILLS (0=skill 1, 1=skill 2, 2=skill 3)
# Source : PDF Parcours AI Project Manager v1.0, pages 7-10.
# =============================================================================
QUESTIONS = [
    # =========================================================================
    # Skill 1 — AI Project Planning
    # =========================================================================
    {
        "skill_index": 0,  # AI Project Planning
        "order": 1,
        "text": (
            "Qu'est-ce qu'une roadmap projet dans un contexte de gestion de "
            "projet ?"
        ),
        "option_a": "La carte routière d'un déplacement professionnel",
        "option_b": (
            "Un document visuel qui décrit les phases, jalons, livrables et "
            "dépendances d'un projet sur une ligne de temps"
        ),
        "option_c": "Un tableau Excel listant les bugs",
        "option_d": "Un planning quotidien des tâches de l'équipe",
        "correct_answer": "B",
        "explanation": (
            "Une roadmap projet est un document visuel qui structure un projet "
            "sur une ligne de temps, en décrivant ses phases, ses jalons clés, "
            "ses livrables et les dépendances entre tâches. Ce n'est ni un "
            "déplacement, ni un simple registre de bugs, ni un planning quotidien "
            "(qui relèverait du sprint backlog ou du daily plan)."
        ),
    },
    {
        "skill_index": 0,
        "order": 2,
        "text": (
            "Tu démarres un nouveau projet de 6 mois avec 8 personnes. Quelle "
            "approche IA est la plus efficace pour générer rapidement un plan "
            "structuré ?"
        ),
        "option_a": "Demander à ChatGPT « fais-moi un planning » sans contexte",
        "option_b": (
            "Préparer un brief structuré (objectif, livrables, contraintes, "
            "équipe), appliquer un prompt de génération de roadmap et itérer en "
            "revue d'équipe"
        ),
        "option_c": "Reprendre tel quel le planning du dernier projet similaire",
        "option_d": (
            "Faire un plan détaillé tout seul sur Excel sans consulter l'équipe"
        ),
        "correct_answer": "B",
        "explanation": (
            "L'approche optimale combine 3 ingrédients : (1) un brief structuré "
            "qui cadre le contexte (objectif, livrables, contraintes, équipe), "
            "(2) un prompt de génération de roadmap appliqué à ce brief, (3) une "
            "revue d'équipe pour valider et ajuster. Le prompt vague ne donne pas "
            "de résultat exploitable, le copier-coller d'un ancien plan ignore "
            "les spécificités, et le travail solo manque l'intelligence "
            "collective."
        ),
    },
    {
        "skill_index": 0,
        "order": 3,
        "text": (
            "Tu veux industrialiser la création de plans projet pour livrer une "
            "roadmap initiale en moins de 1h au lieu de 2 jours. Quelle "
            "architecture choisir ?"
        ),
        "option_a": "Faire chaque planning à la main sur Excel, projet par projet",
        "option_b": "Utiliser uniquement le template natif d'Asana sans IA",
        "option_c": (
            "Bibliothèque de prompts par type de projet + GPT-4 (génération) + "
            "Notion AI / Asana (intégration) + workflow de validation humaine + "
            "revue d'équipe + mise à jour continue automatique"
        ),
        "option_d": "Demander à un consultant externe de tout faire",
        "correct_answer": "C",
        "explanation": (
            "Une architecture industrielle de planification combine 5 composants : "
            "(1) bibliothèque de prompts par type de projet, (2) IA générative "
            "(GPT-4) pour la génération initiale, (3) intégration native dans "
            "l'outil de gestion (Notion AI / Asana), (4) workflow de validation "
            "humaine, (5) mise à jour continue automatique. Excel manuel ne "
            "scale pas, le template natif sans IA reste lent, et l'externalisation "
            "perd le savoir-faire interne."
        ),
    },
    # =========================================================================
    # Skill 2 — AI Risk Intelligence
    # =========================================================================
    {
        "skill_index": 1,  # AI Risk Intelligence
        "order": 1,
        "text": (
            "Qu'est-ce qu'un registre des risques (risk register) en gestion de "
            "projet ?"
        ),
        "option_a": "La liste des employés ayant fait des erreurs",
        "option_b": (
            "Un document vivant qui inventorie les risques identifiés, leur "
            "probabilité, leur impact, et les actions de mitigation associées"
        ),
        "option_c": "Un fichier RH confidentiel",
        "option_d": "Un rapport financier annuel",
        "correct_answer": "B",
        "explanation": (
            "Un risk register est un document vivant — il évolue tout au long du "
            "projet — qui structure pour chaque risque identifié : sa description, "
            "sa probabilité, son impact, son score de criticité, l'owner désigné, "
            "et les actions de mitigation prévues. Ce n'est ni un document RH, ni "
            "un rapport financier, ni une liste de fautifs."
        ),
    },
    {
        "skill_index": 1,
        "order": 2,
        "text": (
            "Tu pilotes un projet stratégique. Comment l'IA peut-elle t'aider à "
            "anticiper les risques au lieu de les subir ?"
        ),
        "option_a": "Attendre que les problèmes apparaissent puis improviser",
        "option_b": (
            "Faire un atelier de risk discovery assisté par IA (analyse des "
            "projets similaires + signaux faibles dans les comptes-rendus + "
            "scoring probabilité×impact + playbooks de mitigation pré-rédigés)"
        ),
        "option_c": "Faire confiance à l'expérience seule, sans documenter",
        "option_d": (
            "Multiplier les réunions de status sans cadre méthodologique"
        ),
        "correct_answer": "B",
        "explanation": (
            "Une démarche proactive combine 4 ingrédients : (1) analyse IA des "
            "projets similaires pour identifier les patterns, (2) détection des "
            "signaux faibles dans les comptes-rendus existants, (3) scoring "
            "probabilité × impact pour prioriser, (4) playbooks de mitigation "
            "pré-rédigés activables immédiatement. L'improvisation, la confiance "
            "dans l'expérience non documentée, et la multiplication des réunions "
            "non cadrées génèrent du retard et de la frustration."
        ),
    },
    {
        "skill_index": 1,
        "order": 3,
        "text": (
            "Tu veux mettre en place un système de risk intelligence en continu "
            "qui détecte les signaux faibles et alerte avant qu'un risque "
            "devienne incident. Quelle stack utiliser ?"
        ),
        "option_a": "Faire un point risques uniquement en fin de projet",
        "option_b": "Demander à chaque membre d'envoyer un email hebdo libre",
        "option_c": (
            "Sync continue (Jira / Asana / Slack) + LLM pour analyse sémantique "
            "des comptes-rendus et tickets + scoring automatique + alertes Slack "
            "+ playbooks de mitigation contextuels + dashboard temps réel"
        ),
        "option_d": (
            "Acheter un logiciel cher sans former l'équipe à l'utiliser"
        ),
        "correct_answer": "C",
        "explanation": (
            "Un système de risk intelligence continu nécessite 6 composants : "
            "synchronisation continue des sources de communication (Jira/Asana/"
            "Slack), analyse sémantique par LLM des comptes-rendus et tickets, "
            "scoring automatique des risques détectés, alertes Slack pour "
            "notifier le PM, playbooks contextuels prêts à activer, et dashboard "
            "temps réel pour la vue d'ensemble. Un point en fin de projet est "
            "trop tardif, les emails libres ne sont pas exploitables, et un "
            "logiciel non adopté reste inutile."
        ),
    },
    # =========================================================================
    # Skill 3 — AI Execution & Productivity
    # =========================================================================
    {
        "skill_index": 2,  # AI Execution & Productivity
        "order": 1,
        "text": (
            "Qu'est-ce que la matrice Eisenhower dans la priorisation de tâches ?"
        ),
        "option_a": "Un type de planning de fabrication industrielle",
        "option_b": (
            "Une grille à 4 quadrants (urgent/important × non-urgent/non-important) "
            "qui aide à classer les tâches selon leur priorité réelle"
        ),
        "option_c": "Un format de réunion d'équipe",
        "option_d": "Une méthode de calcul de salaire",
        "correct_answer": "B",
        "explanation": (
            "La matrice Eisenhower est un outil classique de priorisation qui "
            "croise deux axes (urgence et importance) pour produire 4 quadrants : "
            "Q1 urgent+important (à faire), Q2 non-urgent+important (à planifier), "
            "Q3 urgent+non-important (à déléguer), Q4 non-urgent+non-important "
            "(à éliminer). Ce n'est ni un planning industriel, ni un format de "
            "réunion, ni une méthode de calcul de salaire."
        ),
    },
    {
        "skill_index": 2,
        "order": 2,
        "text": (
            "Ton équipe a 50 tickets en backlog et chaque sprint, vous en livrez "
            "10. Comment l'IA peut-elle aider à mieux prioriser ?"
        ),
        "option_a": "Prendre les 10 premiers tickets de la liste sans réfléchir",
        "option_b": (
            "Appliquer un prompt de priorisation Eisenhower + RICE (Reach, Impact, "
            "Confidence, Effort) sur le backlog complet, équilibrer la charge par "
            "membre et valider en sprint planning collectif"
        ),
        "option_c": "Laisser chaque membre choisir ses tickets favoris",
        "option_d": (
            "Faire passer en priorité les tickets demandés par le chef le plus fort"
        ),
        "correct_answer": "B",
        "explanation": (
            "L'approche optimale combine 3 dimensions : (1) priorisation IA "
            "couplant Eisenhower (urgence/importance) et RICE (Reach × Impact × "
            "Confidence / Effort) pour révéler la vraie valeur business, (2) "
            "équilibrage de la charge par membre pour éviter burn-out et "
            "sous-charge, (3) validation collective en sprint planning. La prise "
            "FIFO, le free-for-all et la priorisation politique mènent à de la "
            "sous-performance et de la démotivation."
        ),
    },
    {
        "skill_index": 2,
        "order": 3,
        "text": (
            "Tu veux déployer un système d'optimisation de la productivité "
            "d'équipe qui automatise la planification de sprint, équilibre les "
            "charges et alerte sur les dérives. Quelles capacités doit-il avoir ?"
        ),
        "option_a": "Uniquement un fichier Excel mis à jour à la main",
        "option_b": "Uniquement un Trello sans automatisation",
        "option_c": (
            "Connexion Jira / ClickUp + LLM pour priorisation Eisenhower+RICE + "
            "moteur d'équilibrage de charge par membre + dashboard performance + "
            "alertes burn-out / retards + suggestions de re-priorisation "
            "hebdomadaires"
        ),
        "option_d": (
            "Imposer 50 tâches par semaine à chaque membre, peu importe la charge"
        ),
        "correct_answer": "C",
        "explanation": (
            "Un système d'optimisation complet couvre 6 capacités : connexion "
            "native à l'outil de tickets (Jira/ClickUp), priorisation IA via "
            "Eisenhower+RICE, moteur d'équilibrage de charge personnalisé par "
            "membre, dashboard performance pour la vue d'ensemble, alertes "
            "automatiques sur burn-out et retards, et suggestions hebdomadaires "
            "de re-priorisation. Excel ou Trello seuls n'apportent aucune "
            "automatisation, et imposer une charge fixe ignore les compétences "
            "et capacités individuelles."
        ),
    },
]


def seed_ai_project_manager_diagnostic(db):
    """
    Seed les 3 skills + 9 questions du diagnostic AI Project Manager v1.

    Idempotent : skip si déjà seedé.
    """
    # =========================================================================
    # 0. Anti-doublon — skip si déjà seedé
    # =========================================================================
    existing_skills = (
        db.query(Skill)
        .filter(Skill.career_path_id == CAREER_PATH_ID)
        .count()
    )
    if existing_skills >= len(SKILLS):
        print(
            f"⚠️  AI Project Manager déjà seedé "
            f"({existing_skills} skills sur career_path {CAREER_PATH_ID}), skip."
        )
        return

    # =========================================================================
    # 1. Insérer les 3 skills
    # =========================================================================
    skill_objects = []
    for skill_data in SKILLS:
        # Vérifier si la skill existe déjà (au cas par cas, en plus du check global)
        existing_skill = (
            db.query(Skill)
            .filter(
                Skill.name == skill_data["name"],
                Skill.career_path_id == CAREER_PATH_ID,
            )
            .first()
        )
        if existing_skill:
            skill_objects.append(existing_skill)
            continue

        skill = Skill(
            name=skill_data["name"],
            description=skill_data["description"],
            career_path_id=CAREER_PATH_ID,
        )
        db.add(skill)
        skill_objects.append(skill)

    # Flush pour obtenir les IDs auto-générés des skills
    db.flush()

    # =========================================================================
    # 2. Insérer les 9 questions (3 par skill)
    # =========================================================================
    for question_data in QUESTIONS:
        skill = skill_objects[question_data["skill_index"]]

        # Vérifier si la question existe déjà (par texte + skill_id)
        existing_question = (
            db.query(Question)
            .filter(
                Question.text == question_data["text"],
                Question.skill_id == skill.id,
            )
            .first()
        )
        if existing_question:
            continue

        question = Question(
            text=question_data["text"],
            option_a=question_data["option_a"],
            option_b=question_data["option_b"],
            option_c=question_data["option_c"],
            option_d=question_data["option_d"],
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"],
            order=question_data["order"],
            skill_id=skill.id,
        )
        db.add(question)

    db.flush()

    print(
        f"✅ AI Project Manager seedé : "
        f"{len(SKILLS)} skills + {len(QUESTIONS)} questions "
        f"(career_path {CAREER_PATH_ID})"
    )