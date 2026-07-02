# Sésame des Techno

Bibliothèque en ligne des anciens sujets et corrigés en Sciences Physiques
(Licence 1 → Master 2), créée par SIDIBÉ Djim.

## Installation

```bash
pip install -r requirements.txt
python main.py
```

Le site est ensuite accessible sur : http://127.0.0.1:5000

## Ajouter des sujets et corrigés

Aucune base de données n'est utilisée : il suffit de déposer les fichiers PDF
dans le bon dossier sous `static/documents/`, en respectant ce chemin :

```
static/documents/<niveau>/<semestre>/<session>/<matiere>/
```

Exemple pour la Mécanique du point, en Licence 1, Semestre 1, Session 1 :

```
static/documents/licence-1/semestre-1/session-1/mecanique-du-point/sujet-2024.pdf
static/documents/licence-1/semestre-1/session-1/mecanique-du-point/corrige-2024.pdf
```

Règles à respecter :
- Les slugs de niveau sont : `licence-1`, `licence-2`, `licence-3`, `master-1`, `master-2`
- Les slugs de semestre sont : `semestre-1` à `semestre-10` (2 par niveau)
- Les slugs de session sont : `session-1`, `session-2`
- Le nom du dossier "matière" peut être libre (ex. `mecanique-du-point`,
  `electromagnetisme`) — il sera affiché automatiquement avec une majuscule.
- Dans le nom du fichier, inclue le mot `sujet` ou `corrige` pour qu'il soit
  étiqueté correctement sur le site (ex. `sujet-...pdf`, `corrige-...pdf`).

Une fois les fichiers déposés, ils apparaissent automatiquement sur la page
de la matière correspondante — aucune modification de code n'est nécessaire.

## Ajouter la photo de profil

Place une photo au format `static/image/photo-profil.jpg` : elle s'affichera
automatiquement sur la page "Profil".

## Structure du projet

```
main.py                 -> application Flask (routes)
requirements.txt        -> dépendances Python
templates/               -> pages HTML (Jinja2)
static/css/style.css     -> feuille de style
static/image/            -> logo + photo de profil
static/documents/        -> tous les sujets et corrigés (PDF)
```
