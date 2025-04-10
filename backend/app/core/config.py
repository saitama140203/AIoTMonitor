from pydantic import computed_field, field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings  

from typing import List, Union
from pathlib import Path

class Settings(BaseSettings):
    #
    API_V1_STR: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = {
        "case_sensitive": True,
        "env_file": str(Path(__file__).resolve().parent.parent.parent/ ".env")
    }

settings = Settings()
