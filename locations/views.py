from django.shortcuts import render, get_object_or_404, redirect
from locations.models import Country, City, Flag
from django.contrib.auth.decorators import login_required
from locations.forms import CountryForm, CityForm, FlagForm
from rest_framework import generics




from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world!")

def text(request, parameter):
    return HttpResponse(f"parameter:{parameter}")

@login_required
def get_countries(request):
    contries = Country.objects.all()
    return render(request, 'locations/all_contries.html', {'contries': contries})

@login_required
def get_country(request, country_id):
    contry = get_object_or_404(Country,id=country_id)
    for city in contry.city_set.all():
        print(f"{city.name}")

    return render(request, 'locations/single_country.html', {'country': contry})

@login_required
def get_city(request, city_id):
    city = get_object_or_404(City,id=city_id)
    return render(request, 'locations/single_city.html', {'city': city})

def delete_city(request, city_id):
    city = get_object_or_404(City, id=city_id)
    city.delete()
    return redirect(f'/locations/country/{city.country.id}')



def country_new(request):
    if request.method == "POST":
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            flag = Flag.objects.create(image=request.POST['image'])
            post = form.save(commit=False)
            post.flag = flag
            post.save()
            return redirect('country', country_id=post.id)
    else:
        form = CountryForm()
        flag_form = FlagForm
    return render(request, 'locations/country_edit.html', {'form': form, 'flag_form': flag_form})

def city_new(request):
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('city', city_id=post.id)
    else:
        form = CityForm()
    return render(request, 'locations/city_edit.html', {'form': form})



