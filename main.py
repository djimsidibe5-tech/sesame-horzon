
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Sésame Horizon - Portail Officiel")

# Montage des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="sesame-tech/static"), name="static")
templates = Jinja2Templates(directory="sesame-tech/templates")

@app.get("/", name="index")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profil", name="profil")
async def profil(request: Request):
    return templates.TemplateResponse("profil.html", {"request": request})

# Ajoute ici d'autres routes si tu en as (ex: pour matiere.html, niveau.html)
@app.get("/matiere", name="matiere")
async def matiere(request: Request):
    return templates.TemplateResponse("matiere.html", {"request": request})
    
@app.get("/telecharger/{niveau}/{semestre}/{session}/{nom_fichier}", name="telecharger")
async def telecharger(niveau: str, semestre: str, session: str, nom_fichier: str):
    # On reconstruit le chemin vers le fichier sur le serveur Render
    chemin_fichier = f"sesame-tech/static/documents/{niveau}/{semestre}/{session}/{nom_fichier}"
   
    # On vérifie que le fichier existe bien pour éviter les erreurs
    if os.path.exists(chemin_fichier):
        return FileResponse(chemin_fichier, media_type='application/pdf', filename=nom_fichier)
    else:
        return {"error": "Ce document n'existe pas encore."}
    # Données du créateur
    biographie = {
        "nom": "SIDIBE DJIM",
        "nationalite": "Ivoirien",
        "niveau": "Licence 3 Sciences Physiques",
        "parcours": "Baccalauréat Série C obtenu en 2024",
        "description": "Étudiant passionné par la physique et le développement web, créateur de la plateforme Sésame Horizon pour soutenir la réussite académique des étudiants."
    }
   
    context = {
        "request": request,
        "title": "Sésame Horizon | Accueil",
        "bio": biographie
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/ressources", response_class=HTMLResponse)
async def ressources(request: Request):
    # Page regroupant Licence 1 à Master 2 et Concours Ingénieurs
    return templates.TemplateResponse("ressources.html", {"request": request})
