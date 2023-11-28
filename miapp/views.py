from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from miapp.models import Evento, Segmento
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# Create your views here.


def index(request):
    segmento = request.GET.get("segmento", "S")
    tipo = request.GET.get("tipo", "S")
    fecha_actual = datetime.now()
    año = fecha_actual.year
    if(segmento == "S"):
        opciones_segmentos = [('S', "Todos")] + list(Segmento.SEGMENTO_CHOICES)
    else:
        opciones_segmentos = list(Segmento.SEGMENTO_CHOICES)
        for opcion in opciones_segmentos:
            if opcion[0] == segmento:
                opciones_segmentos.remove(opcion)
                opciones_segmentos.insert(0, opcion)
        opciones_segmentos.append(('S', "Todos"))

    if(tipo == "S"):
        opciones_tipo = [('S', "Todos" )] + list(Evento.TIPO_CHOICES)
    else:
        opciones_tipo = list(Evento.TIPO_CHOICES)
        for opcion in opciones_tipo:
            if opcion[0] == tipo:
                opciones_tipo.remove(opcion)
                opciones_tipo.insert(0, opcion)
        opciones_tipo.append(('S', "Todos"))
    
   
    

    eventos = Evento.objects.filter(fecha_termino__gte = fecha_actual)
    if (segmento != "S"):
        eventos = eventos.filter(segmento__segmento = segmento)
    if (tipo != "S"):
        eventos = eventos.filter(tipo = tipo)

    eventos = eventos.order_by('fecha_inicio')

    data ={ 
        "año": año,
        "opciones_segmentos": opciones_segmentos,
        "opciones_tipo": opciones_tipo,
        "eventos": eventos,
        "segmento": segmento
    }
    return render(request,'miapp/index.html',data)




@login_required
def home(request):
    segmento = request.GET.get("segmento", "S")
    tipo = request.GET.get("tipo", "S")
    fecha_actual = datetime.now()
    año = fecha_actual.year

    if(segmento == "S"):
        opciones_segmentos = [('S', "Todos")] + list(Segmento.SEGMENTO_CHOICES)
    else:
        opciones_segmentos = list(Segmento.SEGMENTO_CHOICES)
        for opcion in opciones_segmentos:
            if opcion[0] == segmento:
                opciones_segmentos.remove(opcion)
                opciones_segmentos.insert(0, opcion)
        opciones_segmentos.append(('S', "Todos"))

    if(tipo == "S"):
        opciones_tipo = [('S', "Todos" )] + list(Evento.TIPO_CHOICES)
    else:
        opciones_tipo = list(Evento.TIPO_CHOICES)
        for opcion in opciones_tipo:
            if opcion[0] == tipo:
                opciones_tipo.remove(opcion)
                opciones_tipo.insert(0, opcion)
        opciones_tipo.append(('S', "Todos"))



    eventos = Evento.objects.all()
    usuario = request.user
    grupos_usuario = usuario.groups.all()


    eventos = Evento.objects.filter(fecha_termino__gte = fecha_actual)
    if (segmento != "S"):
        eventos = eventos.filter(segmento__segmento = segmento)
    if (tipo != "S"):
        eventos = eventos.filter(tipo = tipo)

    eventos = eventos.order_by('fecha_inicio')
    
    for grupo in grupos_usuario:
        if (grupo.name == "Profesor"):
            mis_eventos = eventos.filter(segmento__segmento = "PR")
        elif (grupo.name == "Jefe Carrera"):
            mis_eventos = eventos.filter(segmento__segmento = "JC")

    aux = []
    contador = 0
    for i in mis_eventos:
        if contador < 3:
            aux.append(i)
        contador +=1


    data ={ 
        "año": año,
        "opciones_segmentos": opciones_segmentos,
        "opciones_tipo": opciones_tipo,
        "eventos": eventos,
        "segmento": segmento,
        "mis_eventos": aux
    }
    return render(request,'miapp/home.html',data)


def singup(request):

    if request.method == 'GET':    
        return render(request,'miapp/singup.html',{
        'form' : UserCreationForm
        })
    else:
        if request.POST['password1']== request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request,'miapp/singup.html',{
                    'form' : UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request,'miapp/singup.html',{
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })   
    
def singout(request):
    logout(request)
    return redirect('index')


def singin(request):
    if request.method == 'GET':
        return render(request, 'miapp/login.html', {
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request,'miapp/login.html', {
                'form' : AuthenticationForm,
                'error':'Usuario o contraseña incorrecta'
            })
        else:
            login(request,user)
            return redirect('home')
            
