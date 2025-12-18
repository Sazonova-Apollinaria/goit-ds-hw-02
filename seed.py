import sqlite3
from faker import Faker
import random

fake = Faker()

conn = sqlite3.connect("tasks.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

statuses = ["new", "in progress", "completed"]

for s in statuses:
    cursor.execute(
        "INSERT OR IGNORE INTO status (name) VALUES (?)",
        (s,)
    )

for _ in range(10):
    cursor.execute(
        "INSERT INTO users (fullname, email) VALUES (?, ?)",
        (fake.name(), fake.unique.email())
    )

cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

for _ in range(30):
    cursor.execute("""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (?, ?, ?, ?)
    """, (
        fake.sentence(),
        fake.text() if random.choice([True, False]) else None,
        random.choice(status_ids),
        random.choice(user_ids)
    ))

conn.commit()
conn.close()

print("Данні добавлені")