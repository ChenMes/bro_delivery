# Generated by Django 4.2.3 on 2023-08-26 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0021_alter_delivery_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='restaurant', to='bro_delivery_app.restaurant'),
        ),
    ]