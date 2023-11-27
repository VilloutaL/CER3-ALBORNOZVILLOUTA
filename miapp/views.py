from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
<<<<<<< HEAD
from django.http import HttpResponse

from miapp.models import Evento


=======
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
>>>>>>> 1ca645a036bf701dfe42107d59f992c73740fb55
# Create your views here.
def index(request):
    segmento = request.GET.get("segmento", "S")
    tipo = request.GET.get("tipo", "S")
    año = 2023

    if(segmento == "S"):
        opciones_segmentos = [('S', "Todos")] + list(Evento.SEGMENTO_CHOICES)
    else:
        opciones_segmentos = list(Evento.SEGMENTO_CHOICES)
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
    if (segmento != "S"):
        eventos = eventos.filter(segmento = segmento)
    if (tipo != "S"):
        eventos = eventos.filter(tipo = tipo)


    data ={ 
        "año": año,
        "opciones_segmentos": opciones_segmentos,
        "opciones_tipo": opciones_tipo,
        "eventos": eventos,
        "segmento": segmento
    }
    return render(request,'miapp/index.html',data)





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
    return redirect('home')


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
            
