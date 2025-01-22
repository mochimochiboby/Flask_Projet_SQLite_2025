rom flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/consultation2/')
def ReadBDD():
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)
