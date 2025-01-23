import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('library.db')

# Lecture et exécution du fichier de schéma SQL
with open('schema2.sql', 'r') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion des données dans la table Utilisateurs
utilisateurs_data = [
    ('Emilie Dupont', 'emilie.dupont@example.com', 'hashed_password_1', 'utilisateur'),
    ('Lucas Leroux', 'lucas.leroux@example.com', 'hashed_password_2', 'utilisateur'),
    ('Amandine Martin', 'amandine.martin@example.com', 'hashed_password_3', 'utilisateur'),
    ('Antoine Tremblay', 'antoine.tremblay@example.com', 'hashed_password_4', 'utilisateur'),
    ('Clement Lahaye', 'cl.lahaye@cfacampusmontsouris.fr', 'ABCDEFG', 'administrateur')
]
cur.executemany(
    "INSERT INTO Utilisateurs (nom, email, mot_de_passe, type_utilisateur) VALUES (?, ?, ?, ?)",
    utilisateurs_data
)

# Insertion des données dans la table Livres
livres_data = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943, 10),
    ('1984', 'George Orwell', 1949, 5),
    ('To Kill a Mockingbird', 'Harper Lee', 1960, 8),
    ('Pride and Prejudice', 'Jane Austen', 1813, 7),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 6),
    ('Moby Dick', 'Herman Melville', 1851, 4),
    ('War and Peace', 'Leo Tolstoy', 1869, 9),
    ('The Catcher in the Rye', 'J.D. Salinger', 1951, 6),
    ('The Hobbit', 'J.R.R. Tolkien', 1937, 10),
    ('Les Misérables', 'Victor Hugo', 1862, 8),
    ('Jane Eyre', 'Charlotte Brontë', 1847, 7),
    ('The Divine Comedy', 'Dante Alighieri', 1320, 3),
    ('The Iliad', 'Homer', -750, 5),
    ('The Odyssey', 'Homer', -725, 6),
    ('Brave New World', 'Aldous Huxley', 1932, 5),
    ('Wuthering Heights', 'Emily Brontë', 1847, 6),
    ('Crime and Punishment', 'Fyodor Dostoevsky', 1866, 7),
    ('The Brothers Karamazov', 'Fyodor Dostoevsky', 1880, 4),
    ('Great Expectations', 'Charles Dickens', 1861, 6),
    ('Don Quixote', 'Miguel de Cervantes', 1615, 8),
    ('One Hundred Years of Solitude', 'Gabriel García Márquez', 1967, 5),
    ('A Tale of Two Cities', 'Charles Dickens', 1859, 7),
    ('Anna Karenina', 'Leo Tolstoy', 1878, 6),
    ('The Count of Monte Cristo', 'Alexandre Dumas', 1844, 10),
    ('Dracula', 'Bram Stoker', 1897, 5),
    ('Frankenstein', 'Mary Shelley', 1818, 4),
    ('Ulysses', 'James Joyce', 1922, 3),
    ('The Lord of the Rings', 'J.R.R. Tolkien', 1954, 12),
    ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 1997, 15),
    ('The Alchemist', 'Paulo Coelho', 1988, 9)
]
cur.executemany(
    "INSERT INTO Livres (titre, auteur, annee_publication, quantite_stock) VALUES (?, ?, ?, ?)",
    livres_data
)

# Insertion des données dans la table Emprunts
emprunts_data = [
    (1, 2, '2023-01-15', None, 'emprunté'),
    (2, 1, '2023-01-20', None, 'emprunté'),
    (3, 4, '2023-01-25', None, 'emprunté')
]
cur.executemany(
    "INSERT INTO Emprunts (utilisateur_id, livre_id, date_emprunt, date_restitution, statut) VALUES (?, ?, ?, ?, ?)",
    emprunts_data
)

# Exemple d'ajout des transactions (stocks)
transactions_data = [
    (1, 'ajout', 10),
    (2, 'ajout', 5),
    (3, 'ajout', 8),
    (4, 'ajout', 7),
    (5, 'ajout', 6)
]
cur.executemany(
    "INSERT INTO Transactions (livre_id, type_transaction, quantite) VALUES (?, ?, ?)",
    transactions_data
)

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()
