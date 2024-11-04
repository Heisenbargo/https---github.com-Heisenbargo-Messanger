from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import Session
from model import Base, Users, Message, get_db, find_user_in_database
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Настройка базы данных
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Создание таблиц

# Роут для начальной страницы с кнопками Login и Register
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

        # Использование сессии для добавления нового пользователя
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

        # Поиск пользователя по имени
        db = next(get_db())
        user = find_user_in_database(db, username)
        if user and user.password == password:
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))

    return render_template('login.html')

# Роут для панели пользователя (пример)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
