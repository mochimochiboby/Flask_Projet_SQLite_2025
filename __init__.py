from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Page d'accueil
@app.route('/')
def home():
    return render_template('home.html')

# Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Vérifiez les identifiants dans votre base de données ici
        # Exemple : cur.execute("SELECT * FROM Utilisateurs WHERE email = ? AND mot_de_passe = ?", (email, password))
        return "Authentification en cours..."
    return render_template('login.html')


# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bibliotheque.db')
    conn.row_factory = sqlite3.Row
    return conn

# Routes pour les utilisateurs
@app.route('/rechercher', methods=['GET'])
def rechercher():
    titre = request.args.get('titre', '')
    conn = get_db_connection()
    livres = conn.execute("SELECT * FROM Livres WHERE titre LIKE ?", ('%' + titre + '%',)).fetchall()
    conn.close()
    return jsonify([dict(livre) for livre in livres])

@app.route('/emprunter', methods=['POST'])
def emprunter():
    utilisateur_id = 1  # À remplacer par l'ID réel après authentification
    livre_id = request.form['livre_id']
    conn = get_db_connection()
    conn.execute("INSERT INTO Emprunts (utilisateur_id, livre_id) VALUES (?, ?)", (utilisateur_id, livre_id))
    conn.execute("UPDATE Livres SET quantite_stock = quantite_stock - 1 WHERE livre_id = ?", (livre_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('rechercher'))

@app.route('/restituer', methods=['POST'])
def restituer():
    emprunt_id = request.form['emprunt_id']
    conn = get_db_connection()
    emprunt = conn.execute("SELECT livre_id FROM Emprunts WHERE emprunt_id = ?", (emprunt_id,)).fetchone()
    if emprunt:
        conn.execute("UPDATE Emprunts SET statut = 'restitué', date_restitution = CURRENT_TIMESTAMP WHERE emprunt_id = ?", (emprunt_id,))
        conn.execute("UPDATE Livres SET quantite_stock = quantite_stock + 1 WHERE livre_id = ?", (emprunt['livre_id'],))
        conn.commit()
    conn.close()
    return redirect(url_for('rechercher'))

# Routes pour les administrateurs
@app.route('/ajouter_livre', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    quantite_stock = request.form['quantite_stock']
    conn = get_db_connection()
    conn.execute("INSERT INTO Livres (titre, auteur, quantite_stock) VALUES (?, ?, ?)", (titre, auteur, quantite_stock))
    conn.commit()
    conn.close()
    return redirect(url_for('gestion_livres'))

@app.route('/supprimer_livre', methods=['POST'])
def supprimer_livre():
    livre_id = request.form['livre_id']
    conn = get_db_connection()
    conn.execute("DELETE FROM Livres WHERE livre_id = ?", (livre_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('gestion_livres'))

@app.route('/ajouter_utilisateur', methods=['POST'])
def ajouter_utilisateur():
    nom = request.form['nom']
    email = request.form['email']
    mot_de_passe = request.form['mot_de_passe']
    type_utilisateur = request.form['type_utilisateur']
    conn = get_db_connection()
    conn.execute("INSERT INTO Utilisateurs (nom, email, mot_de_passe, type_utilisateur) VALUES (?, ?, ?, ?)", 
                 (nom, email, mot_de_passe, type_utilisateur))
    conn.commit()
    conn.close()
    return redirect(url_for('gestion_utilisateurs'))

# Routes pour afficher les pages HTML
@app.route('/recherche_livres')
def recherche_livres():
    return render_template('recherche_livres.html')

@app.route('/gestion_livres')
def gestion_livres():
    return render_template('gestion_livres.html')

@app.route('/gestion_utilisateurs')
def gestion_utilisateurs():
    return render_template('gestion_utilisateurs.html')

if __name__ == '__main__':
    app.run(debug=True)
