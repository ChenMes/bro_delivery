from rest_framework import serializers

from bro_delivery_app.models import Delivery, Restaurant, Delivery_guy, Address


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    model = Restaurant
    field = '__all__'


class Delivery_guySerializer(serializers.ModelSerializer):
    model = Delivery_guy
    field = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    model = Address
    field = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    model = Address
    field = '__all__'


class TipSerializer(serializers.ModelSerializer):
    model = Address
    field = '__all__'
