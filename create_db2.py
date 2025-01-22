import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('database2.db')

# Lecture et exécution du fichier de schéma
with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion des données dans la table Users
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Emilie', 'Dupont', 'emilie.dupont@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Lucas', 'Leroux', 'lucas.leroux@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Amandine', 'Martin', 'amandine.martin@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Antoine', 'Tremblay', 'antoine.tremblay@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Sarah', 'Lambert', 'sarah.lambert@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Nicolas', 'Gagnon', 'nicolas.gagnon@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Charlotte', 'Dubois', 'charlotte.dubois@example.com')
)
cur.execute(
    "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?, ?)", 
    ('Thomas', 'Lefevre', 'thomas.lefevre@example.com')
)

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()
