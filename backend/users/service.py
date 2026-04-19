import sqlite3
from uuid import uuid4


DB_PATH = "db.sqlite3"  # поправь если у тебя другой путь


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def create_user(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (user_id)
        VALUES (?)
    """,
        (user_id,),
    )

    conn.commit()
    conn.close()


def get_user(user_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id FROM users WHERE user_id = ?
    """,
        (user_id,),
    )

    user = cursor.fetchone()
    conn.close()

    return user


def get_or_create_user(user_id: str):
    user = get_user(user_id)

    if not user:
        create_user(user_id)

    return user_id
