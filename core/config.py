# # to store the project settings

from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:

    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", 3306)
    MYSQL_DB: str = os.getenv("MYSQL_DB", "crypto")
    URL_DATABASE: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
   

    # JWT 
    JWT_SECRET: str = os.getenv("JWT_SECRET", "fallback_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXP: timedelta = timedelta(days=float(os.getenv("JWT_ACCESS_TOKEN_EXP_DAYS", "7")))
    JWT_REFRESH_EXP: timedelta = timedelta(days=float(os.getenv("JWT_REFRESH_TOKEN_EXP_DAYS", "7")))

settings = Settings()
