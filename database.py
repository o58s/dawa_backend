from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password_@localhost:5432/database_name"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
