# Generated by Django 4.2.3 on 2023-09-02 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0023_alter_customer_addresses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
