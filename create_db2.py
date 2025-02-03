import sqlite3
import time
from datetime import datetime, timedelta


# Connexion à la base de données SQLite
connection = sqlite3.connect('bibliotheque.db')
cur = connection.cursor()

# Lecture et exécution du schéma SQL
with open('schema2.sql') as f:
    connection.executescript(f.read())


# Convertir les dates en timestamps UNIX
loans = [
    (1, 2, time.mktime(datetime.strptime('2024-01-15', '%Y-%m-%d').timetuple()), 
     time.mktime(datetime.strptime('2024-01-30', '%Y-%m-%d').timetuple()), 'active'),
    (2, 1, time.mktime(datetime.strptime('2024-02-01', '%Y-%m-%d').timetuple()), 
     time.mktime(datetime.strptime('2024-02-15', '%Y-%m-%d').timetuple()), 'active'),
]
cur.executemany("INSERT INTO loans (book_id, user_id, loan_date, due_date, status) VALUES (?, ?, ?, ?, ?)", loans)

# Insertion des utilisateurs
users = [
    ('Alice', 'Durand', 'alice.durand@example.com', 'password123', 'user'),
    ('Bob', 'Martin', 'bob.martin@example.com', 'password123', 'user'),
    ('Charlie', 'Dupont', 'charlie.dupont@example.com', 'password123', 'user'),
    ('Admin', 'Smith', 'admin@example.com', 'adminpass', 'admin')
]
cur.executemany("INSERT INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?)", users)

# Insertion des livres
books = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', '1943-04-06', 'Fiction', 5, 5),
    ('1984', 'George Orwell', '1949-06-08', 'Dystopie', 3, 3),
    ('To Kill a Mockingbird', 'Harper Lee', '1960-07-11', 'Roman', 4, 4),
    ('Pride and Prejudice', 'Jane Austen', '1813-01-28', 'Romance', 6, 6)
]
cur.executemany("INSERT INTO books (title, author, publication_date, genre, quantity, available) VALUES (?, ?, ?, ?, ?, ?)", books)

# Insertion des emprunts
loans = [
    (1, 1, datetime.now(), (datetime.now() + timedelta(days=14)), 'active'),
    (2, 2, datetime.now(), (datetime.now() + timedelta(days=14)), 'active'),
    (3, 3, datetime.now(), (datetime.now() + timedelta(days=14)), 'active')
]
cur.executemany("INSERT INTO loans (book_id, user_id, loan_date, due_date, status) VALUES (?, ?, ?, ?, ?)", loans)

# Validation des changements et fermeture de la connexion
connection.commit()
connection.close()
