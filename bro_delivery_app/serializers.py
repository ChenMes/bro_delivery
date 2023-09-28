from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from bro_delivery_app.models import Delivery, Restaurant, Delivery_guy, Address, Customer, Restaurant


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        restaurant = Restaurant.objects.get(user_id=user.id)
        address = Address.objects.get(id=request.data['address'])
        deliveryDict = dict(request.data)
        del deliveryDict['address']

        # Create Delivery instance
        delivery = Delivery.objects.create(restaurant=restaurant,address=address, **deliveryDict)

        return delivery

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user
        delivery_guy = Delivery_guy.objects.get(user_id=user.id)

        # Update only the 'delivery_guy' field of the instance
        instance.delivery_guy = delivery_guy
        instance.status = 'מצורף לשליח'

        # Save the updated instance to the database
        instance.save()
        print(instance, delivery_guy)

        return instance


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class Delivery_guySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_guy
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        user_repr = super().to_representation(instance)
        return user_repr

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        depth = 1
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        user = User(
            email=self.validated_data["email"],
            username=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"]
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()
        return user


class CreateCustomerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'avg_tip', 'addresses']
        depth = 1

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')  # Pop addresses data

        with transaction.atomic():
            customer = Customer.objects.create(
                name=validated_data['name'],
                phone_number=validated_data['phone_number'],
                avg_tip=validated_data.get('avg_tip')
            )

            for address_data in addresses_data:
                customer.addresses.create(**address_data)  # Create addresses

        return customer


class CreateUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=20, write_only=True)
    is_restaurant = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'is_restaurant', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        validators = [UniqueTogetherValidator(User.objects.all(), ['email'])]
        depth = 1

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')  # pop phone number
        is_restaurant = validated_data.pop('is_restaurant')  # pop is_restaurant
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''))

        if is_restaurant:  # is_restaurant True
            restaurant = Restaurant.objects.create(user=user, phone_number=phone_number)  # create user Restaurant
            # return restaurant
        else:  # is_restaurant False
            delivery_guy = Delivery_guy.objects.create(user=user, phone_number=phone_number)  # create user Delivery_guy
            # return delivery_guy
        return user


class ExtendedTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        return obj
