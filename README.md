# Pipeline CI/CD - Rattrapage DevOps

Application web Django (une seule page, template Django) avec un pipeline
CI/CD automatisé : **GitHub Actions** pour les tests, **Vercel** pour le
déploiement de production.

## Architecture du pipeline

- **Branche `test`** : branche de développement. C'est sur cette branche que
  l'on push par défaut. Chaque push y déclenche le test de couleur (retour
  rapide).
- **Branche `main`** : branche de production, connectée directement à
  Vercel. Le déploiement automatique n'a lieu que si le test passe.
- **GitHub Actions** (`.github/workflows/ci.yml`) : exécute
  `tests/test_color.py`, qui vérifie la couleur de fond de la page rendue.
  - Fond **orange** → test en échec → merge vers `main` bloqué (si la
    protection de branche est activée) → pas de déploiement.
  - Fond **bleu** (ou toute autre couleur) → test réussi → merge vers `main`
    autorisé → déploiement automatique sur Vercel.

## Lancer le projet en local

```bash
python -m venv venv
source venv/bin/activate        # ou venv\Scripts\activate sous Windows
pip install -r requirements.txt
python manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/

## Lancer le test de couleur en local

```bash
python -m pytest tests/test_color.py -v
```

## Structure du projet

```
.
├── manage.py
├── requirements.txt
├── mysite/                     # configuration du projet Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pages/                      # application avec la page d'accueil
│   ├── views.py
│   ├── urls.py
│   └── templates/pages/index.html
├── tests/
│   └── test_color.py           # script de test de la couleur de fond
└── .github/workflows/ci.yml    # workflow GitHub Actions
```
