# chatbot/core/dependencies.py

from sqlalchemy.orm import Session
from core.config import SessionLocal

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
