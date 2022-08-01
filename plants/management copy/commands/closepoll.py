from django.core.management.base import BaseCommand
from plants.models import Plants

class Command(BaseCommand):
    help = "Create tasks for excisting plants"
    def handle(self, *args, **options):
        plants=Plants.objects.all()
        for plant in plants:
            if plant.status=="list":
                plant.create_tasks()
