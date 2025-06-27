# chatbot/tenants/models.py

from sqlalchemy import Column, String, Boolean
from core.config import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    whatsapp_number = Column(String, unique=True, nullable=False)
    openai_key = Column(String, nullable=False)
    whatsapp_token = Column(String, nullable=False)  # ACCESS_TOKEN da Meta
    phone_number_id = Column(String, nullable=False)  # ID do número na Meta
    context_path = Column(String, nullable=False)
    ia_enabled = Column(Boolean, default=True)
