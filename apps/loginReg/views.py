from django.shortcuts import render, HttpResponse, redirect
from . models import *
from django.contrib import messages
import bcrypt

def index(request):
 
    return render(request, 'loginReg/index.html')

def login(request):
    result = User.objects.log_validator(request.POST)
    if len(result) > 0:
        for key in result.keys():
            messages.error(request, result[key])
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['log_email'])
        request.session['user_id'] = user.id      
    return redirect('/success')

def create(request):
    result = User.objects.reg_validator(request.POST)
    if len(result) > 0:
        for key in result.keys():
            messages.error(request, result[key])
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashedpw)
        user = User.objects.last()
        request.session['user_id'] = user.id
    return redirect('/success')

def success(request):
    if User.objects.get(id = request.session['user_id']) == User.objects.last():
        status = "registered"
    else:
        status = "logged in"

    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        'status' : status,
    }
    return render(request, 'loginReg/success.html', context)

