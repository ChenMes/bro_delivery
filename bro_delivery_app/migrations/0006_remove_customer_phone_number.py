# Generated by Django 4.2.3 on 2023-08-09 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0005_alter_customer_phone_number_alter_delivery_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone_number',
        ),
    ]