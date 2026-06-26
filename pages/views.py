from django.shortcuts import render


def index(request):
    """Affiche l'unique page de l'application (template Django)."""
    return render(request, "pages/index.html")
