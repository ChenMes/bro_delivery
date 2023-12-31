# Generated by Django 4.2.3 on 2023-08-09 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bro_delivery_app', '0004_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(default='משלוח חדש', max_length=20),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='delivery_guy',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
    ]
