# Generated by Django 4.2.3 on 2023-09-28 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0030_alter_delivery_address_alter_delivery_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='bro_delivery_app.address'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='bro_delivery_app.customer'),
        ),
    ]
