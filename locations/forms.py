from django import forms

from .models import Country, City, Flag

class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        exclude = ('flag', 'user',)

class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = '__all__'

class FlagForm(forms.ModelForm):

    class Meta:
        model = Flag
        fields = '__all__'