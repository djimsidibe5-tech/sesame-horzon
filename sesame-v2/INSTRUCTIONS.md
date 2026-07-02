# Sésame des Techno — remise à plat

Ce dossier remplace tout ce qui est actuellement sur ton dépôt GitHub.
Structure volontairement simple pour éviter les erreurs de chemin :

```
main.py
requirements.txt
render.yaml
static/
  index.html
  profil.html
  style.css
  image/logo.svg
  image/photo-profil.jpg   <- à ajouter toi-même (ta vraie photo)
  documents/                <- à remplir plus tard avec tes PDF
```

## Étapes pour corriger ton dépôt GitHub

1. **Désactive la traduction automatique du navigateur** avant toute
   manipulation (icône de traduction dans la barre d'adresse → "Afficher la
   page d'origine" / ne pas traduire).

2. Sur GitHub, **supprime les fichiers actuels à la racine** :
   `index.html`, `main.py`, `profil.jpg`, `requirements.txt`, `style.css`,
   et le dossier `Statique`. (Clique sur chaque fichier → icône poubelle →
   "Commit changes".)

3. Sur la page principale du dépôt, clique sur **"Add file" → "Upload
   files"**, puis fais un glisser-déposer de **tous les fichiers et dossiers**
   contenus dans ce livrable (garde la même arborescence : `static/` doit
   rester un dossier, pas des fichiers à plat). Valide avec "Commit changes".
   Cette méthode envoie le contenu exact des fichiers, sans passer par un
   copier-coller dans le navigateur — donc aucun risque de traduction.

4. Ajoute ensuite manuellement dans `static/image/` ta photo sous le nom
   `photo-profil.jpg` (upload direct du fichier, toujours pas de copier-coller
   de texte).

5. Sur Render : **Manual Deploy → Clear build cache & deploy**.

## Pourquoi ça plantait avant

Le code copié-collé avait été traduit en français par le navigateur
(`import` → `Importation`, `app.mount` → `Application.Mont`, `:root` →
`:Racine`, etc.). Le code source d'un site (Python, CSS) doit toujours
rester dans sa syntaxe d'origine, jamais traduit.

## Pour la suite

Cette version affiche les niveaux mais ne liste pas encore automatiquement
les PDF déposés (contrairement à la version précédente avec Jinja2). C'est
un choix volontaire pour stabiliser le déploiement d'abord. Une fois le site
en ligne et fonctionnel, dis-le-moi et on réintroduira la liste automatique
des sujets/corrigés par matière.
