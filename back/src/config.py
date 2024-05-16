from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class DataBaseSettings(BaseSettings):
    DB_USER: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"


class AuthSettings(BaseException):
    public_key: Path = Path(BASE_DIR / "cert" / "jwt-public.pem")
    private_key: Path = Path(BASE_DIR / "cert" / "jwt-private.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60


class Settings(BaseSettings):
    db: DataBaseSettings = DataBaseSettings()
    auth: AuthSettings = AuthSettings()


settings = Settings()
