from django.shortcuts import render, get_object_or_404
from .models import Character, Equipement


# Create your views here.
def view(request):
    Characters = Character.objects.filter().order_by("id_character")
    Equipements = Equipement.objects.filter().order_by("id_equip")
    return render(
        request,
        "project/view.html",
        {"characters": Characters, "equipements": Equipements},
    )


def character(request, pk):
    try:
        char = get_object_or_404(Character, pk=pk)
        return render(request, "project/character.html", {"character": char})
    except Exception:
        equip = get_object_or_404(Equipement, pk=pk)
        return render(request, "project/equipement.html", {"equipement": equip})
