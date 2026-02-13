from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(200), nullable=False)

class To_Do(Base):
    __tablename__ = "task_list"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    domain = Column(String(30), unique=False, nullable=True)

    domain_usr = Column(String(150), unique=False, nullable=True)
    domain_pass = Column(String(150), unique=False, nullable=True)