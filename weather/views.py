import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    appid = 'fe6bc397bab08811f34916f92e229545'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res.get('main'):
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"]
            }
        else:
            city_info = {
                'city': city.name,
                'error': True
            }
        all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)
