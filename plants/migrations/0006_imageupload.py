# Generated by Django 3.2.8 on 2022-05-22 12:40

from django.db import migrations, models
import plants.models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0005_alter_plants_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plantimage', models.ImageField(null=True, upload_to=plants.models.upload_to)),
            ],
        ),
    ]