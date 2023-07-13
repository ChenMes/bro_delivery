from django.db import models


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    phone_number = models.IntegerField(null=False, blank=False)
    address = models.ForeignKey('Address', on_delete=models.RESTRICT)
    customers = models.ManyToManyField('Customer')

    class Meta:
        db_table = 'restaurant'


class Delivery(models.Model):
    preparation_time = models.PositiveIntegerField(null=True, blank=True,)
    arrival_time = models.DateTimeField(null=False, blank=False)
    time_left = models.IntegerField(null=False, blank=False)
    time_late = models.IntegerField(null=True, blank=True)
    payment = models.BooleanField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    address = models.ForeignKey('Address', on_delete=models.RESTRICT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.RESTRICT)
    delivery_guys = models.ForeignKey('Delivery_guy', on_delete=models.RESTRICT)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'delivery'


class Delivery_guy(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    phone_number = models.IntegerField(null=False, blank=False)
    vehicle = models.CharField(null=True, blank=True, max_length=20)

    class Meta:
        db_table = 'delivery_guy'


class Address(models.Model):
    building_type = models.BooleanField(null=True, blank=True)
    street = models.CharField(null=False, blank=False, max_length=20)
    number = models.PositiveIntegerField(null=False, blank=False)
    enter = models.CharField(null=True, blank=True, max_length=5)
    floor = models.PositiveIntegerField(null=True, blank=True)
    appartement = models.PositiveIntegerField(null=True, blank=True)
    password = models.CharField(null=True, blank=True, max_length=20)
    spacial_comment = models.TextField(db_column='spacial_comment', null=True, blank=True)
    customers = models.ManyToManyField('Customer')

    class Meta:
        db_table = 'address'


class Customer(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    phone_number = models.IntegerField(null=False, blank=False)
    avg_tip = models.IntegerField(null=True, blank=True)
    addresses = models.ManyToManyField('Address')
    restaurants = models.ManyToManyField('Restaurant')

    class Meta:
        db_table = 'customer'


class Tip(models.Model):
    tip = models.IntegerField(null=False, blank=False)
    spacial_comment = models.TextField(db_column='spacial_comment', null=True,)
    delivery_guy = models.ForeignKey(Delivery_guy, on_delete=models.RESTRICT)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)

    class Meta:
        db_table = 'tip'
