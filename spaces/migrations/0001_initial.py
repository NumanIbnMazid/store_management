# Generated by Django 3.2.7 on 2021-09-26 11:50

from django.db import migrations, models
import django.db.models.deletion
import utils.image_upload_helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('image_1', models.ImageField(blank=True, null=True, upload_to=utils.image_upload_helper.upload_space_image_path)),
                ('image_1_reference', models.CharField(blank=True, max_length=254, null=True)),
                ('image_1_comment', models.CharField(blank=True, max_length=254, null=True)),
                ('image_2', models.ImageField(blank=True, null=True, upload_to=utils.image_upload_helper.upload_space_image_path)),
                ('image_2_reference', models.CharField(blank=True, max_length=254, null=True)),
                ('image_2_comment', models.CharField(blank=True, max_length=254, null=True)),
                ('image_3', models.ImageField(blank=True, null=True, upload_to=utils.image_upload_helper.upload_space_image_path)),
                ('image_3_reference', models.CharField(blank=True, max_length=254, null=True)),
                ('image_3_comment', models.CharField(blank=True, max_length=254, null=True)),
                ('image_4', models.ImageField(blank=True, null=True, upload_to=utils.image_upload_helper.upload_space_image_path)),
                ('image_4_reference', models.CharField(blank=True, max_length=254, null=True)),
                ('image_4_comment', models.CharField(blank=True, max_length=254, null=True)),
                ('image_5', models.ImageField(blank=True, null=True, upload_to=utils.image_upload_helper.upload_space_image_path)),
                ('image_5_reference', models.CharField(blank=True, max_length=254, null=True)),
                ('image_5_comment', models.CharField(blank=True, max_length=254, null=True)),
                ('equipment_details', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_spaces', to='stores.store')),
            ],
            options={
                'verbose_name': 'Space',
                'verbose_name_plural': 'Spaces',
                'ordering': ['-created_at'],
            },
        ),
    ]
