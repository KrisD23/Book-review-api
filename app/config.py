APP_NAME = "Book Review API"
API_VERSION = "v1"
DEBUG = True
DATABASE_URL = "postgresql://localhost:5432/books"

class Settings:
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "book_review"
    DB_USER = "krishan"
    DB_PASSWORD = "password123"

settings = Settings()

JWT_SECRET_KEY = "ilovedogs"
JWT_ALGORITHM = "HS256"