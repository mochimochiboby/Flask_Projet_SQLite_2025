from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                   
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    mot_de_passe = request.form['mot_de_passe']
    
    conn = get_db_connection()
    cur = conn.cursor()

    # Vérification des informations d'identification de l'utilisateur
    cur.execute("SELECT * FROM utilisateurs WHERE email = ? AND mot_de_passe = ?", (email, mot_de_passe))
    utilisateur = cur.fetchone()

    if utilisateur:
        # Connexion réussie, démarrer une session
        session['utilisateur_id'] = utilisateur['id']
        session['nom'] = utilisateur['nom']
        session['role'] = utilisateur['role']
        return redirect(url_for('dashboard'))  # Page d'accueil après connexion
    else:
        # Si l'utilisateur n'existe pas ou les informations sont incorrectes
        return render_template('login.html', message="Identifiants incorrects")

@app.route('/dashboard')
def dashboard():
    if 'utilisateur_id' not in session:
        return redirect(url_for('index'))  # Rediriger vers la page de login si non connecté
    return render_template('dashboard.html', utilisateur=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/recherche', methods=['GET'])
def recherche_livres():
    titre = request.args.get('titre', '')
    auteur = request.args.get('auteur', '')

    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres WHERE titre LIKE ? AND auteur LIKE ?', 
                          ('%' + titre + '%', '%' + auteur + '%')).fetchall()
    conn.close()

    return render_template('recherche_livres.html', livres=livres)

@app.route('/emprunter', methods=['POST'])
def emprunter():
    livre_id = request.form['livre_id']
    utilisateur_id = 1  # Assumer que l'utilisateur est connecté avec ID 1 pour cet exemple
    date_emprunt = datetime.now().strftime('%Y-%m-%d')

    conn = get_db_connection()
    conn.execute('INSERT INTO emprunts (utilisateur_id, livre_id, date_emprunt) VALUES (?, ?, ?)',
                 (utilisateur_id, livre_id, date_emprunt))
    conn.commit()
    conn.close()

    return 'Livre emprunté avec succès !'

@app.route('/admin_gestion_livres')
def admin_gestion_livres():
    conn = get_db_connection()
    livres = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return render_template('admin_gestion_livres.html', livres=livres)

@app.route('/ajouter_livre', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    stock = request.form['stock']

    conn = get_db_connection()
    conn.execute('INSERT INTO livres (titre, auteur, stock) VALUES (?, ?, ?)', 
                 (titre, auteur, stock))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_gestion_livres'))

if __name__ == '__main__':
    app.run(debug=True)
