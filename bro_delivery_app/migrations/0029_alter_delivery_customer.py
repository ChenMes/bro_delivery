# Generated by Django 4.2.3 on 2023-09-26 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0028_alter_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='bro_delivery_app.customer'),
        ),
    ]
