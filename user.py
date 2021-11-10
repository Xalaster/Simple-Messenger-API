# coding=utf-8

from sqlalchemy import Column, String, Integer, Date
from base import Base

class User(Base):
    __tablename__ = 'Users'

    Id = Column(Integer, primary_key=True)
    FullName = Column(String)

    def __init__(self, FullName):
        self.FullName = FullName
