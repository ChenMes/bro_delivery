# Generated by Django 4.2.3 on 2023-08-10 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bro_delivery_app', '0011_remove_delivery_guy_vehicle_remove_restaurant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]