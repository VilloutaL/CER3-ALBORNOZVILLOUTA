from rest_framework import routers
from .views import EventoViewSet
from django.urls import path,include

router = routers.DefaultRouter()
router.register('eventos',EventoViewSet)

urlpatterns =[
    path('',include(router.urls)),
]