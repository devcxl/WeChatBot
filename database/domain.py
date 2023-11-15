from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    wechat_id = Column(String, unique=True, index=True, nullable=False)
    user_name = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, unique=True, index=True, nullable=False)
    marked_name = Column(String, unique=True, index=True, nullable=False)
    head_img = Column(String, unique=True, index=True, nullable=False)
    bg_img = Column(String, unique=True, index=True, nullable=False)
    ticket = Column(String, unique=True, index=True, nullable=False)
    # 用户状态 0 未验证 1 已验证
    status = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())
    user_id = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)
