# Generated by Django 3.2.8 on 2022-05-11 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plants',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('plantname', models.CharField(max_length=300)),
                ('ligth', models.FloatField(null=True)),
                ('spot', models.FloatField(null=True)),
                ('watersum', models.IntegerField(null=True)),
                ('waterwin', models.IntegerField(null=True)),
                ('lastwater', models.DateField(null=True)),
                ('feedsum', models.IntegerField(null=True)),
                ('feedwin', models.IntegerField(null=True)),
                ('lastfeed', models.DateField(null=True)),
                ('poting', models.IntegerField(null=True)),
                ('lastpot', models.DateField(null=True)),
                ('warm', models.IntegerField(null=True)),
                ('lastwarm', models.DateField(null=True)),
                ('clean', models.IntegerField(null=True)),
                ('lastclean', models.DateField(null=True)),
                ('spark', models.IntegerField(null=True)),
                ('lastspark', models.DateField(null=True)),
                ('soil', models.CharField(max_length=500)),
                ('add', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=10)),
                ('pot', models.IntegerField(null=True)),
            ],
        ),
    ]
