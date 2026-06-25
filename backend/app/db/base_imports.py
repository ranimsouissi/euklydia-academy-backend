# This file exists only to import all models so Alembic can discover them.
from app.models.user import User
from app.models.career_path import CareerPath
from app.models.role import Role
from app.models.skill import Skill
from app.models.question import Question
from app.models.user_skill_score import UserSkillScore
from app.models.user_profile import UserProfile
from app.models.oauth_account import OAuthAccount
from app.models.diagnostic_session import DiagnosticSession
from app.models.password_reset_token import PasswordResetToken
from app.models.user_module_progress import UserModuleProgress
from app.models.oauth_state import OAuthState
from app.models.module import Module
from app.models.module_skill import ModuleSkill

# Adaptive Learning Engine
from app.models.unit import Unit
from app.models.lesson import Lesson
from app.models.activity import Activity
from app.models.learner_activity_log import LearnerActivityLog
from app.models.learner_skill_mastery import LearnerSkillMastery
from app.models.learner_path_log import LearnerPathLog
from app.models.user_response import UserResponse