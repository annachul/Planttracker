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
    path('api/', views.TodoView.as_view()),
    path('getlist/', views.PlantView.as_view({'get': 'list'})),
    path('poststatus/', views.StatusSerializer.as_view()),
     path('delete/', views.DeleteSerializer.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)