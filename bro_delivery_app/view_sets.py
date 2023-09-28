import os
import uuid
from pprint import pprint

from django.contrib.auth.models import User
from django.http import JsonResponse
from google.auth.transport import requests
from google.cloud import storage
from google.oauth2 import service_account, id_token
from rest_framework import mixins

import django_filters
from django_filters import FilterSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from bro_delivery_app import models
from bro_delivery_app.serializers import *


class DeliveryFilterSet(FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    delivery_guy = django_filters.NumberFilter(field_name='delivery_guy')
    restaurant = django_filters.NumberFilter(field_name='restaurant')

    class Meta:
        model = models.Delivery
        fields = []


class DeliveryPageClass(PageNumberPagination):
    page_size = 20


# class DeliveryPermission(BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user.is_staff or view.action \
#                in ('list', 'retrieve')
#
#     def has_object_permission(self, request, view, obj):
#         return view.action == 'retrieve' or \
#                obj.created_by == request.user


class DeliveryViewSet(ModelViewSet):
    serializer_class = DeliverySerializer
    queryset = Delivery.objects.all()
    pagination_class = DeliveryPageClass
    filterset_class = DeliveryFilterSet
    # permission_classes = [DeliveryPermission]


class RestaurantFilterSet(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='iexact')

    class Meta:
        model = models.Restaurant
        fields = []


class RestaurantPageClass(PageNumberPagination):
    page_size = 5


class RestaurantViewSet(ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = models.Restaurant.objects.all()
    pagination_class = RestaurantPageClass
    filterset_class = RestaurantFilterSet
    # permission_classes =


class CustomerFilterSet(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='iexact')

    class Meta:
        model = models.Customer
        fields = []


class CustomerPageClass(PageNumberPagination):
    page_size = 5


class CustomerViewSet(ModelViewSet):
    serializer_class = CreateCustomerSerializer
    queryset = models.Customer.objects.all()
    pagination_class = CustomerPageClass
    filterset_class = CustomerFilterSet


class UsersViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.restaurant.phone_number,
        }
        return JsonResponse(data)


class AddressFilterSet(FilterSet):

    class Meta:
        model = models.Address
        fields = []


class AddressPageClass(PageNumberPagination):
    page_size = 5


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = models.Address.objects.all()
    pagination_class = AddressPageClass
    filterset_class = AddressFilterSet


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    # you will get here only if the user is already authenticated!
    user_serializer = UserSerializer(instance=request.user, many=False)
    print(request.user)
    return Response(data=user_serializer.data)


class ExtendedTokenObtainPairView(TokenObtainPairView):

    serializer_class = ExtendedTokenObtainPairSerializer


@api_view(['POST'])
def google_login(request):
    google_jwt = request.data['google_jwt']
    CLIENT_ID = '872794659630-ehu55i6a7fbglef45mjno5pgjv7qeab9.apps.googleusercontent.com'
    try:
        idinfo = id_token.verify_oauth2_token(google_jwt, requests.Request(), CLIENT_ID)
        email = idinfo['email']
        try:
            user = User.objects.get(email=email)
            print('user found')
            print(user)

        except User.DoesNotExist:
            print('does not exist')
            user = User.objects.create_user(username=email, email=email, password=str(uuid.uuid4()),
                                            first_name=idinfo['given_name'], last_name=idinfo['family_name'])

        refresh = RefreshToken.for_user(user)
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    except ValueError as e:
        print(e)
    print(google_jwt)
    return Response()


@api_view(['GET'])
def get_address_delivery(request):
    all_addresses = list(Address.objects.order_by().values_list('street').distinct())
    all_addresses = [street for sublist in all_addresses for street in sublist]
    print(all_addresses)
    return JsonResponse(data=list(all_addresses), safe=False)


@api_view(['GET'])
def get_customer_phone(request):
    all_customers = list(Customer.objects.order_by().values_list('phone_number').distinct())
    phones = [phone_number for sublist in all_customers for phone_number in sublist]
    print(phones)
    return JsonResponse(data=list(phones), safe=False)


@api_view(['GET'])
def get_delivery_guy(request):
    user = request.user
    print('user:', user)
    delivery_guy = Delivery_guy.objects.filter(user=user)
    print('delivery_guy:', delivery_guy)
    serializer = Delivery_guySerializer(delivery_guy, many=True)
    return Response(data=serializer.data)


@api_view(['GET'])
def restaurant_deliveries(request):
    user = request.user
    restaurant = Restaurant.objects.filter(user=user).first()  # Use .first() to get a single instance
    deliveries = Delivery.objects.filter(restaurant=restaurant)
    ser = DeliverySerializer(deliveries, many=True)
    return Response(data=ser.data)


@api_view(['GET'])
def delivery_guy_deliveries(request):
    user = request.user
    delivery_guy = Delivery_guy.objects.filter(user=user).first()
    deliveries = Delivery.objects.filter(delivery_guy=delivery_guy)
    ser = DeliverySerializer(deliveries, many=True)
    return Response(data=ser.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_profile_img(request, boto3=None):
#     bucket_name = 'edulabs-flights-profile'
#     file_stream = request.FILES['file'].file
#     _, ext = os.path.splitext(request.FILES['file'].name)
#
#     object_name = f"profile_img_{request.user.id}{ext}"
#
#     try:
#         s3 = boto3.client('s3')
#         # response = s3.upload_file(
#         #         '../requirements.txt', bucket_name, object_name+'.txt')
#         s3.upload_fileobj(file_stream, bucket_name, object_name)
#
#         request.user.profile.img_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
#         request.user.profile.save()
#     except Exception:
#         return Response(status=500)
#
#     return Response()
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_profile_img_url(request, boto3=None):
#     bucket_name = 'edulabs-flights-profile'
#     filename = request.data['filename']
#     _, ext = os.path.splitext(filename)
#
#     object_name = f"profile_img_{request.user.id}_{uuid.uuid4()}{ext}"
#
#     s3 = boto3.client('s3')
#     response = s3.generate_presigned_post(bucket_name, object_name, ExpiresIn=3600)
#     pprint(response)
#
#     # request.user.profile.img_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
#     # request.user.profile.save()
#     return Response(data=response)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_profile_img_done(request, boto3=None):
#     bucket_name = 'edulabs-flights-profile'
#     object_name = request.data['object_name']
#     old_url = request.user.profile.img_url
#
#     request.user.profile.img_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
#     request.user.profile.save()
#
#     s3 = boto3.client('s3')
#
#     old_object_name = old_url.split("/")[-1]
#     s3.delete_object(Bucket='edulabs-flights-profile', Key=old_object_name)
#
#     ser = UserProfileSerializer(request.user)
#     return Response(data=ser.data)
#
#
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_profile_img(request):
#     bucket_name = 'jb-eve'
#     file_stream = request.FILES['file'].file
#     _, ext = os.path.splitext(request.FILES['file'].name)
#
#     object_name = f"profile_img_{uuid.uuid4()}{ext}"
#
#     credentials = service_account.Credentials.from_service_account_file(
#         '/Users/valeria/Documents/keys/jb-eve-service-account-key.json')
#
#     storage_client = storage.Client(credentials=credentials)
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(object_name)
#     blob.upload_from_file(file_stream)
#
#     return Response()
