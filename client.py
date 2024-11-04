import requests

SERVER_URL = "http://127.0.0.1:5000"

def register_user(username, password):
    response = requests.post(f"{SERVER_URL}/register", json={'username': username, 'password': password})
    if response.status_code == 201:
        print("Registration successful")
    else:
        print("Error:", response.json())

def login_user(username, password):
    response = requests.post(f"{SERVER_URL}/login", json={'username': username, 'password': password})
    if response.status_code == 200:
        print("Login successful")
        return True
    else:
        print("Login failed:", response.json())
        return False

def send_message(sender_id, receiver_id, content):
    response = requests.post(f"{SERVER_URL}/messages/send", json={'sender_id': sender_id, 'receiver_id': receiver_id, 'content': content})
    if response.status_code == 200:
        print("Message sent")
    else:
        print("Error:", response.json())

def get_messages(sender_id, receiver_id):
    response = requests.get(f"{SERVER_URL}/messages", params={'sender_id': sender_id, 'receiver_id': receiver_id})
    if response.status_code == 200:
        messages = response.json()
        for msg in messages:
            print(f"{msg['timestamp']} - {msg['sender_id']} -> {msg['receiver_id']}: {msg['content']}")
    else:
        print("Error fetching messages:", response.json())
