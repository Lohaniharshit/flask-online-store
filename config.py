import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '466df0ab2c7d8ae4c6697f5926c1f5ca36a598600aad865d'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/shopping_app12345'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
