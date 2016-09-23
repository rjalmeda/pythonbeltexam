from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users
from datetime import datetime

# Create your views here.
def checkloggedin(request):
    return 'userid' in request.session
    

def index(request):
    if checkloggedin(request):
        return redirect('/pokes')
    return render(request, 'mylogin/index.html')

def success(request):
    context = {}
    user = Users.objects.get(id=request.session['userid'])
    context['user'] = user
    return render(request, 'mylogin/success.html', context)

def displayall(request):
    context = {}
    allusers = Users.objects.all()
    context['allusers'] = allusers
    return render(request, 'mylogin/displayall.html', context)

def register(request):
    if request.method == 'POST':
        res = Users.objects.register(request.POST)
        if res['success']:
            user = Users.objects.get(email=request.POST['email'])
            request.session['name'] = user.name
            request.session['alias'] = user.alias
            request.session['userid'] = user.id
            request.session['email'] = user.email
            for message in res['success']:
                messages.add_message(request, messages.SUCCESS, message)
            return redirect('/success')
        else:
            for message in res['errors']:
                messages.add_message(request, messages.ERROR, message)
            return redirect('/')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        res = Users.objects.login(request.POST)
        if res['success']:
            user = Users.objects.get(email=request.POST['email'])
            print user
            request.session['name'] = user.name
            request.session['alias'] = user.alias
            request.session['userid'] = user.id
            request.session['email'] = user.email
            for message in res['success']:
                messages.add_message(request, messages.SUCCESS, message)
            return redirect('/success')
        else:
            for message in res['errors']:
                messages.add_message(request, messages.ERROR, message)
            return redirect('/')
    else:
        return redirect('/')
    
def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')
    
def delete(request, deleteid):
    user = Users.objects.get(id=deleteid)
    user.delete()
    return redirect('/displayall')
    