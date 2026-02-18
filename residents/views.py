from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Resident

# Create your views here.
@login_required
def resident_list(request):
    residents = Resident.objects.filter(is_active=True)

    context = {
        "residents": residents
    }
    return render(request, "residents/resident_list.html", context)
