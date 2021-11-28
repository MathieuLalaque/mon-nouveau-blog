from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement
from django.contrib import messages

# Create your views here.
def animal_list(request):
    animals = Animal.objects.filter()
    equipements=Equipement.objects.filter
    return render(request, 'animalerie/animal_list.html', {'animals': animals,'equipements':equipements})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    if request.method == "POST":
         form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()

    if form.is_valid():

        animal = form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)


        if nouveau_lieu.disponibilite == "libre":
            if nouveau_lieu.id_equip =='mangeoire':
                animal.etat ='repus'
            elif nouveau_lieu.id_equip =='roue':
                animal.etat ='fatigué'
            elif nouveau_lieu.id_equip =='nid':
                animal.etat ='endormi'
            else:
                animal.etat ='affamé'

            animal.save()

            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()

            if not nouveau_lieu.id_equip == "litière":

                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
        else:
            messages.error(request,"lieu occupé")
            return redirect('animal_detail',id_animal=id_animal)

        return redirect('animal_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form})
