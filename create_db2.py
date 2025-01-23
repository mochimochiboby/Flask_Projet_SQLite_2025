import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('bibliotheque.db')

# Exécution du schéma pour créer les tables (assurez-vous que schema2.sql existe)
with open('schema2.sql') as f:
    connection.executescript(f.read())

# Création du curseur
cur = connection.cursor()

# Insertion des utilisateurs
cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)", ('Emilie Dupont', 'emilie.dupont@example.com', 'motdepasse1', 'utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)", ('Lucas Leroux', 'lucas.leroux@example.com', 'motdepasse2', 'utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)", ('Amandine Martin', 'amandine.martin@example.com', 'motdepasse3', 'utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)", ('Antoine Tremblay', 'antoine.tremblay@example.com', 'motdepasse4', 'utilisateur'))
cur.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)", ('Clement Lahaye', 'cl.lahaye@cfacampusmontsouris.fr', 'motdepasseadmin', 'administrateur'))

# Insertion des livres
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943, 10))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('1984', 'George Orwell', 1949, 5))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('To Kill a Mockingbird', 'Harper Lee', 1960, 8))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('Pride and Prejudice', 'Jane Austen', 1813, 7))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 6))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('Moby Dick', 'Herman Melville', 1851, 4))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('War and Peace', 'Leo Tolstoy', 1869, 9))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('The Catcher in the Rye', 'J.D. Salinger', 1951, 6))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('The Hobbit', 'J.R.R. Tolkien', 1937, 10))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('Les Misérables', 'Victor Hugo', 1862, 8))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('Jane Eyre', 'Charlotte Brontë', 1847, 7))
cur.execute("INSERT INTO livres (titre, auteur, annee_publication, stock) VALUES (?, ?, ?, ?)", ('The Divine Comedy', 'Dante Alighieri', 1320, 3))

# Insertion des emprunts
cur.execute("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_restitution, statut) VALUES (?, ?, ?, ?, ?)", (1, 2, '2023-01-15', None, 'emprunté'))
cur.execute("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_restitution, statut) VALUES (?, ?, ?, ?, ?)", (2, 1, '2023-01-20', None, 'emprunté'))
cur.execute("INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt, date_restitution, statut) VALUES (?, ?, ?, ?, ?)", (3, 4, '2023-01-25', None, 'emprunté'))

# Insertion des transactions (ajout de stock)
cur.execute("INSERT INTO transactions (livre_id, type_transaction, quantite, date_transaction) VALUES (?, ?, ?, ?)", (1, 'ajout', 10, '2023-01-01'))
cur.execute("INSERT INTO transactions (livre_id, type_transaction, quantite, date_transaction) VALUES (?, ?, ?, ?)", (2, 'ajout', 5, '2023-01-05'))
cur.execute("INSERT INTO transactions (livre_id, type_transaction, quantite, date_transaction) VALUES (?, ?, ?, ?)", (3, 'ajout', 8, '2023-01-10'))
cur.execute("INSERT INTO transactions (livre_id, type_transaction, quantite, date_transaction) VALUES (?, ?, ?, ?)", (4, 'ajout', 7, '2023-01-12'))
cur.execute("INSERT INTO transactions (livre_id, type_transaction, quantite, date_transaction) VALUES (?, ?, ?, ?)", (5, 'ajout', 6, '2023-01-15'))

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()
