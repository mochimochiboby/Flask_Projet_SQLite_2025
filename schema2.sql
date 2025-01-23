-- Table pour les utilisateurs
DROP TABLE IF EXISTS Utilisateurs;
CREATE TABLE Utilisateurs (
    utilisateur_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    type_utilisateur TEXT NOT NULL CHECK (type_utilisateur IN ('utilisateur', 'administrateur')),
    date_inscription DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table pour les livres
DROP TABLE IF EXISTS Livres;
CREATE TABLE Livres (
    livre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    annee_publication INTEGER,
    quantite_stock INTEGER NOT NULL CHECK (quantite_stock >= 0)
);

-- Table pour les emprunts
DROP TABLE IF EXISTS Emprunts;
CREATE TABLE Emprunts (
    emprunt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER NOT NULL,
    livre_id INTEGER NOT NULL,
    date_emprunt DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_restitution DATETIME,
    statut TEXT NOT NULL DEFAULT 'emprunté' CHECK (statut IN ('emprunté', 'restitué')),
    FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(utilisateur_id),
    FOREIGN KEY (livre_id) REFERENCES Livres(livre_id)
);
