from django.http import request
from rest_framework import serializers
from .models import Plants, ImageUpload


class PlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields = ('id' ,'plantname', 'ligth', 'spot','watersum' ,'waterwin', 'lastwater', 'feedsum','feedwin','lastfeed','poting','lastpot','warm','lastwarm','clean','lastclean','spark', 'lastspark', 'soil','add', 'status', 'pot','image','hard')
        
class PlantsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields = ('id' ,'plantname', 'ligth', 'spot','watersum' ,'waterwin', 'lastwater', 'feedsum','feedwin','lastfeed','poting','lastpot','warm','lastwarm','clean','lastclean','spark', 'lastspark', 'soil','add', 'status', 'pot','image','hard')
        

        
class StatusGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Plants
        fields = ('id' , 'status')
        