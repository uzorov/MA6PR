from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@localhost:5672"
    # postgres_url: str = "postgresql://:uzorov@maprac6-postgres-1:5432/test"
    postgres_url: str = "postgresql://postgres:uzorov@localhost:5432/test"


settings = Settings()
