from pydantic import BaseModel
from ..config.email import get_settings
 
settings = get_settings()

class EmailConfig(BaseModel):
    SMTP_SERVER: str = settings.SMTP_SERVER
    SMTP_PORT: int = settings.SMTP_PORT
    SMTP_USERNAME: str = settings.SMTP_USERNAME
    SMTP_PASSWORD: str = settings.SMTP_PASSWORD