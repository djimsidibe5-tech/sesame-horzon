
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Sésame Horizon - Portail Officiel")

# Montage des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
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
