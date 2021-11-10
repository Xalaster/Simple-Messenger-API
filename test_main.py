from fastapi.testclient import TestClient
from db_setup_and_test import get_all_user_ids
from main import app
import random

client = TestClient(app)

def test_create_message():
    all_user_ids = get_all_user_ids()
    sender_id, recipient_id = random.choices(all_user_ids, k=2)
    response = client.post(
        "/messages/create_message",
        json={"SenderId": sender_id, "RecipientId": recipient_id, "MessageText": "Hey! This is a test text message."},
    )
    assert response.status_code == 200
    assert response.json()['SenderId'] == sender_id
    assert response.json()['RecipientId'] == recipient_id
    assert response.json()['MessageText'] == "Hey! This is a test text message."

def test_create_message_bad_sender_id():
    all_user_ids = get_all_user_ids()
    good_recipient_id = random.choice(all_user_ids)
    bad_sender_id = max(all_user_ids) + 1
    response = client.post(
        "/messages/create_message",
        json={"SenderId": bad_sender_id, "RecipientId": good_recipient_id, "MessageText": "Hey! This is a test text message."},
    )
    assert response.status_code == 404

def test_create_message_bad_recipient_id():
    all_user_ids = get_all_user_ids()
    good_sender_id = random.choice(all_user_ids)
    bad_recipient_id = max(all_user_ids) + 1
    response = client.post(
        "/messages/create_message",
        json={"SenderId": good_sender_id, "RecipientId": bad_recipient_id, "MessageText": "Hey! This is a test text message."},
    )
    assert response.status_code == 404

def test_get_messages_from_sender():
    all_user_ids = get_all_user_ids()
    sender_id, recipient_id = random.choices(all_user_ids, k=2)
    response = client.get("/messages/get_messages_from_sender", params={'recipient_id': recipient_id, 'sender_id': sender_id})
    assert response.status_code == 200
    assert type(response.json()) == list

def test_get_messages_to_recipient():
    all_user_ids = get_all_user_ids()
    recipient_id = random.choice(all_user_ids)
    response = client.get("/messages/get_messages_to_recipient", params={'recipient_id': recipient_id})
    assert response.status_code == 200
    assert type(response.json()) == list
