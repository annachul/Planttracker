from django.test import TestCase

from ..models import PlantTasks, Plants
from datetime import date, timedelta, datetime
from django.test import Client
from django.urls import reverse
import json



client = Client()

class PlantsTodoViewTests(TestCase):
    def test_get_plants(self):
        plant1=Plants(plantname="FooPlant", watersum=3, waterwin=3, lastwater=date.today())
        plant1.save()
        plant2=Plants(plantname="BooPlant", watersum=3, waterwin=3, lastwater=date.today())
        plant2.save()
        response = self.client.get(reverse('plants'))
        lencon=len(response.json())
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(
            json_response[0]['plantname'],
            plant1.plantname
        )
        self.assertEqual(lencon, 2)

class TaskIdViewTests(TestCase):
    def test_delete_task(self):
        task=PlantTasks(type="Water", duedate=date.today(), done=False)
        task.save()
        response = self.client.delete(reverse('tasks_id', args=[task.id]))
        self.assertEqual(response.status_code, 200)
        task=PlantTasks.objects.filter(type="Water")
        self.assertEqual(
            len(task),
            0
        )

class PlantTaskTests(TestCase):
    def test_post_task(self):
        plant=Plants(plantname="NOOPlant", watersum=3, waterwin=3, lastwater=date.today())
        plant.save()
        data={'type': "Water", 'duedate': "2022-02-22", 'done': False, 'description': "blabla", 'plantname': "NOOPlant"}
        response = self.client.post(reverse('planttask'), data, content_type='application/json',)
        self.assertEqual(response.status_code, 200)
        tasks=PlantTasks.objects.filter(plantid=plant)
        self.assertEqual(len(tasks), 1)
