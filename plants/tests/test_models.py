from django.test import TestCase


from ..models import PlantTasks, Plants
from datetime import date, timedelta, datetime
from importlib import reload 


class PlantTasksModelTests(TestCase):
    def test_taskdone_water(self):
        plant=Plants(plantname="FooPlant", watersum=3, waterwin=3, lastwater=date.today())
        plant.save()
        task=PlantTasks(type="Water", actualdate=date.today(), done=True, plantid=plant)
        task.taskdone()
        newtask=PlantTasks.objects.get(type="Water", done=False, plantid=plant)
        waterdate=date.today()+timedelta(days=3)
        self.assertEqual(newtask.duedate, waterdate)

    def test_taskdone_feed(self):
        plant3=Plants(plantname="WohPlant", watersum=3, waterwin=3, feedsum=14, feedwin=14)
        plant3.save()
        task1=PlantTasks(type="Feed", actualdate=date.today(), done=True, plantid=plant3)
        task1.save()
        task2=PlantTasks(type="Water", actualdate=date.today(), done=False, plantid=plant3)
        task2.save()
        task1.taskdone()
        plant3=Plants.objects.get(id=task1.plantid.id)
        self.assertEqual(plant3.lastfeed, date.today())
        self.assertEqual(plant3.lastwater, date.today())
        task2new=PlantTasks.objects.get(id=task2.id)
        self.assertEqual(task2new.done, True)
        tasksnew=PlantTasks.objects.filter(plantid=plant3, done=False)
        self.assertEqual(len(tasksnew), 2)

class PlantsModelTests(TestCase):
    def test_delete_all_active_tasks(self):
        plant=Plants(plantname="MooPlant", watersum=3, waterwin=3, feedsum=14, feedwin=14)
        plant.save()
        task1=PlantTasks(type="Feed", actualdate=date.today(), done=False, plantid=plant)
        task1.save()
        task2=PlantTasks(type="Water", actualdate=date.today(), done=False, plantid=plant)
        task2.save()
        plant.delete_all_active_tasks()
        tasks=PlantTasks.objects.filter(plantid=plant)
        self.assertEqual(len(tasks), 0)

