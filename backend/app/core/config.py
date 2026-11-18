from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    database_url: str = "sqlite:///./resume_coach.db"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    frontend_origin: str = "http://localhost:5173"
    max_upload_mb: int = 8
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
settings = Settings()
