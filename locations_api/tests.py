from rest_framework import status
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from django_learn import settings
from locations.models import User
import random
import string
from locations.models import City, Country

class LocationTests(APITestCase):
    urlpatterns = [
        path('locations_api/', include('locations_api.urls')),
    ]

    def test_create_country(self):
        url = reverse('locations_api:CountryLists')
        data = {
            'name': ''.join(random.choice(string.ascii_lowercase) for i in range(10)),
            'description': ''.join(random.choice(string.ascii_lowercase) for i in range(70)),
            'population': random.randint(10000, 9999999),
            'flag_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Flag_of_Japan.svg/1024px-Flag_of_Japan.svg.png"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_city(self):
        data = {
            'name': ''.join(random.choice(string.ascii_lowercase) for i in range(12)),
            'country': random.randint(1,5),
            'longitude': random.randint(10000, 9999999),
            'latitude': random.randint(10000, 9999999),
        }
        response = self.client.post("/api/cities", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_country_get(self):
        response = self.client.get(reverse('locations_api:countries/', kwargs={'country_id': random.randint(1, 5)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city_get(self):
        response = self.client.get(reverse('locations_api:city/', kwargs={'id': random.randint(1,5)}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)