from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from base import Session, engine, Base
from message import Message as DbMessage
from db_setup_and_test import initialize_message_db

class Message(BaseModel):
    SenderId: int
    RecipientId: int
    SentDateTime: Optional[datetime.datetime] = None
    MessageText: str

app_description = """
Simple Message API facilitates basic communication between two parties.

## Messages

You can create and fetch **messages**.

You are be able to:

* **Create messages**.
* **Fetch messages sent from one user to another user**.
* **Fetch messages sent to a user**.
"""


app = FastAPI(
    title="Simple Message API",
    description=app_description,
    version="0.0.1",
    contact={
        "name": "Chris Cybulski",
        "email": "cacybulski@gmail.com"
    }
)
initialize_message_db()

@app.post(
    "/messages/create_message", 
    response_model=Message,
    description="Create message from sender to recipient.",
    tags=['messages']
)
def create_message(message: Message):
    session = Session()
    try:
        session.add(DbMessage(**message.dict()))
        session.commit()
        fetch_message = session.query(DbMessage).filter(DbMessage.RecipientId == message.RecipientId, DbMessage.SenderId == message.SenderId,\
            DbMessage.MessageText == message.MessageText).first()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    session.close()
    return {'SenderId': fetch_message.SenderId, 'RecipientId': fetch_message.RecipientId, 'MessageText': fetch_message.MessageText, \
        'SentDateTime': fetch_message.SentDateTime}

@app.get(
    "/messages/get_messages_from_sender", 
    response_model=List[Message],
    description="Get messages from sender to recipient limited to 100 messages sent in the last 30 days.",
    tags=['messages']
)
def get_messages_from_sender(recipient_id: int, sender_id: int):
    session = Session()
    db_messages = session.query(DbMessage).filter(DbMessage.RecipientId == recipient_id, DbMessage.SenderId == sender_id,\
        DbMessage.SentDateTime >= (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')).order_by(DbMessage.SentDateTime).limit(100)
    messages = [{'SenderId': message.SenderId, 'RecipientId': message.RecipientId, 'MessageText': message.MessageText, \
        'SentDateTime': message.SentDateTime} for message in db_messages]
    session.commit()
    session.close()
    return messages

@app.get(
    "/messages/get_messages_to_recipient", 
    response_model=List[Message],
    description="Get messages to recipient limited to 100 messages sent in the last 30 days.",
    tags=['messages']
)
def get_messages_to_recipient(recipient_id: int):
    session = Session()
    db_messages = session.query(DbMessage).filter(DbMessage.RecipientId == recipient_id, \
        DbMessage.SentDateTime >= (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')).order_by(DbMessage.SentDateTime).limit(100)
    messages = [{'SenderId': message.SenderId, 'RecipientId': message.RecipientId, 'MessageText': message.MessageText, \
        'SentDateTime': message.SentDateTime} for message in db_messages]
    session.commit()
    session.close()
    return messages
