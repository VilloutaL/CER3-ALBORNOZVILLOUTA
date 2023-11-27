from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
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
            
