from django.contrib.auth.models import User, Group
from locations.models import Country,City, Flag
from rest_framework import serializers
from locations.validators import validate_image_url
from locations.validators import validate_image_url
from . import aditionals
from django.core import files

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"




class CitySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True,read_only=True)
    class Meta:
        model = City
        fields = ('id', 'user', 'name', 'country')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name') if validated_data.get('name') is not None else instance.name
        instance.country = validated_data.get('country') if validated_data.get('country') is not None else instance.country
        instance.save()
        return instance

class CountrySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True,read_only=True)
    cities = CitySerializer(many=True,read_only=True)

    class Meta:
        model = Country
        fields = ("name","description","population","cities_count","user", 'cities')

    def create(self, validated_data):
        request_data = self.context.get("request").data
        flag_url = validate_image_url(request_data.get("flag_url"))
        image = aditionals.image_load(flag_url)
        flag = Flag()
        flag.image.save(image['name'], files.File(image['file']))
        country = Country.objects.create(flag=flag, **validated_data)
        return country

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name') if validated_data.get('name') is not None else instance.name
        instance.description = validated_data.get('description') if validated_data.get(
            'description') is not None else instance.description
        instance.population = validated_data.get('population') if validated_data.get(
            'population') is not None else instance.population
        instance.cities_count = validated_data.get('cities_count') if validated_data.get(
            'cities_count') is not None else instance.cities_count
        instance.save()
        return instance


class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


