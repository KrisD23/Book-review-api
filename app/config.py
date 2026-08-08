from dotenv import load_dotenv
import os

load_dotenv()


APP_NAME = "Book Review API"
API_VERSION = "v1"
DEBUG = True


class Settings:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "book_review")
    DB_USER = os.getenv("DB_USER", "krishan")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


settings = Settings()