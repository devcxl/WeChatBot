from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    wechat_id = Column(String(64), unique=True, index=True, nullable=False)
    user_name = Column(String(32), unique=True, index=True, nullable=False)
    nick_name = Column(String(32), unique=True, index=True, nullable=False)
    marked_name = Column(String(32), unique=True, index=True, nullable=False)
    head_img = Column(String(320), unique=True, index=True, nullable=False)
    bg_img = Column(String(320), unique=True, index=True, nullable=False)
    ticket = Column(String(100), unique=True, index=True, nullable=False)
    # 用户状态 0 未验证 1 已验证
    status = Column(Integer, nullable=False, default=0)
    default_prompt = Column(String(500), default="你是一个强大的人工智能，能良好的完成给你的任何需求。", nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(15), default='text')  # image voice video
    content = Column(String(500), nullable=False)  # text: message_content other: file_path
    timestamp = Column(DateTime, default=func.now())
    user_id = Column(Integer, nullable=False)
    replay = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(bind=engine)
