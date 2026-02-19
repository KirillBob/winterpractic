import os


class Settings:
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:kirill@localhost:5432/WinterPractic')
    STORAGE_PATH = os.getenv('STORAGE_PATH', os.path.join(os.getcwd(), 'storage'))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'


settings = Settings()
