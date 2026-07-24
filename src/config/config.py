import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.environ["DATABASE_URL"]
    N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "")


config = Config()
