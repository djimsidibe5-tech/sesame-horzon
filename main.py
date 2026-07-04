from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI(title="Sésame Horizon - Portail Officiel")

# Montage des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="sesame-tech/static"), name="static")
templates = Jinja2Templates(directory="sesame-tech/templates")

DOCS_ROOT = Path("sesame-tech/static/documents")


# --- Définition des niveaux (Licence 1 -> Master 2) ---
class Niveau:
    def __init__(self, slug, nom, semestres):
        self.slug = slug
        self.nom = nom
        self.semestres = semestres  # liste de strings, ex: ["S1", "S2"]


NIVEAUX = [
    Niveau("L1", "Licence 1", ["S1", "S2"]),
    Niveau("L2", "Licence 2", ["S3", "S4"]),
    Niveau("L3", "Licence 3", ["S5", "S6"]),
    Niveau("M1", "Master 1", ["S1", "S2"]),
    Niveau("M2", "Master 2", ["S3", "S4"]),
]


def get_niveau_by_slug(slug):
    return next((n for n in NIVEAUX if n.slug == slug), None)


def scanner_arborescence(chemin_niveau: Path):
    """Scanne static/documents/<niveau>/ pour lister semestre -> session -> matieres."""
    arbo = {}
    if not chemin_niveau.exists():
        return arbo
    for semestre_dir in sorted(chemin_niveau.iterdir()):
        if not semestre_dir.is_dir():
            continue
        arbo[semestre_dir.name] = {}
        for session_dir in sorted(semestre_dir.iterdir()):
            if not session_dir.is_dir():
                continue
            matieres = []
            for matiere_dir in sorted(session_dir.iterdir()):
                if matiere_dir.is_dir():
                    fichiers = [f.name for f in matiere_dir.iterdir() if f.suffix == ".pdf"]
                    matieres.append({"nom": matiere_dir.name, "fichiers": fichiers})
            arbo[semestre_dir.name][session_dir.name] = matieres
    return arbo


# --- Données du créateur ---
biographie = {
    "nom": "SIDIBE DJIM",
    "nationalite": "Ivoirien",
    "niveau": "Licence 3 Sciences Physiques",
    "parcours": "Baccalauréat Série C obtenu en 2024",
    "description": "Étudiant passionné par la physique et le développement web, créateur de la plateforme Sésame Horizon pour soutenir les étudiants.",
}


@app.get("/", name="index", response_class=HTMLResponse)
async def home(request: Request):
    context = {
        "request": request,
        "title": "Sésame Horizon | Accueil",
        "bio": biographie,
        "niveaux": NIVEAUX,
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/profil", name="profil", response_class=HTMLResponse)
async def profil(request: Request):
    return templates.TemplateResponse("profil.html", {"request": request, "bio": biographie})


# --- Page d'un niveau : liste semestres / sessions / matieres ---
@app.get("/niveau/{niveau_slug}", name="niveau", response_class=HTMLResponse)
async def page_niveau(request: Request, niveau_slug: str):
    niveau = get_niveau_by_slug(niveau_slug)
    if niveau is None:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    arbo = scanner_arborescence(DOCS_ROOT / niveau_slug)
    return templates.TemplateResponse(
        "niveau.html",
        {"request": request, "niveau": niveau, "arbo": arbo},
    )


# --- Page d'une matière (sujet + corrigé) ---
@app.get( "/matiere/{niveau_slug}/{semestre}/{session}/{matiere_nom}", name="matiere",   response_class=HTMLResponse)
async def matiere(request: Request, niveau_slug: str, semestre: str, session: str, matiere_nom: str):
    niveau = get_niveau_by_slug(niveau_slug)
    chemin_matiere = DOCS_ROOT / niveau_slug / semestre / session / matiere_nom    
    fichiers = []
    if chemin_matiere.exists():
        for f in chemin_matiere.iterdir():
            if f.suffix == ".pdf":
                # Correction du terme "corriq" en "corrig" pour plus de logique
                categorie = "Corrigé" if "corrig" in f.name.lower() else "Sujet"
                fichiers.append({
                    "nom": f.name,
                    "categorie": categorie,
                    "url": request.url_for(
                        "telecharger",
                        niveau=niveau_slug,
                        semestre=semestre,
                        session=session,
                        matiere=matiere_nom,
                        nom_fichier=f.name,
                    ),
                })
                
    return templates.TemplateResponse(
        "matiere.html",
        {
            "request": request,
            "niveau": niveau,
            "semestre_slug": semestre,
            "session_slug": session,
            "matiere_nom": matiere_nom,
            "fichiers": fichiers,
        },
    )

# --- Téléchargement du PDF ---
@app.get("/telecharger/{niveau}/{semestre}/{session}/{matiere}/{nom_fichier}", name="telecharger")
async def telecharger(niveau: str, semestre: str, session: str, matiere: str, nom_fichier: str):
    chemin_fichier = DOCS_ROOT / niveau / semestre / session / matiere / nom_fichier
    if chemin_fichier.exists() and chemin_fichier.suffix == ".pdf":
        return FileResponse(chemin_fichier, media_type="application/pdf", filename=nom_fichier)
    return {"error": "Ce document n'existe pas encore."}


@app.get("/ressources", name="ressources", response_class=HTMLResponse)
async def ressources(request: Request):
    # Page regroupant Licence 1 à Master 2 et Concours Ingénieurs
    return templates.TemplateResponse("ressources.html", {"request": request, "niveaux": NIVEAUX})
