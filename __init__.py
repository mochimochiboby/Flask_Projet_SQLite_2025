from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions


# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')


@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

    # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"


@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password':  # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)


@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)


@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)


@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire


@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']
    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement


# === NOUVELLES ROUTES POUR LA GESTION DES LIVRES ET DES UTILISATEURS ===

# Ajouter un livre
@app.route('/add_book/', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form.get('genre', '')
        year = request.form.get('year', None)
        stock = request.form['stock']

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Books (Title, Author, Genre, PublishedYear, Stock) VALUES (?, ?, ?, ?, ?)",
                       (title, author, genre, year, stock))
        conn.commit()
        conn.close()
        return redirect('/list_books/')
    return render_template('add_book.html')


# Supprimer un livre
@app.route('/delete_book/', methods=['GET', 'POST'])
def delete_book():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        book_id = request.form['book_id']
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        conn.commit()
        conn.close()
        return redirect('/list_books/')
    return render_template('delete_book.html', books=books)


# Liste des livres
@app.route('/list_books/')
def list_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()
    return render_template('list_books.html', books=books)


# Rechercher un livre
@app.route('/search_books/', methods=['GET', 'POST'])
def search_books():
    books = []
    if request.method == 'POST':
        title = request.form['title']
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE Title LIKE ?", (f"%{title}%",))
        books = cursor.fetchall()
        conn.close()
    return render_template('search_books.html', books=books)


# Emprunter un livre
@app.route('/borrow_book/', methods=['GET', 'POST'])
def borrow_book():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM Books WHERE Stock > 0")
    books = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO BorrowedBooks (UserID, BookID) VALUES (?, ?)", (user_id, book_id))
        cursor.execute("UPDATE Books SET Stock = Stock - 1 WHERE BookID = ?", (book_id,))
        conn.commit()
        conn.close()
        return redirect('/list_books/')
    return render_template('borrow_book.html', users=users, books=books)


# Gestion des utilisateurs
@app.route('/manage_users/')
def manage_users():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return render_template('manage_users.html', users=users)


# Gestion des stocks
@app.route('/manage_stock/', methods=['GET', 'POST'])
def manage_stock():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        book_id = request.form['book_id']
        quantity = request.form['quantity']
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE Books SET Stock = Stock + ? WHERE BookID = ?", (quantity, book_id))
        conn.commit()
        conn.close()
        return redirect('/list_books/')
    return render_template('manage_stock.html', books=books)


if __name__ == "__main__":
    app.run(debug=True)
