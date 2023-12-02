from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILES = ("dev.env",)

class RMQSettings(BaseSettings):
    """ base rmq settings """
    USER: str
    PASS: str
    HOST: str
    PORT: int
    DEFAULT_QUEUE: str
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=ENV_FILES,
        env_prefix="RABBITMQ_"
    )

rmq_config = RMQSettings()
