from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from app.db import Base
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(120),nullable=False)
    email=Column(String(255),unique=True,index=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    resumes=relationship("Resume",back_populates="owner",cascade="all, delete-orphan")
class Resume(Base):
    __tablename__="resumes"
    id=Column(Integer,primary_key=True,index=True)
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,index=True)
    filename=Column(String(255),nullable=False)
    content_type=Column(String(120),nullable=False)
    extracted_text=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    owner=relationship("User",back_populates="resumes")
    analyses=relationship("Analysis",back_populates="resume",cascade="all, delete-orphan")
class Analysis(Base):
    __tablename__="analyses"
    id=Column(Integer,primary_key=True,index=True)
    resume_id=Column(Integer,ForeignKey("resumes.id",ondelete="CASCADE"),nullable=False,index=True)
    ats_score=Column(Float,nullable=False)
    readability_score=Column(Float,nullable=False)
    result_json=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    resume=relationship("Resume",back_populates="analyses")
