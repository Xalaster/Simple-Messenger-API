# coding=utf-8

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from base import Base
import datetime

class Message(Base):
    __tablename__ = 'Messages'

    Id = Column(Integer, primary_key=True)
    SenderId = Column(Integer, ForeignKey('Users.Id'))
    RecipientId = Column(Integer, ForeignKey('Users.Id'))
    SentDateTime = Column(DateTime)
    MessageText = Column(String)

    def __init__(self, SenderId, RecipientId, MessageText, SentDateTime=datetime.datetime.utcnow()):
        self.SenderId = SenderId
        self.RecipientId = RecipientId
        if SentDateTime is None:
            self.SentDateTime = datetime.datetime.utcnow()
        else:
            self.SentDateTime = SentDateTime
        self.MessageText = MessageText
