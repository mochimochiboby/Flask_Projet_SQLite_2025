from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secret_key'

# Connexion à la base de données
def get_db():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Gestion des sessions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Accès réservé aux administrateurs', 'error')
            return redirect(url_for('user_home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        db.close()
        
        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_home'))
            return redirect(url_for('user_home'))
        flash('Identifiants incorrects', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin_home')
@admin_required
def admin_home():
    return render_template('admin_home.html')

@app.route('/user_home')
@login_required
def user_home():
    return render_template('user_home.html')

@app.route('/user_livres')
@login_required
def user_livres():
    db = get_db()
    books = db.execute('SELECT * FROM books WHERE available > 0').fetchall()
    db.close()
    return render_template('page_livres.html', books=books)

@app.route('/user_livres_empruntes')
@login_required
def user_livres_empruntes():
    db = get_db()
    loans = db.execute('''
        SELECT books.title, loans.loan_date, loans.due_date
        FROM loans
        JOIN books ON loans.book_id = books.id
        WHERE loans.user_id = ? AND loans.status = 'active'
    ''', (session['user_id'],)).fetchall()
    db.close()
    return render_template('page_livres_empruntes.html', loans=loans)

@app.route('/admin_livres')
@admin_required
def admin_livres():
    db = get_db()
    books = db.execute('SELECT * FROM books').fetchall()
    db.close()
    return render_template('gestion_livres.html', books=books)

@app.route('/admin_utilisateurs')
@admin_required
def admin_utilisateurs():
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    return render_template('gestion_utilisateurs.html', users=users)

@app.route('/admin_emprunts')
@admin_required
def admin_emprunts():
    db = get_db()
    loans = db.execute('''
        SELECT books.title, users.first_name, users.last_name, loans.loan_date, loans.due_date
        FROM loans
        JOIN books ON loans.book_id = books.id
        JOIN users ON loans.user_id = users.id
    ''').fetchall()
    db.close()
    return render_template('gestion_emprunts.html', loans=loans)

@app.route('/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        publication_date = request.form['publication_date']
        quantity = int(request.form['quantity'])
        
        db = get_db()
        db.execute('INSERT INTO books (title, author, genre, publication_date, quantity, available) VALUES (?, ?, ?, ?, ?, ?)',
                   (title, author, genre, publication_date, quantity, quantity))
        db.commit()
        db.close()
        flash('Livre ajouté avec succès', 'success')
        return redirect(url_for('admin_livres'))
    
    return render_template('ajouter_livre.html')  # Cette page sera une simple page avec un formulaire pour ajouter un livre


if __name__ == '__main__':
    app.run(debug=True)
