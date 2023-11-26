from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EventoSerializer
from miapp.models import Evento
# Create your views here.
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer