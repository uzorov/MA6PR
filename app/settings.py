from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest@localhost:5672/"
    # postgres_url: str = "postgresql://:uzorov@maprac6-postgres-1:5432/test"
    postgres_url: str = "postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/postgres"
    port: str = "80"
    # model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
