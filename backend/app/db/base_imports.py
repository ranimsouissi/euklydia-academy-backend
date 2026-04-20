# This file exists only to import all models so Alembic can discover them.

from app.models.user import User
from app.models.career_path import CareerPath
from app.models.role import Role
from app.models.skill import Skill
from app.models.question import Question
from app.models.user_response import UserResponse
from app.models.user_skill_score import UserSkillScore
from app.models.user_profile import UserProfile
from app.models.oauth_account import OAuthAccount
from app.models.report import Report
from app.models.assessment_session import AssessmentSession
from app.models.password_reset_token import PasswordResetToken
from app.models.user_module_progress import UserModuleProgress
from app.models.oauth_state import OAuthState