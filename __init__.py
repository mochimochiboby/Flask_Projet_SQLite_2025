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
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Vérification de l'authentification
def is_authenticated():
    return 'user_id' in session

# Vérification si l'utilisateur est admin
def is_admin():
    return session.get('is_admin', False)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT UserID, PasswordHash, Email FROM Users WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['is_admin'] = email == 'admin@example.com'  # Remplacez par votre logique admin
            return redirect('/admin/' if is_admin() else '/')
        else:
            return render_template('login.html', error=True)

    return render_template('login.html', error=False)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/login/')

@app.route('/borrow/', methods=['GET', 'POST'])
def borrow():
    if not is_authenticated():
        return redirect('/login/')

    if request.method == 'POST':
        book_id = request.form['book_id']

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Stock FROM Books WHERE BookID = ?", (book_id,))
        book = cursor.fetchone()

        if book and book[0] > 0:
            cursor.execute("INSERT INTO BorrowedBooks (UserID, BookID) VALUES (?, ?)", (session['user_id'], book_id))
            cursor.execute("UPDATE Books SET Stock = Stock - 1 WHERE BookID = ?", (book_id,))
            conn.commit()
        conn.close()
        return redirect('/')

    return render_template('borrow.html')

@app.route('/admin/borrows/')
def admin_borrows():
    if not is_admin():
        return redirect('/login/')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.BorrowID, u.FirstName || ' ' || u.LastName AS UserName, bo.Title AS BookTitle, b.BorrowDate, b.ReturnDate
        FROM BorrowedBooks b
        JOIN Users u ON b.UserID = u.UserID
        JOIN Books bo ON b.BookID = bo.BookID
    """)
    borrows = cursor.fetchall()
    conn.close()

    return render_template('admin_borrowed_books.html', borrows=borrows)

@app.route('/admin/')
def admin_dashboard():
    if not is_admin():
        return redirect('/login/')
    return render_template('admin_dashboard.html')


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

# Retourner livre
@app.route('/return_book/', methods=['GET', 'POST'])
def return_book():
    if not is_authenticated():
        return redirect('/login/')

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        borrow_id = request.form['borrow_id']

        # Mettre à jour la date de retour dans BorrowedBooks
        cursor.execute("UPDATE BorrowedBooks SET ReturnDate = CURRENT_DATE WHERE BorrowID = ?", (borrow_id,))
        
        # Récupérer l'ID du livre retourné
        cursor.execute("SELECT BookID FROM BorrowedBooks WHERE BorrowID = ?", (borrow_id,))
        book_id = cursor.fetchone()[0]

        # Incrémenter le stock du livre dans la table Books
        cursor.execute("UPDATE Books SET Stock = Stock + 1 WHERE BookID = ?", (book_id,))

        # Commit les changements
        conn.commit()

        # Rediriger l'utilisateur vers la page des emprunts ou une autre page de confirmation
        return redirect('/my_borrows/')  # ou une autre page de votre choix

    # Afficher les livres empruntés par l'utilisateur
    cursor.execute("""
        SELECT b.BorrowID, bo.Title AS BookTitle, b.BorrowDate
        FROM BorrowedBooks b
        JOIN Books bo ON b.BookID = bo.BookID
        WHERE b.UserID = ? AND b.ReturnDate IS NULL
    """, (session['user_id'],))

    borrows = cursor.fetchall()
    conn.close()

    return render_template('return_book.html', borrows=borrows)


if __name__ == "__main__":
    app.run(debug=True)
