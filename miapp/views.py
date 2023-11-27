from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.
def index(request):
    data ={
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