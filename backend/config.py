from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
