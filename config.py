import os

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://nome:password@localhost/Biblioteca"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)