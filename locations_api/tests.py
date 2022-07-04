import json

from rest_framework import status
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from django_learn import settings
from locations.models import User
import random
import string
from django.core import files
from locations.models import City, Country, Flag
from locations_api import aditionals


class LocationTests(APITestCase):
    urlpatterns = [
        path('locations_api/', include('locations_api.urls')),
    ]

    @classmethod
    def setUpTestData(cls):
        flag_url = "https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg"
        image = aditionals.image_load(flag_url)
        flag = Flag()
        flag.image.save(image['name'], files.File(image['file']))
        Country.objects.create(name='TestCountry',
                               description='TestCountryDescription',
                               population=10009999,
                               flag=flag,
                               )

        City.objects.create(name='TestCity',
                            country_id=1,
                            longitude=99999,
                            latitude=1000000,
                            )

    def test_create_country(self):
        data = {
            'name': ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
            'description': ''.join(random.choice(string.ascii_lowercase) for i in range(70)),
            'population': random.randint(10000, 9999999),
            'flag_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Flag_of_Japan.svg/1024px-Flag_of_Japan.svg.png"
        }
        response = self.client.post("/api/countries", data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_city(self):
        country = Country.objects.get(name="TestCountry")
        data = {
            'name': ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
            'country': country.id,
            'longitude': random.randint(10000, 9999999),
            'latitude': random.randint(10000, 9999999),
        }
        response = self.client.post("/api/cities", data, format='json')
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_country_get(self):
        response = self.client.get("/api/country/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'TestCountry')
        self.assertEqual(content['description'], 'TestCountryDescription')
        self.assertEqual(content['population'], 10009999)

    def test_city_get(self):
        response = self.client.get("/api/cities/1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)
        self.assertEqual(content['name'], 'TestCity')
        self.assertEqual(content['longitude'], 99999)
        self.assertEqual(content['latitude'], 1000000)