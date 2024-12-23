import sqlite3
from codecs import xmlcharrefreplace_errors

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


connection.commit()
connection.close()

# Налаштування бази даних
def setup_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Створення таблиці користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        chat_id INTEGER NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Створення таблиці бронювань
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date_start TEXT NOT NULL,
        date_end TEXT NOT NULL,
        guests INTEGER NOT NULL,
        room_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    connection.commit()
    connection.close()
    print("База даних успішно налаштована.")

setup_database()

def add_user(username, chat_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO users (username, chat_id)
        VALUES (?, ?)
        """, (username, chat_id))
        connection.commit()
        print(f"Користувач {username} успішно доданий.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні користувача: {e}")
    finally:
        connection.close()

def add_booking(chat_id, date_start, date_end, guest, room_type):
    connection = sqlite3.connect("datebase.db")
    cursor = connection.cursor()
    try:
        # Отримання user_id за chat_id
        cursor.execute("SELECT is FROM users WHERE chat-id = ?", (chat_id))
        user_id = cursor.fetchone()
        if user_id:
            user_id = user_id[0]
            cursor.execute("""INSERT INTO booking (user_id, date_start, data_end, guests, room_type)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, date_start, date_end, guests, room_type))
            connection.commit()
            print("Користувача не зенайденно в базі.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні бронювання: {e}")
    finally:
        connection.close()