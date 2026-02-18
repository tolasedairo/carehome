from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resident
from .forms import ResidentForm


# Create your views here.
# This view retrieves all active residents 
# from the database and renders them in a template.
@login_required
def resident_list(request):
    residents = Resident.objects.filter(is_active=True)

    context = {
        "residents": residents
    }
    return render(request, "residents/resident_list.html", context)


# This view allows managers to create new resident records.
@login_required
def resident_create(request):
    """
    Only managers can create residents.
    """

    if request.user.role != "MANAGER":
        return redirect("residents:list")

    if request.method == "POST":
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("residents:list")
    else:
        form = ResidentForm()

    context = {
        "form": form
    }

    return render(request, "residents/resident_form.html", context)

