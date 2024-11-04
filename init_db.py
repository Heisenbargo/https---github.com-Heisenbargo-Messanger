import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')  # Подключение к базе данных
    c = conn.cursor()
    # Создание таблицы users, если её нет
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Таблица users успешно создана.")

# Запуск функции инициализации
if __name__ == '__main__':
    init_db()
