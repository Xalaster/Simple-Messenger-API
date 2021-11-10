# coding=utf-8

from base import Session, engine, Base
from user import User
from message import Message
from faker import Faker
import random
import datetime

def initialize_message_db():
    """Create messenger_db with designed tables and relationships."""
    Base.metadata.create_all(engine)

def add_random_users(number_of_users=500):
    """Add requested number of fake users for the purposes of testing."""
    # Create session connection to database.
    session = Session()
    # Instantiate Faker.
    fake = Faker()
    # Create a fake name to insert the requested number of users.
    for _ in range(number_of_users):
        session.add(User(FullName=fake.name()))
    # Commit and close session.
    session.commit()
    session.close()

def generate_random_datetime():
    """Pick a random datetime within the last 60 days for the purposes of testing."""
    # Date Range from now to 60 days ago.
    end_datetime = datetime.datetime.utcnow()
    start_datetime = end_datetime - datetime.timedelta(days=60)
  
    # Initialize a list of options from which to choose.
    datetime_options = [start_datetime]
  
    # Loop through adding 20 minutes through entire range.
    loop_datetime = start_datetime
    while loop_datetime < end_datetime:
        loop_datetime += datetime.timedelta(minutes=20)
        datetime_options.append(loop_datetime)
    return random.choice(datetime_options)

def get_all_user_ids():
    # Create session connection to database.
    session = Session()
    # Fetch all Users from Users table so Ids can be used in generating messages.
    all_users = session.query(User).all()
    all_user_ids = [user.Id for user in all_users]
    session.close()
    return all_user_ids

def add_random_messages(number_of_messages=1500):
    """Add requested number of fake messages for the purposes of testing."""
    # Create session connection to database.
    session = Session()
    # Fetch all Users from Users table so Ids can be used in generating messages.
    all_user_ids = get_all_user_ids()
    # Instantiate Faker.
    fake = Faker()
    # Create a fake message to insert the requested number of messages.
    for _ in range(number_of_messages):
        sender_id, recipient_id = random.choices(all_user_ids, k=2)
        session.add(Message(SenderId=sender_id, RecipientId=recipient_id, MessageText=fake.text(), SentDateTime=generate_random_datetime()))
    # Commit and close session.
    session.commit()
    session.close()

if __name__ == "__main__":
    print("Initializing message_db database.")
    initialize_message_db()
    print("Creating 500 random users for testing purposes.")
    add_random_users(500)
    print("Creating 1500 random messages between users for testing purposes.")
    add_random_messages(1500)

