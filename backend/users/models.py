from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)


# --- MEETINGS ---
class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    summary = Column(Text)
    transcript = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
