import jwt
from django.contrib.auth import user_logged_in
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_jwt.serializers import jwt_payload_handler
from django_learn import settings
from locations_api.serializers import CountrySerializer, CitySerializer, UserSerializer
from locations.models import Country, City
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
import django_filters.rest_framework
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from locations_api.tasks import country_created, country_chanched

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
            task = country_created.delay("stas22.08.2004@gmail.com")
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
            task = country_chanched.delay(request.user.email)
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
        return Response(status=status.HTTP_204_NO_CONTENT)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]




class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserVievSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):

    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (
                    user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)