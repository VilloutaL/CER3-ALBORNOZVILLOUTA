from django.shortcuts import render

# Create your views here.
def index(request):
    data ={

    }
    return render(request,'miapp/index.html',data)