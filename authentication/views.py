import jwt, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny 
from .serializers import UserSerializer
from .models import User
from .token import account_activation_token

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated request')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated request')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'successfully signed out!'
        }
        return response

class ActivateAccount(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("<h3>Account is activated successfully. Please login to your account <a href='https://www.profile11.tk/login'>here</a></h3>")
        else:
            return HttpResponse('<h3>Invalid activation link</h3>')

# class ProfilesList(APIView):
#     def get(self, request):
#         # token = request.COOKIES.get('jwt')
 
#         # if not token:
#         #     raise AuthenticationFailed('Unauthenticated request')


#         profiles = People.objects.filter(public = True)
#         serializer = PeopleSerializer(profiles, many=True)
#         return Response(serializer.data)

# class ProfileCreate(APIView):
#     def post(self, request, format=None):
#         serializer = PeopleSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,
#                             status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProfileDetailView(APIView):
#     serializer = PeopleSerializer
#     def get_queryset(self):
#         profiles = People.objects.all()
#         return profiles
    
#     def destroy(self, request, *args, **kwargs):
#         id = request.query_params['id']
#         profile = People.objects.get(id=id)
#         profile.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT) 

    # permission_classes = (IsAuthenticated,)
    # def get_object(self, pk):
    #     try:
    #         return People.objects.get(pk=pk)
    #     except Transformer.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     profile = self.get_object(pk)
    #     serializers = PeopleSerializer(profile)
    #     return Response(serializer.data)

    # def delete(request, pk):
    #     profile = self.get_object(pk)
    #     profile.delete()
    #     return HttpResponse(status=status.HTTP_204_NO_CONTENT)


    
