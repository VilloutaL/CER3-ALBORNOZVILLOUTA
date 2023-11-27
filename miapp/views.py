from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from miapp.models import Evento


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
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['pasword1'])
                user.save()
                return HttpResponse('Usuario creado')
            except:
                return render(request,'miapp/singup.html',{
                    'form' : UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request,'miapp/singup.html',{
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })   