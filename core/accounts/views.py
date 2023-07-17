from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Account
from .serializers import UserSerializer, UserSerializerWithToken, AccountSerializer, LogoutSerializer, \
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, EmailVerificationSerializer, RegisterSerializer, \
    LoginSerializer, AccountSubSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, permissions, views, filters

from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.http import HttpResponsePermanentRedirect
import os
import jwt
from django.conf import settings
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
import django_filters
# from django.contrib.sites.models import Site
from django.db.models import Q


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class Accountuser(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountSubUser(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSubSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # permission_classes = [IsCompanyUser]

    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        #### For the Setting the cookies in the browser ####
        response.set_cookie(key='access_token', value=response.data['token'], httponly=True)

        return response

    def create(self, validated_data):
        return Account.objects.create(**validated_data)


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = Account.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)

        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = Account.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = Account.objects.get(id=pk)
    serializer = AccountSubSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request, pk):
    user = Account.objects.get(id=pk)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    user.avtar = data['avtar']
    user.is_staff = data['isAdmin']
    user.save()
    serializer = AccountSubSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
#@permission_classes([IsAuthenticated])
def updateUserAvtar(request, pk):
    user = Account.objects.get(id=pk)
    data = request.data
    user.avtar = data['avtar']
    user.save()
    serializer = AccountSubSerializer(user, many=False)
    return Response({'Message': 'Avtar update successfully'})


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    userForDeletion = Account.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = Account.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = Account.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            # current_site = Site.objects.get_current().domain
            print(current_site)
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relativeLink
            # http: // localhost: 3000 / reset / password /: id
            # absurl = 'http://' + 'localhost:3000/reset/password/' + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         absurl + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'unsuccessful': 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListView(generics.ListAPIView):
    serializer_class = AccountSubSerializer
    queryset = Account.objects.all()
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    filter_backends = [filters.SearchFilter]
    search_fields = ['department', 'first_name', 'last_name', 'location']

    def _queryfy(self, search_terms=None, department_terms=None, location_terms=None):
        if search_terms and department_terms and location_terms:
            return Account.objects.filter(
                (Q(first_name__icontains=search_terms) | Q(last_name__icontains=search_terms)) & Q(department__icontains=department_terms) & Q(
                    location__icontains=location_terms))

        elif search_terms and department_terms:
            return Account.objects.filter(
                (Q(first_name__icontains=search_terms) | Q(last_name__icontains=search_terms))  & Q(department__icontains=department_terms))

        elif search_terms and location_terms:
            return Account.objects.filter((Q(first_name__icontains=search_terms) | Q(last_name__icontains=search_terms))  & Q(location__icontains=location_terms))

        elif search_terms and location_terms:
            return Account.objects.filter(
                Q(department__icontains=department_terms) & Q(location__icontains=location_terms))

        elif search_terms:
            return Account.objects.filter(Q(first_name__icontains=search_terms) | Q(last_name__icontains=search_terms))

        elif department_terms:
            return Account.objects.filter(department__icontains=department_terms)

        elif location_terms:
            return Account.objects.filter(location__icontains=location_terms)

        else:
            return Account.objects.all()

    # if not search_terms and not department_terms and not location_terms:
    def get_queryset(self):
        queryset = Account.objects.all()
        search_terms = self.request.query_params.get('user', None)
        department_terms = self.request.query_params.get('department', None)
        location_terms = self.request.query_params.get('location', None)
        queryset = self._queryfy(search_terms, department_terms, location_terms)
        return queryset

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = AccountSubSerializer
#     pagination_class = PageNumberPagination
#     pagination_class.page_size = 1

# @permission_classes([IsAuthenticated])
# class UserListView(generics.ListAPIView):
#     serializer_class = AccountSubSerializer
#     queryset = Account.objects.all()
#     pagination_class = PageNumberPagination
#     pagination_class.page_size = 2
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['department', 'first_name', 'location']
#
#     def get_queryset(self):
#         queryset = Account.objects.all()
#         search_terms = self.request.query_params.get('search', None)
#         department_terms = self.request.query_params.get('department', None)
#         location_terms = self.request.query_params.get('location', None)
#         if search_terms or department_terms or location_terms:
#             queryset = queryset.filter(
#                 Q(first_name__icontains=search_terms) |
#                 Q(department__icontains= department_terms) |
#                 Q(location__icontains= location_terms)
#             )
#
#         return queryset

# class EmployeeFilter(django_filters.FilterSet):
#     #fullname = django_filters.CharFilter(lookup_expr='icontains')
#     department = django_filters.CharFilter(lookup_expr='icontains')
#     location = django_filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = Account
#         fields = ['department', 'location']
#
#
# class UserListView(generics.ListAPIView):
#     serializer_class = AccountSubSerializer
#     queryset = Account.objects.all()
#     pagination_class = PageNumberPagination
#     pagination_class.page_size = 2
#     filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
#     filter_class = EmployeeFilter
#     #search_fields = ['department', 'location']
