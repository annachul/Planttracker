# Generated by Django 3.2.8 on 2022-05-19 11:54

from django.db import migrations, models
import plants.models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0004_alter_plants_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='image',
            field=models.ImageField(null=True, upload_to=plants.models.upload_to),
        ),
    ]