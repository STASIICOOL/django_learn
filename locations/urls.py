from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/<parameter>', views.text),
    path('countries/', views.get_countries, name='contries'),
    path('country/<int:country_id>', views.get_country, name='country'),
    path('city/<int:city_id>', views.get_city, name='city'),
    path('delete_city/<int:city_id>', views.delete_city, ),
    path('country/new/', views.country_new, name='country_new'),
    path('city/new/', views.city_new, name='city_new'),
]

from django.urls import include, path
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

