import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('bibliotheque.db')

# Exécution du schéma pour créer les tables
with open('schema.sql') as f:
    connection.executescript(f.read())

# Création du curseur
cur = connection.cursor()

# Insertion des utilisateurs
cur.execute("INSERT INTO users (nom, prenom, email, password, role) VALUES (?, ?, ?, ?, ?)", ('Dupont', 'Emilie', 'emilie.dupont@example.com', 'motdepasse1', 'user'))
cur.execute("INSERT INTO users (nom, prenom, email, password, role) VALUES (?, ?, ?, ?, ?)", ('Leroux', 'Lucas', 'lucas.leroux@example.com', 'motdepasse2', 'user'))
cur.execute("INSERT INTO users (nom, prenom, email, password, role) VALUES (?, ?, ?, ?, ?)", ('Martin', 'Amandine', 'amandine.martin@example.com', 'motdepasse3', 'user'))
cur.execute("INSERT INTO users (nom, prenom, email, password, role) VALUES (?, ?, ?, ?, ?)", ('Tremblay', 'Antoine', 'antoine.tremblay@example.com', 'motdepasse4', 'user'))
cur.execute("INSERT INTO users (nom, prenom, email, password, role) VALUES (?, ?, ?, ?, ?)", ('Lahaye', 'Clement', 'cl.lahaye@cfacampusmontsouris.fr', 'motdepasseadmin', 'admin'))

# Insertion des livres
cur.execute("INSERT INTO books (title, author, publication_date, genre) VALUES (?, ?, ?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry', '1943-04-06', 'Conte'))
cur.execute("INSERT INTO books (title, author, publication_date, genre) VALUES (?, ?, ?, ?)", ('1984', 'George Orwell', '1949-06-08', 'Dystopie'))
cur.execute("INSERT INTO books (title, author, publication_date, genre) VALUES (?, ?, ?, ?)", ('Pride and Prejudice', 'Jane Austen', '1813-01-28', 'Romance'))
cur.execute("INSERT INTO books (title, author, publication_date, genre) VALUES (?, ?, ?, ?)", ('Les Misérables', 'Victor Hugo', '1862-04-03', 'Roman Historique'))
cur.execute("INSERT INTO books (title, author, publication_date, genre) VALUES (?, ?, ?, ?)", ('Moby Dick', 'Herman Melville', '1851-10-18', 'Aventure'))

# Insertion des emprunts
cur.execute("INSERT INTO loans (book_id, user_id, loan_date, due_date, status) VALUES (?, ?, ?, ?, ?)", (1, 1, '2024-01-15', '2024-01-29', 'active'))
cur.execute("INSERT INTO loans (book_id, user_id, loan_date, due_date, status) VALUES (?, ?, ?, ?, ?)", (2, 2, '2024-01-20', '2024-02-03', 'active'))
cur.execute("INSERT INTO loans (book_id, user_id, loan_date, due_date, status) VALUES (?, ?, ?, ?, ?)", (3, 3, '2024-01-25', '2024-02-08', 'active'))

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()
