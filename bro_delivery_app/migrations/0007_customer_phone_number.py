# Generated by Django 4.2.3 on 2023-08-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0006_remove_customer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(default=0),
            preserve_default=False,
        ),
    ]