from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt
import re

# Create your views here.
def index(request):
    return render(request, 'regi/index.html')

def register(request):
    valid = True
    if not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', request.POST['email']):
        messages.add_message(request, messages.ERROR, 'Invalid email')
        valid = False
    if len(request.POST['password']) < 8:
        messages.add_message(request, messages.ERROR, 'password must be longer than 8 characters')
        valid = False
    if len(request.POST['first_name']) < 2:
        messages.add_message(request, messages.ERROR, 'No Fewer than 2 characters')
        valid = False
    if len(request.POST['last_name']) < 2:
        messages.add_message(request, messages.ERROR, 'No Fewer than 2 characters')
        valid = False
    if User.objects.filter(email=request.POST['email']):
        messages.add_message(request, messages.ERROR, 'email already exist')
        valid = False
    if not valid:
        return redirect('/')
    else:
        newuser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=request.POST['password'])
        request.session['user_id'] = User.objects.filter(email=request.POST['email'])[0].id
        data = User.objects.filter(id = request.session['user_id'])
        context = {
        'data':data
        }

        return render(request, 'regi/success.html', context)

def login(request):
    valid = True
    log_user = User.objects.filter(email=request.POST['email'])
    if not User.objects.filter(email=request.POST['email']):
        messages.add_message(request, messages.ERROR, 'email is not registered')
        valid = False
    if not User.objects.filter(password=request.POST['password']).exists():
        messages.add_message(request, messages.ERROR, 'password is not correct')
        valid = False
    if valid:
        request.session['user_id'] = log_user[0].id
        data = User.objects.filter(id=request.session['user_id'])
        context = {
        'data':data
        }
        return render(request, 'regi/success.html', context)
    else:
        return redirect('/')

def log_out(request):
    request.session.flush()
    return redirect('/')
