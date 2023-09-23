import enum

from pydantic_settings import BaseSettings


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    application_name: str = "Kirgu employee"
    host: str = "0.0.0.0"
    port: int = 8000
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # DB config
    db_address: str = "./kirgu_employee.db"

    # Auth config
    secret_key: str = "secret"
    access_token_expire_minutes: int = 50
    auth_url: str = "login"

    # Current environment
    environment: str = "dev"

    log_level: LogLevel = LogLevel.INFO

    class Config:
        env_file = ".env"
        env_prefix = "KIRGU_EMPLOYEE_"
        env_file_encoding = "utf-8"


settings = Settings()
