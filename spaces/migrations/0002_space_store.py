# Generated by Django 3.2.7 on 2021-09-26 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('spaces', '0001_initial'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='space',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_spaces', to='stores.store'),
        ),
    ]
