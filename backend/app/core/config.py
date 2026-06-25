from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Core ---
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- OpenAI ---
    OPENAI_API_KEY: str | None = None
    USE_LLM_REPORT: bool = False
    OPENAI_MODEL_REPORT: str = "gpt-4.1"

    # --- Gemini ---
    GEMINI_API_KEY: str | None = None

    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # --- Frontend ---
    FRONTEND_URL: str

    # --- diagnostic ---
    diagnostic_COOLDOWN_DAYS: int = 0

    # --- Email ---
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()