from django.contrib.auth.models import User
from django.db import models


# Create your models here
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='restaurant')
    phone_number = models.CharField(null=False, blank=False)
    address = models.ForeignKey('Address', on_delete=models.RESTRICT, null=True, blank=True)
    customers = models.ManyToManyField('Customer')

    class Meta:
        db_table = 'restaurant'


class Delivery(models.Model):
    status = models.CharField(null=True, blank=False, default='משלוח חדש', max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    preparation_time = models.PositiveIntegerField(null=True, blank=True)
    payment = models.BooleanField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    address = models.ForeignKey('Address', on_delete=models.RESTRICT, null=True, blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.RESTRICT, related_name='restaurant',
                                   null=True, blank=False)
    delivery_guy = models.ForeignKey('Delivery_guy', on_delete=models.RESTRICT, null=True, blank=True)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT, null=True, blank=True)
    tip = models.IntegerField(null=True, blank=True)
    spacial_comment = models.TextField(null=True, blank=True, db_column='spacial_comment')

    class Meta:
        db_table = 'delivery'


class Delivery_guy(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    phone_number = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'delivery_guy'


class Address(models.Model):
    building_type = models.BooleanField(null=True, blank=True)
    street = models.CharField(null=False, blank=False, max_length=20)
    number = models.PositiveIntegerField(null=False, blank=False)
    enter = models.CharField(null=True, blank=True, max_length=5)
    floor = models.PositiveIntegerField(null=True, blank=True)
    appartement = models.PositiveIntegerField(null=True, blank=True)
    building_password = models.CharField(null=True, blank=True, max_length=20)
    spacial_comment = models.TextField(db_column='spacial_comment', null=True, blank=True)
    customers = models.ManyToManyField('Customer', blank=True)

    class Meta:
        db_table = 'address'


class Customer(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    phone_number = models.CharField(null=False, blank=False, max_length=20)
    avg_tip = models.IntegerField(null=True, blank=True)
    addresses = models.ManyToManyField('Address', blank=False)
    restaurants = models.ManyToManyField('Restaurant', blank=True)

    class Meta:
        db_table = 'customer'

