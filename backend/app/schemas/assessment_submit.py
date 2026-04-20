from pydantic import BaseModel, field_validator


class AnswerIn(BaseModel):
    question_id: int
    selected_option: str  # "A", "B", "C" ou "D"

    @field_validator("selected_option")
    @classmethod
    def validate_option(cls, v: str) -> str:
        v = v.upper().strip()
        if v not in {"A", "B", "C", "D"}:
            raise ValueError("selected_option must be A, B, C or D")
        return v


class SubmitAnswersIn(BaseModel):
    answers: list[AnswerIn]