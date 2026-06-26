"""
Script de test pour le pipeline CI/CD.

Ce script vérifie la couleur de fond de la page d'accueil de l'application
Django en analysant le HTML réellement rendu par la vue (via le client de
test de Django, sans avoir besoin de lancer un vrai serveur).

Règle métier du rattrapage DevOps :
    - Si la couleur de fond est "orange" -> le test DOIT échouer.
      GitHub Actions bloque alors le merge sur `main` et empêche
      le déploiement sur Vercel.
    - Si la couleur de fond est "blue" (ou toute autre couleur) -> le test
      réussit. GitHub Actions valide l'étape, ce qui autorise le merge sur
      `main` et déclenche le déploiement automatique sur Vercel.

Exécution locale :
    python -m pytest tests/test_color.py -v
"""

import os
import re

import django

# On indique à Django où trouver les settings du projet avant de l'initialiser.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.test import Client  # noqa: E402  (import après django.setup())

# Couleur interdite : si elle est détectée, le déploiement doit être bloqué.
FORBIDDEN_COLOR = "orange"


def get_background_color() -> str:
    """
    Récupère la couleur de fond appliquée au <body> de la page d'accueil.

    On effectue une vraie requête HTTP (simulée) vers la vue Django, puis on
    extrait la valeur de `background-color` directement depuis le HTML
    renvoyé. Cela garantit que l'on teste le rendu réel de la page, et pas
    simplement le contenu du fichier source.
    """
    client = Client()
    response = client.get("/")

    assert response.status_code == 200, (
        f"La page d'accueil a renvoyé le code {response.status_code} "
        "au lieu de 200."
    )

    html = response.content.decode("utf-8")
    match = re.search(r"background-color:\s*([#\w]+)", html, re.IGNORECASE)

    assert match is not None, (
        "Impossible de trouver une propriété 'background-color' dans la "
        "page rendue. Vérifie le template pages/index.html."
    )

    return match.group(1).strip().lower()


def test_background_color_is_not_orange():
    """
    Test principal du pipeline : le fond de la page ne doit jamais être
    orange. C'est ce test qui est exécuté automatiquement par GitHub Actions
    à chaque push / pull request sur la branche `main`.
    """
    color = get_background_color()
    print(f"Couleur de fond détectée sur la page : '{color}'")

    assert color != FORBIDDEN_COLOR, (
        f"ECHEC : la couleur de fond est '{color}'. La couleur orange est "
        "interdite en production. Le merge sur main et le déploiement "
        "Vercel doivent être bloqués."
    )


if __name__ == "__main__":
    # Permet aussi un lancement direct : python tests/test_color.py
    test_background_color_is_not_orange()
    print("Test réussi : la page peut être déployée.")
