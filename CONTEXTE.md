# Euklydia Academy — Contexte projet
## Stack
- Backend : FastAPI + PostgreSQL + SQLAlchemy + Alembic
- Frontend : React + Tailwind CSS
- Auth : JWT + Google OAuth
## Structure backend
- app/api/v1/endpoints/ → auth.py, diagnostic.py, modules.py
- app/services/ → learning_path_service.py, assessment_rules.py
- app/models/ → User, Module, Skill, Question, UserModuleProgress...
- app/schemas/ → learning_path.py, auth.py, diagnostic_*.py
- app/core/ → config.py, security.py, limiter.py
## Structure frontend
- src/pages/ → CommandCenterPage, AIRoadmapPage, LearningPage,
               ModuleDetailPage, DiagnosticPage, OnboardingPage...
- src/utils/api.js → apiFetch (gestion 401 auto)
- src/hooks/useApi.js → hook chargement données
- src/components/ → Toast, ConfirmModal, ...
## État MVP
- 6 modules generiques "All roles"
- 30 questions diagnostic (6 skills x 5 questions)
- Scoring HIGH/MEDIUM/LOW
- Progression complète validée (0% → 100%)
- Bilingue EN/FR
## Prochaine étape