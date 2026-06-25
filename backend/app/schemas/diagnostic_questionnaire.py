from pydantic import BaseModel


class QuestionOut(BaseModel):
    id: int
    text: str
    order: int
    option_a: str
    option_b: str
    option_c: str
    option_d: str


class SkillWithQuestionsOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    questions: list[QuestionOut]


class QuestionnaireOut(BaseModel):
    career_path_id: int
    skills: list[SkillWithQuestionsOut]