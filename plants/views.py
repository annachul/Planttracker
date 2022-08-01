

from email.mime import image
from xml.dom import minicompat
from django.shortcuts import render
from .serializers import PlantsSerializer, StatusGetSerializer
from .models import Plants,PlantTasks    
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from datetime import date,datetime, timedelta
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch 
from reportlab.lib.pagesizes import letter 
import redis


  
r = redis.Redis(host='localhost', port=6379, db=0) 
      

class PlantId(APIView):  
    serializer_class = StatusGetSerializer
    def patch(self, request, id, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            querysetid = Plants.objects.filter(id=id)
            if querysetid.exists():
                plant = querysetid[0]
                plant.status=serializer.validated_data.get('status')
                plant.save(update_fields=['status'])
                if plant.status=="dead":
                    plant.delete_all_active_tasks()
                r.delete(f"{id}_plant")
        return Response({'Good Request': 'Ok'})

    def delete(self, request, id, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            querysetid = Plants.objects.filter(id=id)
            if querysetid.exists():
                plant = querysetid[0]
                plant.delete()
        return Response({'Good Request': 'Ok'})
    def get(self, request, id, format=None):
        plantdata=r.get(f"{id}_plant")
        
        if plantdata is None:
            plant=Plants.objects.get(id=id)
            plantdata={
                'id':plant.id,
                'plantname':plant.plantname,
                'ligth':plant.ligth,
                'spot':plant.spot,
                'watersum':plant.watersum,
                'waterwin':plant.waterwin,
                'lastwater':plant.lastwater,
                'feedsum':plant.feedsum,
                'feedwin':plant.feedwin,
                'lastfeed':plant.lastfeed,
                'poting':plant.poting,
                'lastpot':plant.lastpot,
                'warm':plant.warm,        
                'lastwarm':plant.lastwarm,           
                'clean':plant.clean,   
                'lastclean':plant.lastclean,   
                'spark':plant.spark,  
                'lastspark':plant.lastspark, 
                'soil':plant.soil,   
                'add':plant.add,   
                'status':plant.status,  
                'pot':plant.pot, 
                'hard':plant.hard
                }
            r.set(f"{id}_plant", json.dumps(plantdata, default=str))
            r.expire(f"{id}_plant", timedelta(minutes=10))
        else:
            plantdata=json.loads(plantdata.decode('utf-8'))
        plantdatalist=[]
        plantdatalist.append(plantdata)
            
        return JsonResponse(plantdatalist, safe=False)

    def put(self, request, id, format=None):
        request=request.body.decode('utf-8')
        request=json.loads(request)
        
        plant = Plants.objects.get(id=id)
        if plant.watersum != request['watersum'] or plant.waterwin != request['waterwin'] or plant.lastwater != request['lastwater']:
            plant.watersum = int(request['watersum'])
            plant.waterwin = int(request['waterwin'])
            if plant.lastwater:
                plant.lastwater = datetime.strptime(request['lastwater'], '%Y-%m-%d')
                plant.delete_and_create_water_task()
            plant.save()
        if plant.feedsum != request['feedsum'] or plant.feedwin != request['feedwin'] or plant.lastfeed != request['lastfeed']:
            plant.feedsum = int(request['feedsum'])
            plant.feedwin = int(request['feedwin'])
            if plant.lastfeed:
                plant.lastfeed = datetime.strptime(request['lastfeed'], '%Y-%m-%d')
                plant.delete_and_create_feed_task()
            plant.save()
        if plant.poting != request['poting'] or plant.lastpot != request['lastpot']:
            plant.poting = int(request['poting'])
            if plant.lastpot:
                plant.lastpot = datetime.strptime(request['lastpot'], '%Y-%m-%d')
                plant.delete_and_create_poting_task()
            plant.save()
        if plant.warm != request['warm'] or plant.lastwarm != request['lastwarm']:
            plant.warm = int(request['warm'])
            if plant.lastwarm:
                plant.lastwarm = datetime.strptime(request['lastwarm'], '%Y-%m-%d')
                plant.delete_and_create_warm_task()
            plant.save()
        if plant.clean != request['clean'] or plant.lastclean != request['lastclean']:
            plant.clean = int(request['clean'])
            if plant.lastclean:
                plant.lastclean = datetime.strptime(request['lastclean'], '%Y-%m-%d')
                plant.delete_and_create_clean_task()
            plant.save()
        if plant.spark != request['spark'] or plant.lastspark != request['lastspark']:
            plant.spark = int(request['spark'])
            if plant.lastspark:
                plant.lastspark = datetime.strptime(request['lastspark'], '%Y-%m-%d')
                plant.delete_and_create_spark_task()
            plant.save()
        plant.ligth = int(request['ligth'])
        plant.spot = request['spot']
        plant.soil = request['soil']
        plant.add = request['add']
        plant.status = request['status']
        plant.pot = request['pot']
        plant.hard = request['hard']
        plant.save()
        r.delete(f"{id}_plant")
        return Response({'Good Request': 'Ok'})




class TodoView(APIView):  
    serializer_class = PlantsSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            plant=serializer.save()
            if plant.status=="list":
                plant.create_tasks()
        return Response({'Good Request': 'Ok'})
    def get(self, request, format=None):
        serializer_class = PlantsSerializer
        plants=Plants.objects.all()
        plantdata=[]
        for plant in plants:
            image=""
            if plant.image:
                image=plant.image.url
            plantdata.append({
                'id':plant.id,
                'plantname':plant.plantname,
                'ligth':plant.ligth,
                'spot':plant.spot,
                'watersum':plant.watersum,
                'waterwin':plant.waterwin,
                'lastwater':plant.lastwater,
                'feedsum':plant.feedsum,
                'feedwin':plant.feedwin,
                'lastfeed':plant.lastfeed,
                'poting':plant.poting,
                'lastpot':plant.lastpot,
                'warm':plant.warm,        
                'lastwarm':plant.lastwarm,           
                'clean':plant.clean,   
                'lastclean':plant.lastclean,   
                'spark':plant.spark,  
                'lastspark':plant.lastspark, 
                'soil':plant.soil,   
                'add':plant.add,   
                'status':plant.status,  
                'pot':plant.pot, 
                'hard':plant.hard,
                'image':image
                })


        return JsonResponse(plantdata, safe=False)




class PlantTask(APIView):  
    def get(self, request, format=None):
        datetaday=date.today()
        tasks=PlantTasks.objects.filter(done=request.GET.get('done', False)).filter(duedate__lte=request.GET.get('duedate',datetaday))
        if request.GET.get('plantname'):
            plantid=Plants.objects.get(plantname=request.GET.get('plantname'))
            tasks=tasks.filter(plantid=plantid)
        if request.GET.get('type'):
            tasks=tasks.filter(type=request.GET.get('type'))

        planttasksdata=[]
        for task in tasks:
            try:
                plant=Plants.objects.get(id=task.plantid.id)
                planttasksdata.append({
                'id':task.id,
                'description':task.description,
                'type':task.type,
                'duedate':task.duedate,
                'done':task.done,
                'plantname': task.plantid.plantname,
                'pot':plant.pot,
                'soil':plant.soil})
            except:
                planttasksdata.append({
                'id':task.id,
                'description':task.description,
                'type':task.type,
                'duedate':task.duedate,
                'done':task.done})

        return JsonResponse(planttasksdata, safe=False)
    
    def post(self, request, format=None):
        request=request.body.decode('utf-8')
        request=json.loads(request)
        if request['plantname']:
            plant=Plants.objects.get(plantname=request['plantname'])
            plantid=plant
            description=request['description']
            type=request['type']
            duedate=request['duedate']
            task=PlantTasks(description=description, type=type, duedate=duedate, plantid=plantid)
        else:
            description=request['description']
            type=request['type']
            duedate=request['duedate']
            task=PlantTasks(description=description, type=type, duedate=duedate)
        task.save()
        return Response({'Good Request': 'Ok'})



@csrf_exempt
@transaction.atomic
def TaskDone(request,id):
    request=request.body.decode('utf-8')
    request=json.loads(request)
    tasks=PlantTasks.objects.all()
    taskselect = PlantTasks.objects.get(id=id)
    taskselect.done=True
    taskselect.actualdate=date.today()
    taskselect.save()
    taskselect.taskdone()
    
    planttasksdata=[]
    for task in tasks:
        if task.done==False:
            try:
                planttasksdata.append({
                'id':task.id,
                'description':task.description,
                'type':task.type,
                'duedate':task.duedate,
                'done':task.done,
                'plantname': task.plantid.plantname})
            except:
                planttasksdata.append({
                'id':task.id,
                'description':task.description,
                'type':task.type,
                'duedate':task.duedate,
                'done':task.done})

    return JsonResponse(planttasksdata, safe=False)

class TaskId(APIView):
    def delete(self, request, id, format=None):
        task = PlantTasks.objects.get(id=id)
        if task:
            task.delete()
        return Response({'Good Request': 'Ok'})


@csrf_exempt
def ImageUpload(request,id):
    plant=Plants.objects.get(id=id)
    plant.image=request.FILES.get('image')
    r.delete(f"{id}_plant")
    plant.save()
    return JsonResponse({}, safe=False)


def pdfexport(request,id):
    
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize = letter, bottomup=0.1)
    plant=Plants.objects.get(id=id)


    img_file=plant.image.path

    plantname="Plant name: "+ plant.plantname
    plantlight="Level of light: " +str(plant.ligth)
    plantwatersum="Watering in summer time:  every: "+str(plant.watersum)+ " days"
    plantwaterwin="Watering in winter time: every: "+str(plant.waterwin)+ " days"
    plantfeedsum="Feeding in summer time: every "+str(plant.feedsum)+ " days"
    plantfeedwin="Feeding in winter time: every "+str(plant.feedwin)+ " days"
    plantsoil= "Soil: " +str(plant.soil)
    plantpot = "Radius of the pot: "+ str(plant.pot)
    planthard= "Difficulty level "+ str(plant.hard)

    lines= [
    plantname,
    plantlight,
    plantwatersum,
    plantwaterwin,
    plantfeedsum,
    plantfeedwin,
    plantsoil,
    planthard,
    plantpot
    ]

    if plant.warm:
        plantwarm= "Warm bath: every "+str(plant.warm)+ " days"
        lines.append(plantwarm)

    if plant.clean:
        plantclean= "Cleaning: every "+str(plant.clean)+ " days"
        lines.append(plantclean)

    if plant.spark:
        plantspark= "Spraying: every "+str(plant.spark)+ " days"
        lines.append(plantspark)

    if plant.add:
        plantadd= "Comments: "+str(plant.add)
        lines.append(plantadd)
    
    


    textob=p.beginText(0,0)
    textob.setTextOrigin(50,720)
    textob.setFont('Helvetica', 14)

    for line in lines:
        textob.textLine(line)

    p.drawText(textob)
    p.drawImage(img_file,400,500, 150,300, preserveAspectRatio=True, mask='auto')
    
    avgsumwater=plant.count_average_sumwater()
    avgwinwater=plant.count_average_winwater()
    avgsumfeed=plant.count_average_sumfeed()
    avgwinfeed=plant.count_average_winfeed()
    avgwarm=plant.count_average_warm()
    avgclean=plant.count_average_clean()
    avgspark=plant.count_average_spark()
    stats=[]
    if avgsumwater:
        stats.append(avgsumwater)
    if avgwinwater:
        stats.append(avgwinwater)
    if avgsumfeed:
        stats.append(avgsumfeed)
    if avgwinfeed:
        stats.append(avgwinfeed)
    if avgwarm:
        stats.append(avgwarm)
    if avgclean:
        stats.append(avgclean)
    if avgspark:
        stats.append(avgspark)

    statob=p.beginText(0,0)
    statob.setTextOrigin(50,420)
    statob.setFont('Helvetica', 14)
    for stat in stats:
        statob.textLine(stat)
    p.drawText(statob)

    p.showPage()
    p.save()

   
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')