
from __future__ import annotations


from django.db import models
from django.db.models import QuerySet



from datetime import date, timedelta, datetime
import redis

r = redis.Redis(host='localhost', port=6379, db=0) 

def upload_to(instance, filename):
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

    def delete_all_active_tasks(self):
        tasks=PlantTasks.objects.filter(plantid=self, done="False")
        for task in tasks:
            task.delete()

    def create_water_task(self):
        if self.watersum:
            if self.lastwater:
                today = date.today()
                month=today.month
                waterdate=''
                if month in [5,6,7,8,9]:
                    waterdate=timedelta(days=self.watersum)+self.lastwater
                else:
                    waterdate=timedelta(days=self.waterwin)+self.lastwater
                type="Water"
                task=PlantTasks(type=type, duedate=waterdate, plantid=self)
                task.save()

    def delete_and_create_water_task(self):
        if self.lastwater:
            task=PlantTasks.objects.get(plantid=self, done="False", type="Water")
            self.create_water_task()
            task.delete()


    def create_feed_task(self):
        if self.feedsum:
            if self.lastfeed:
                today = date.today()
                month=today.month
                feeddate=""
                if month in [5,6,7,8,9]:
                    feeddate=timedelta(days=self.feedsum)+self.lastfeed
                else:
                    feeddate=timedelta(days=self.feedwin)+self.lastfeed
                type="Feed"
                task=PlantTasks(type=type, duedate=feeddate, plantid=self)
                task.save() 

    def delete_and_create_feed_task(self):
        if self.lastfeed:
            task=PlantTasks.objects.get(plantid=self, done="False", type="Feed")
            self.create_feed_task()
            task.delete()

    def create_poting_task(self):
         if self.poting:
            if self.lastpot:
                potdate=timedelta(days=self.poting)+self.lastpot
                type="Repot"
                task=PlantTasks(type=type, duedate=potdate, plantid=self)
                task.save() 

    def delete_and_create_poting_task(self):
        if self.lastpot:
            task=PlantTasks.objects.get(plantid=self, done="False", type="Repot")
            self.create_poting_task()
            task.delete()

    def create_warm_task(self):
         if self.warm:
            if self.lastwarm:
                warmdate=timedelta(days=self.warm)+self.lastwarm
                type="Warm bath"
                task=PlantTasks(type=type, duedate=warmdate, plantid=self)
                task.save() 

    def delete_and_create_warm_task(self):
        if self.lastwarm:
            task=PlantTasks.objects.get(plantid=self, done="False", type="Warm bath")
            self.create_warm_task()
            task.delete()

    def create_clean_task(self):
        if self.clean:
            if self.lastclean:
                cleandate=timedelta(days=self.clean)+self.lastclean
                type="Clean"
                task=PlantTasks(type=type, duedate=cleandate, plantid=self)
                task.save() 

    def delete_and_create_clean_task(self):
        if self.lastclean:
            task=PlantTasks.objects.get(plantid=self, done="False", type="Clean")
            self.create_clean_task()
            task.delete()

    def create_spark_task(self):
        if self.spark:
            if self.lastspark:
                sparkdate=timedelta(days=self.spark)+self.lastspark
                type="Spray"
                task=PlantTasks(type=type, duedate=sparkdate, plantid=self)
                task.save() 

    def delete_and_create_spark_task(self):
        if self.lastspark:
            task=PlantTasks.objects.get(plantid=self, done="False", type="Spray")
            self.create_spark_task()
            task.delete()
    

    def create_tasks(self):
        self.create_water_task()
        self.create_feed_task()
        self.create_poting_task()
        self.create_warm_task()
        self.create_clean_task()
        self.create_spark_task()

    def count_average_sumwater(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Water", done="True").order_by('actualdate')
            listsum=[]
            listsum1=[]
            for task in tasks:
                if task.actualdate.month in [5,6,7,8,9]:
                    listsum.append(task.actualdate)     
            if len(listsum)>4:
                for i in range(0, len(listsum)-1):
                    dif= listsum[i+1]-listsum[i]
                    if dif.days<30:
                        listsum1.append(dif.days)
                avgsum=sum(listsum1)/len(listsum1)
                avgsum1="Average watering in summer time: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return

    def count_average_winwater(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Water", done="True").order_by('actualdate')
            listwin=[]
            listwin1=[]
            for task in tasks:
                if task.actualdate.month in [1,2,3,4,10,11,12]:
                    listwin.append(task.actualdate)     
            if len(listwin)>4:
                for i in range(0, len(listwin)-1):
                    dif= listwin[i+1]-listwin[i]
                    if dif.days<30:
                        listwin1.append(dif.days)
                avgsum=sum(listwin1)/len(listwin1)
                avgsum1="Average watering in winter time: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return


    def count_average_sumfeed(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Feed", done="True").order_by('actualdate')
            listsum=[]
            listsum1=[]
            for task in tasks:
                if task.actualdate.month in [5,6,7,8,9]:
                    listsum.append(task.actualdate)    
            if len(listsum)>4:
                for i in range(0, len(listsum)-1):
                    dif= listsum[i+1]-listsum[i]
                    if dif.days<30:
                        listsum1.append(dif.days)
                avgsum=sum(listsum1)/len(listsum1)
                avgsum1="Average feeding in summer time: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return

    def count_average_winfeed(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Feed", done="True").order_by('actualdate')
            listwin=[]
            listwin1=[]
            for task in tasks:
                if task.actualdate.month in [1,2,3,4,10,11,12]:
                    listwin.append(task.actualdate)     
            if len(listwin)>4:
                for i in range(0, len(listwin)-1):
                    dif= listwin[i+1]-listwin[i]
                    if dif.days<30:
                        listwin1.append(dif.days)
                avgsum=sum(listwin1)/len(listwin1)
                avgsum1="Average feeding in winter time: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return

    def count_average_warm(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Warm bath", done="True").order_by('actualdate')
            listwarm=[]
            listwarm1=[]
            for task in tasks:
                listwarm.append(task.actualdate)     
            if len(listwarm)>4:
                for i in range(0, len(listwarm)-1):
                    dif= listwarm[i+1]-listwarm[i]
                    listwarm1.append(dif.days)
                avgsum=sum(listwarm1)/len(listwarm1)
                avgsum1="Average warm bath: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return
        
    
    def count_average_clean(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Clean", done="True").order_by('actualdate')
            listclean=[]
            listclean1=[]
            for task in tasks:
                listclean.append(task.actualdate)     
            if len(listclean)>4:
                for i in range(0, len(listclean)-1):
                    dif= listclean[i+1]-listclean[i]
                    listclean1.append(dif.days)
                avgsum=sum(listclean1)/len(listclean1)
                avgsum1="Average cleaning: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return


    def count_average_spark(self):
        try:
            tasks=PlantTasks.objects.filter(plantid=self, type="Spray", done="True").order_by('actualdate')
            listspray=[]
            listspray1=[]
            for task in tasks:
                listspray.append(task.actualdate)     
            if len(listspray)>4:
                for i in range(0, len(listspray)-1):
                    dif= listspray[i+1]-listspray[i]
                    listspray1.append(dif.days)
                avgsum=sum(listspray1)/len(listspray1)
                avgsum1="Average spraying: {}".format(round(avgsum,1))
                return avgsum1
            else:
                return
        except:
            return
   


class PlantTasks(models.Model):
    id = models.BigAutoField(primary_key=True)
    description=models.CharField(max_length=500, null=True)
    type=models.CharField(max_length=100)
    duedate=models.DateField(null=True)
    actualdate= models.DateField(null=True)
    done=models.BooleanField(default=False)
    plantid=models.ForeignKey(Plants, on_delete=models.CASCADE, null=True)


    def taskdone(self):
        plant=Plants.objects.get(id=self.plantid.id)
        r.delete(f"{plant.id}_plant")
        if self.type=="Water":
          plant.lastwater=self.actualdate
          plant.save()
          plant.create_water_task()
        elif self.type=="Feed":
          plant.lastfeed=self.actualdate
          plant.lastwater=self.actualdate
          plant.save()
          task=PlantTasks.objects.get(type="Water", plantid=self.plantid.id, done="False")
          if task:
              task.actualdate=date.today()
              task.done=True
              task.save()
          plant.create_feed_task()
          plant.create_water_task()
        elif self.type=="Repot":
          plant.lastpot=self.actualdate
          plant.lastfeed=self.actualdate+timedelta(days=14)
          plant.save()
          task=PlantTasks.objects.get(type="Feed", plantid=self.plantid.id, done="False")
          task.delete()
          plant.create_poting_task()
          plant.create_feed_task()
        elif self.type=="Warm bath":
          plant.lastwarm=self.actualdate
          plant.lastwater=self.actualdate
          plant.save()
          task=PlantTasks.objects.get(type="Water", plantid=self.plantid.id, done="False")
          if task:
              task.actualdate=date.today()
              task.done=True
              task.save()
          plant.create_warm_task()
          plant.create_water_task()
        elif self.type=="Clean":
          plant.lastclean=self.actualdate
          plant.save()
          plant.create_clean_task()
        elif self.type=="Spray":
          plant.lastspark=self.actualdate
          plant.save()
          plant.create_spark_task()  

