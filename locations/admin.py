from django.contrib import admin
from locations.models import Flag, Country, City

# Register your models here.

admin.site.register(Flag)

@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_filter = ['country']

@admin.register(Country)
class AdminCountry(admin.ModelAdmin):
    search_fields = ['name']


