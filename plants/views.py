

from django.shortcuts import render
from .serializers import PlantsSerializer, PlantsGetSerializer, StatusGetSerializer
from rest_framework import viewsets      
from .models import Plants    
from rest_framework import serializers
from django.core import serializers
from django.http import StreamingHttpResponse, request
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

  
 
      

class StatusSerializer(APIView):  
    serializer_class = StatusGetSerializer
    queryset = Plants.objects.all()
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id=serializer.data.get('id')
            querysetid = Plants.objects.filter(id=serializer.data.get('id'))
            if querysetid.exists():
                plant = querysetid[0]
                plant.status=serializer.validated_data.get('status')
                plant.save(update_fields=['status'])
        return Response({'Good Request': 'Ok'})
    

class DeleteSerializer(APIView):  
    serializer_class = StatusGetSerializer
    queryset = Plants.objects.all()
    def delete(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id=serializer.data.get('id')
            querysetid = Plants.objects.filter(id=serializer.data.get('id'))
            if querysetid.exists():
                plant = querysetid[0]
                plant.delete()
        return Response({'Good Request': 'Ok'})




class TodoView(APIView):  
    serializer_class = PlantsSerializer
    # parser_classes = [MultiPartParser, FormParser]
    print(request)
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        queryset = Plants.objects.all()
        if serializer.is_valid():
                serializer.save()
            # plantname = serializer.data.get('plantname')
            # ligth = serializer.data.get('ligth')
            # spot = serializer.data.get('spot')
            # watersum = serializer.data.get('watersum')
            # waterwin = serializer.data.get('waterwin')
            # lastwater=serializer.data.get('lastwater')
            # feedsum=serializer.data.get('feedsum')
            # feedwin=serializer.data.get('feedwin')
            # lastfeed=serializer.data.get('lastfeed')
            # poting=serializer.data.get('poting')
            # lastpot=serializer.data.get('lastpot')
            # warm=serializer.data.get('warm')
            # lastwarm=serializer.data.get('lastwarm')
            # clean=serializer.data.get('clean')
            # lastclean=serializer.data.get('lastclean')
            # spark=serializer.data.get('spark')
            # lastspark=serializer.data.get('lastspark')
            # soil=serializer.data.get('soil')
            # add=serializer.data.get('add')
            # status=serializer.data.get('status')
            # pot=serializer.data.get('pot')
            # image=serializer.data.get('image')
            # hard=serializer.data.get('hard')
            # plant=Plants (plantname=plantname, ligth=ligth, spot=spot, watersum=watersum, waterwin=waterwin, lastwater=lastwater, feedsum=feedsum,feedwin=feedwin, lastfeed=lastfeed, poting=poting, lastpot=lastpot, warm=warm, lastwarm=lastwarm, clean=clean, lastclean=lastclean, spark=spark, lastspark=lastspark, soil=soil,add=add, status=status, pot=pot, image=image, hard=hard)
            # plant.save()
        return Response({'Good Request': 'Ok'})


class PlantView(ModelViewSet):
    serializer_class = PlantsGetSerializer
    queryset = Plants.objects.all()