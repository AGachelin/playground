from django.shortcuts import render, get_object_or_404
from .forms import MoveForm
from .models import Character, Equipement
import random as rd


# Create your views here.
def view(request):
    Characters = Character.objects.filter().order_by("id_character")
    Equipements = Equipement.objects.filter().order_by("id_equip")
    return render(
        request,
        "project/view.html",
        {"characters": Characters, "equipements": Equipements},
    )


def detail(request, pk):
    try:
        character = get_object_or_404(Character, pk=pk)
        form = MoveForm(request.POST)
        if form.is_valid():
            message = move(form, character)
            Characters = Character.objects.filter().order_by("id_character")
            Equipements = Equipement.objects.filter().order_by("id_equip")
            if message is None:
                return render(
                    request,
                    "project/view.html",
                    {"characters": Characters, "equipements": Equipements},
                )
            else:
                return render(
                    request,
                    "project/character.html",
                    {"character": character, "message": message, "form": form},
                )
        else:
            form = MoveForm()
            return render(
                request,
                "project/character.html",
                {"character": character, "form": form},
            )
    except Exception:
        equip = get_object_or_404(Equipement, pk=pk)
        Characters = Character.objects.filter(lieu_id=equip.id_equip).order_by(
            "id_character"
        )
        return render(
            request,
            "project/equipement.html",
            {"equipement": equip, "characters": Characters},
        )


def move(form, character):
    ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
    nouveau_lieu = get_object_or_404(Equipement, id_equip=form.data["lieu"])
    if nouveau_lieu == ancien_lieu:
        return "Entrer un lieu différent du lieu de départ."
    else:
        match nouveau_lieu.id_equip:
            case "Storage":
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                character.lieu = nouveau_lieu
                character.save()
            case "Charging station":
                if character.etat != "Discharged":
                    if character.etat == "Damaged":
                        return (
                            "Ce robot doit être réparé avant de pouvoir être rechargé."
                        )
                    return "Ce robot n'a pas besoin d'être chargé."
                if nouveau_lieu.disponibilite != "libre":
                    return "La station de chargement est occupée."
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                character.etat = "Fully_charged"
                character.lieu = nouveau_lieu
                character.save()
            case "Repair station":
                if character.etat != "Damaged":
                    return "Ce robot n'a pas besoin d'être réparé."
                if nouveau_lieu.disponibilite != "libre":
                    return "La station de réparation est occupée."
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                character.etat = "Discharged"
                character.lieu = nouveau_lieu
                character.save()
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
            case "Arena":
                if character.etat != "Fully_charged":
                    return "Ce robot n'est pas en état de combattre."
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                if rd.randint(0, 1) == 0:
                    character.etat = "Discharged"
                else:
                    character.etat = "Damaged"
                character.lieu = nouveau_lieu
                character.save()
            case _:
                return "Lieu invalide"
