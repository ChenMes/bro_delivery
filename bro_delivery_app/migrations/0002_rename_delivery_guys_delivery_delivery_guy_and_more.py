# Generated by Django 4.2.3 on 2023-08-09 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bro_delivery_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='delivery_guys',
            new_name='delivery_guy',
        ),
        migrations.AddField(
            model_name='delivery',
            name='spacial_comment',
            field=models.TextField(db_column='spacial_comment', null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='tip',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='restaurant', to='bro_delivery_app.restaurant'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='phone_number',
            field=models.CharField(),
        ),
        migrations.DeleteModel(
            name='Tip',
        ),
    ]
