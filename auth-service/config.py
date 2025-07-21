import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") + "?connect_timeout=5"
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'connect_args': {
            'connect_timeout': 5,
            'options': '-c statement_timeout=15000'
        }
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False