from django.contrib import admin
from django.http import request
from django.urls import path, include               
from rest_framework import routers                 
from plants import views     
from django.conf import settings
from django.conf.urls.static import static                     

router = routers.DefaultRouter()                   
router.register(r'plants', views.TodoView, 'plants')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/plants', views.TodoView.as_view(), name="plants"),
    path('api/plants/<id>', views.PlantId.as_view()),
    path('api/tasks', views.PlantTask.as_view(), name="planttask"),
    path('api/tasks/<id>/done', views.TaskDone),
    path('api/tasks/<id>', views.TaskId.as_view(), name="tasks_id"),
    path('api/plants/<id>/image', views.ImageUpload),
    path('api/plants/<id>/pdf', views.pdfexport)
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
