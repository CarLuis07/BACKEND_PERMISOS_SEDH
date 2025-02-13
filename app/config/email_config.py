from pydantic_settings import BaseSettings

class EmailSettings(BaseSettings):
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SENDER_EMAIL: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Permite campos extras en el archivo .env