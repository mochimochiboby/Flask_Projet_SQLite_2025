-- Table des utilisateurs
DROP TABLE IF EXISTS utilisateurs;
CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('utilisateur', 'administrateur'))
);

-- Table des livres
DROP TABLE IF EXISTS livres;
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    annee_publication INTEGER,
    stock INTEGER NOT NULL
);

-- Table des emprunts
DROP TABLE IF EXISTS emprunts;
CREATE TABLE emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER,
    livre_id INTEGER,
    date_emprunt DATE NOT NULL,
    date_retour DATE,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(livre_id) REFERENCES livres(id)
);

-- Table des transactions (pour gérer les emprunts et restitutions)
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER,
    livre_id INTEGER,
    type_transaction TEXT NOT NULL CHECK(type_transaction IN ('emprunt', 'restitution')),
    date_transaction DATE NOT NULL,
    FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id),
    FOREIGN KEY(livre_id) REFERENCES livres(id)
);
