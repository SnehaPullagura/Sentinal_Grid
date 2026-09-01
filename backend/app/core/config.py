from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel Grid Backend Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "sentinel_grid_production_super_secret_jwt_key_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    DATABASE_URL: str = "sqlite:///./sentinel_grid.db"

    class Config:
        case_sensitive = True

settings = Settings()
