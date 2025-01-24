# Configuration settings
import os


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")


settings = Settings()
