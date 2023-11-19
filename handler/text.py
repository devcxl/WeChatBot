from sqlalchemy.orm import Session

from database import SessionLocal
from database.domain import Message


def handler_text(msg_id:str,content: str):
    db: Session = SessionLocal
    message: Message = db.query(Message).filter(Message.id == msg_id).first()
    if message:
        return
    else:
        pass
