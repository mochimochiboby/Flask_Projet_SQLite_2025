import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('library.db')

# Lecture et exécution du fichier de schéma SQL
with open('schema2.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insertion des données dans la table Books
books_data = [
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 'Fiction', 1943, 10),
    ('1984', 'George Orwell', 'Dystopia', 1949, 5),
    ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 1960, 8),
    ('Pride and Prejudice', 'Jane Austen', 'Romance', 1813, 7),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 1925, 6),
    ('Moby Dick', 'Herman Melville', 'Adventure', 1851, 4),
    ('War and Peace', 'Leo Tolstoy', 'Historical Fiction', 1869, 9),
    ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 1951, 6),
    ('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 1937, 10),
    ('Les Misérables', 'Victor Hugo', 'Historical Fiction', 1862, 8),
    ('Jane Eyre', 'Charlotte Brontë', 'Romance', 1847, 7),
    ('The Divine Comedy', 'Dante Alighieri', 'Poetry', 1320, 3),
    ('The Iliad', 'Homer', 'Epic', -750, 5),
    ('The Odyssey', 'Homer', 'Epic', -725, 6),
    ('Brave New World', 'Aldous Huxley', 'Dystopia', 1932, 5),
    ('Wuthering Heights', 'Emily Brontë', 'Romance', 1847, 6),
    ('Crime and Punishment', 'Fyodor Dostoevsky', 'Psychological Fiction', 1866, 7),
    ('The Brothers Karamazov', 'Fyodor Dostoevsky', 'Philosophical Fiction', 1880, 4),
    ('Great Expectations', 'Charles Dickens', 'Fiction', 1861, 6),
    ('Don Quixote', 'Miguel de Cervantes', 'Adventure', 1615, 8),
    ('One Hundred Years of Solitude', 'Gabriel García Márquez', 'Magical Realism', 1967, 5),
    ('A Tale of Two Cities', 'Charles Dickens', 'Historical Fiction', 1859, 7),
    ('Anna Karenina', 'Leo Tolstoy', 'Romance', 1878, 6),
    ('The Count of Monte Cristo', 'Alexandre Dumas', 'Adventure', 1844, 10),
    ('Dracula', 'Bram Stoker', 'Horror', 1897, 5),
    ('Frankenstein', 'Mary Shelley', 'Horror', 1818, 4),
    ('Ulysses', 'James Joyce', 'Modernist Fiction', 1922, 3),
    ('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, 12),
    ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 'Fantasy', 1997, 15),
    ('The Alchemist', 'Paulo Coelho', 'Fable', 1988, 9)
]

# Ajout des livres dans la table Books
cur.executemany("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)", books_data)

# Insertion des données dans la table Users
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Emilie', 'Dupont', 'emilie.dupont@example.com', 'hashed_password_1'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Lucas', 'Leroux', 'lucas.leroux@example.com', 'hashed_password_2'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Amandine', 'Martin', 'amandine.martin@example.com', 'hashed_password_3'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Antoine', 'Tremblay', 'antoine.tremblay@example.com', 'hashed_password_4'))
cur.execute("INSERT INTO Users (FirstName, LastName, Email, PasswordHash) VALUES (?, ?, ?, ?)",
            ('Sarah', 'Lambert', 'sarah.lambert@example.com', 'hashed_password_5'))

# Insertion des données dans la table BorrowedBooks
cur.execute("INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate) VALUES (?, ?, ?)",
            (1, 2, '2023-01-15'))
cur.execute("INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate) VALUES (?, ?, ?)",
            (2, 1, '2023-01-20'))
cur.execute("INSERT INTO BorrowedBooks (UserID, BookID, BorrowDate) VALUES (?, ?, ?)",
            (3, 4, '2023-01-25'))

# Insertion des données dans la table Transactions
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (1, 'Addition', 10))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (2, 'Addition', 5))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (3, 'Addition', 8))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (4, 'Addition', 7))
cur.execute("INSERT INTO Transactions (BookID, TransactionType, Quantity) VALUES (?, ?, ?)",
            (5, 'Addition', 6))

# Validation des changements
connection.commit()

# Fermeture de la connexion
connection.close()
