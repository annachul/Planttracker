
from __future__ import annotations
from distutils.command.upload import upload

from typing import Union, Optional, Tuple

from django.db import models
from django.db.models import QuerySet, Manager
from django.db.models.fields import DateField, IntegerField
from django.db.models.fields.related import ForeignKey
from django.db.models import Avg


from django.utils.timezone import datetime
from datetime import datetime, timedelta

import string

def upload_to(instance, filename):
    print(filename)
    return 'post/{filename}'.format(filename=filename)



class Plants(models.Model):
    id = models.BigAutoField(primary_key=True)
    plantname = models.CharField(max_length=300)
    ligth = models.FloatField(null=True)
    spot = models.FloatField(null=True)
    watersum = models.IntegerField(null=True)
    waterwin = models.IntegerField(null=True)
    lastwater = models.DateField(null=True)
    feedsum = models.IntegerField(null=True)
    feedwin = models.IntegerField(null=True)
    lastfeed = models.DateField(null=True)
    poting = models.IntegerField(null=True)
    lastpot = models.DateField(null=True)
    warm = models.IntegerField(null=True)
    lastwarm = models.DateField(null=True)
    clean = models.IntegerField(null=True)
    lastclean = models.DateField(null=True)
    spark = models.IntegerField(null=True)
    lastspark = models.DateField(null=True)
    soil = models.CharField(max_length=500, null=True)
    add = models.CharField(max_length=500, null=True)
    status = models.CharField(max_length=10, null=True)
    pot = models.IntegerField(null=True)
    image=models.ImageField(null=True, upload_to=upload_to)
    hard=models.CharField(max_length=10, null=True)


    def __str__(self):
        return f'{self.plantname} - {self.id}'




class ImageUpload(models.Model):
    id = models.BigAutoField(primary_key=True)
    plantimage = models.ImageField(null=True, upload_to=upload_to)

