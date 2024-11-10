from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from sqlalchemy.orm import Session
from model import Base, Users, Message, get_db, find_user_in_database
from sqlalchemy import create_engine
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройка базы данных
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Создание таблиц

# Роут для начальной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Роут для регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('register'))

        db = next(get_db())
        if find_user_in_database(db, username):
            flash('Username already exists.')
            return redirect(url_for('register'))

        new_user = Users(username=username, password=password)
        db.add(new_user)
        db.commit()
        flash('Registration successful!')
        return redirect(url_for('index'))
    
    return render_template('register.html')

# Роут для логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required.')
            return redirect(url_for('login'))

        db = next(get_db())
        user = find_user_in_database(db, username)
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

# Роут для панели пользователя
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Роут для страницы чата
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

# Роут для отправки сообщения
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    content = data.get('content')
    receiver_id = data.get('receiver_id')
    
    db = next(get_db())
    message = Message(
        sender_id=session['user_id'],
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.add(message)
    db.commit()
    return jsonify({'status': 'success', 'message': 'Message sent successfully'})

# Роут для получения сообщений
@app.route('/get_messages')
def get_messages():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    db = next(get_db())
    sender_id = session['user_id']
    receiver_id = request.args.get('receiver_id')

    messages = db.query(Message).filter(
        ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
        ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
    ).order_by(Message.timestamp).all()
    
    messages_data = [
        {'sender': msg.sender.username, 'content': msg.content, 'timestamp': msg.timestamp}
        for msg in messages
    ]
    return jsonify(messages_data)

# Роут для получения списка пользователей
@app.route('/get_users')
def get_users():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    db = next(get_db())
    users = db.query(Users).filter(Users.id != session['user_id']).all()
    users_data = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users_data)


if __name__ == '__main__':
    app.run(debug=True)
