from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Define db only once

class User(UserMixin, db.Model):  # Add UserMixin for Flask-Login
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email field
    password = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
