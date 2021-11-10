# coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event


engine = create_engine('sqlite:///messenger_db.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Included event listener to "activate" Foreign Keys for SQLite3. (This is recommended in SQLAlchemy docs.)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()