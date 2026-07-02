"""
Sésame des Techno
------------------
Bibliothèque en ligne des anciens sujets et corrigés
(Licence 1 -> Master 2, spécialité Sciences Physiques)

Auteur : SIDIBÉ Djim
"""

import os
from pathlib import Path
from flask import Flask, render_template, abort

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "static" / "documents"

# ---------------------------------------------------------------------------
# Données de structure du site (niveaux -> semestres -> sessions -> matières)
# ---------------------------------------------------------------------------

NIVEAUX = [
    {"nom": "Licence 1", "slug": "licence-1", "semestres": ["Semestre 1", "Semestre 2"]},
    {"nom": "Licence 2", "slug": "licence-2", "semestres": ["Semestre 3", "Semestre 4"]},
    {"nom": "Licence 3", "slug": "licence-3", "semestres": ["Semestre 5", "Semestre 6"]},
    {"nom": "Master 1", "slug": "master-1", "semestres": ["Semestre 7", "Semestre 8"]},
    {"nom": "Master 2", "slug": "master-2", "semestres": ["Semestre 9", "Semestre 10"]},
]

SESSIONS = ["Session 1", "Session 2"]


def slugify(texte: str) -> str:
    """Transforme un texte en identifiant d'URL simple (sans accents/espaces)."""
    remplacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a",
        "î": "i", "ï": "i",
        "ô": "o", "ö": "o",
        "û": "u", "ù": "u", "ü": "u",
        "ç": "c",
    }
    texte = texte.lower().strip()
    for accent, lettre in remplacements.items():
        texte = texte.replace(accent, lettre)
    return texte.replace(" ", "-")


def get_niveau(slug: str):
    for n in NIVEAUX:
        if n["slug"] == slug:
            return n
    return None


def lister_matieres(niveau_slug, semestre_slug, session_slug):
    """Renvoie la liste des matières (dossiers) disponibles pour une session donnée."""
    chemin = DOCS_DIR / niveau_slug / semestre_slug / session_slug
    matieres = []
    if chemin.exists():
        for entree in sorted(chemin.iterdir()):
            if entree.is_dir():
                fichiers = [f for f in entree.iterdir() if f.is_file()]
                matieres.append({
                    "nom": entree.name.replace("-", " ").title(),
                    "slug": entree.name,
                    "nb_fichiers": len(fichiers),
                })
    return matieres


def lister_fichiers(niveau_slug, semestre_slug, session_slug, matiere_slug):
    """Renvoie la liste des fichiers (sujets/corrigés) d'une matière."""
    chemin = DOCS_DIR / niveau_slug / semestre_slug / session_slug / matiere_slug
    fichiers = []
    if chemin.exists():
        for f in sorted(chemin.iterdir()):
            if f.is_file():
                nom_bas = f.name.lower()
                if "corrige" in nom_bas or "correction" in nom_bas:
                    categorie = "Corrigé"
                elif "sujet" in nom_bas or "epreuve" in nom_bas:
                    categorie = "Sujet"
                else:
                    categorie = "Document"
                url = f"/static/documents/{niveau_slug}/{semestre_slug}/{session_slug}/{matiere_slug}/{f.name}"
                fichiers.append({"nom": f.name, "categorie": categorie, "url": url})
    return fichiers


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html", niveaux=NIVEAUX)


@app.route("/niveau/<niveau_slug>")
def niveau(niveau_slug):
    n = get_niveau(niveau_slug)
    if not n:
        abort(404)

    semestres_data = []
    for semestre in n["semestres"]:
        semestre_slug = slugify(semestre)
        sessions_data = []
        for session in SESSIONS:
            session_slug = slugify(session)
            matieres = lister_matieres(niveau_slug, semestre_slug, session_slug)
            sessions_data.append({
                "nom": session,
                "slug": session_slug,
                "matieres": matieres,
            })
        semestres_data.append({
            "nom": semestre,
            "slug": semestre_slug,
            "sessions": sessions_data,
        })

    return render_template("niveau.html", niveau=n, semestres=semestres_data)


@app.route("/matiere/<niveau_slug>/<semestre_slug>/<session_slug>/<matiere_slug>")
def matiere(niveau_slug, semestre_slug, session_slug, matiere_slug):
    n = get_niveau(niveau_slug)
    if not n:
        abort(404)

    fichiers = lister_fichiers(niveau_slug, semestre_slug, session_slug, matiere_slug)
    matiere_nom = matiere_slug.replace("-", " ").title()

    return render_template(
        "matiere.html",
        niveau=n,
        semestre_slug=semestre_slug,
        session_slug=session_slug,
        matiere_slug=matiere_slug,
        matiere_nom=matiere_nom,
        fichiers=fichiers,
    )


@app.route("/profil")
def profil():
    return render_template("profil.html")


@app.errorhandler(404)
def page_non_trouvee(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Crée le dossier de documents s'il n'existe pas encore
    os.makedirs(DOCS_DIR, exist_ok=True)
    app.run(debug=True)
