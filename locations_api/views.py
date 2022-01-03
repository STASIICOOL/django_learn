from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from locations_api.serializers import CountrySerializer
from locations.models import Country
from rest_framework import status
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry endpoint of our API.
    """
    return Response({
        'users': 'endpointtowork',
    })


# Create your views here.


class CountryList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self):
        countries = Country.objects.all()
        return countries

    def get(self, request, *args, **kwargs):
        countries = self.get_queryset()
        serializer = self.serializer_class(countries, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CountryDell(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def get_queryset(self, country_id):
        try:
            country = get_object_or_404(Country, id=country_id)
        except country.DoesNotExist:
            content = {
                "status" : "not found"
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return country

    def get(self, request, country_id):
        country = self.get_queryset(country_id)
        serializer = self.serializer_class(country)
        return Response(serializer.data)

    def put(self, request, country_id):
        country = self.get_queryset(country_id)
        serializer = self.serializer_class(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    def patch(self, request, country_id):
        country = self.get_queryset(country_id)
        serializer = self.serializer_class(country, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, country_id):
        country = self.get_queryset(country_id)
        country.delete()
        return Response(self.content, status=status.HTTP_204_NO_CONTENT)
