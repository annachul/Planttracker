# Generated by Django 3.2.8 on 2022-05-19 09:35

from django.db import migrations, models
import plants.models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0003_auto_20220518_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plants',
            name='image',
            field=models.ImageField(default='media/default.jpg', null=True, upload_to=plants.models.upload_to),
        ),
    ]