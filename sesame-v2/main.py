"""
Sésame des Techno — version simplifiée
----------------------------------------
Tout le site (HTML, CSS, images, documents) vit dans le dossier static/.
FastAPI se contente de servir ce dossier tel quel : index.html est
automatiquement la page d'accueil, et chaque fichier .html est accessible
directement par son nom (ex. /profil.html).

C'est volontairement le plus simple possible pour éviter les erreurs de
chemin (Jinja2Templates, dossiers manquants, etc.).
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Sésame des Techno")

# html=True -> sert automatiquement static/index.html sur "/"
# et static/profil.html sur "/profil.html", etc.
app.mount(
    "/",
    StaticFiles(directory=str(BASE_DIR / "static"), html=True),
    name="static",
)
