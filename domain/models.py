from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    message_count = Column(Integer, default=0)
    message_limit = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)

    logs = relationship("ConversationLog", back_populates="session", cascade="all, delete")


class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)

    session_id = Column(String, ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="logs")

    turn_index = Column(Integer)
    question = Column(String)
    answer = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)