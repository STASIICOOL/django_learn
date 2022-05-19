from locations_api.views import CountryList, CountryDell, CityViewSet, CreateUserAPIView, UserRetrieveUpdateAPIView, GoogleView
from rest_framework import routers
from django.urls import include,path
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from quickstart.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'cities', CityViewSet)
app_name = "locations_api"

urlpatterns = [
    path('countries', CountryList.as_view(), name="CountryLists"),
    path('country/<country_id>', CountryDell.as_view(), name="CountryDell"),
    path('', include(router.urls)),
    url(r'user/create/$', CreateUserAPIView.as_view()),
    url(r'user/update/$', UserRetrieveUpdateAPIView.as_view()),
    path('google/', GoogleView.as_view(), name='google'),
]

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
urlpatterns += router.urls

