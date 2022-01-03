from locations_api.views import CountryList, CountryDell
from rest_framework import routers
from django.urls import path

router = routers.SimpleRouter(trailing_slash=False)
app_name = "locations_api"

urlpatterns = [
    path('countries', CountryList.as_view(), name="CountryLists"),
    path('country/<country_id>', CountryDell.as_view(), name="CountryDell"),
]