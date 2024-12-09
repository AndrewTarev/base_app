import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# abs_path_env = os.path.abspath("../../.env")
# env_template = os.path.abspath("../../.env.template")
load_dotenv()


class BaseServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class ApiV1Prefix(BaseModel):
    tweets: str = "/api/tweets"
    users: str = "/api/users"
    medias: str = "/api/medias"


class DatabaseConfig(BaseServiceSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    # авто наминг для ключей БД алембик
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"


class Settings(BaseModel):
    api: ApiV1Prefix = ApiV1Prefix()
    db: DatabaseConfig = DatabaseConfig()
    logging: str = "DEBUG"


settings = Settings()

if __name__ == "__main__":
    print(settings.rabbit_config.url)
