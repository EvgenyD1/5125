import os

POSTGRES_DB = os.getenv("POSTGRES_DB", "ваше название db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5428")
POSTGRES_USER = os.getenv("POSTGRES_USER", "ваш user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ваш пароль")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
