# Generated by Django 3.2.7 on 2021-09-26 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Open'), (1, 'Closed')], default=0)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=254, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=30, null=True)),
                ('about', models.TextField(blank=True, max_length=2000, null=True)),
                ('linkedin', models.URLField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, max_length=254, null=True)),
                ('facebook', models.URLField(blank=True, max_length=254, null=True)),
                ('instagram', models.URLField(blank=True, max_length=254, null=True)),
                ('twitter', models.URLField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studio_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Studio',
                'verbose_name_plural': 'Studios',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='StudioModerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('contact', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=254, null=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('studio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Studio', to='studios.studio')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='studio_moderator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'StudioModerator',
                'verbose_name_plural': 'StudioModerators',
                'ordering': ['-created_at'],
            },
        ),
    ]