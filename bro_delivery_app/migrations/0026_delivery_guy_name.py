# Generated by Django 4.2.3 on 2023-09-25 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0025_restaurant_name_alter_delivery_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_guy',
            name='name',
            field=models.CharField(default='none'),
        ),
    ]