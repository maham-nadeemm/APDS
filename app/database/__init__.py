"""
Database initialization module
"""
from flask import Flask
from app.database.db_connection import DatabaseConnection

def init_db(app: Flask):
    """Initialize database connection"""
    db = DatabaseConnection()
    db.init_app(app)
    return db




