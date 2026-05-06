import os

class Settings:
    APP_NAME = os.getenv("APP_NAME", "NutriLog")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "nutrition")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    RELEASE_VERSION = os.getenv("RELEASE_VERSION", "local")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

settings = Settings()