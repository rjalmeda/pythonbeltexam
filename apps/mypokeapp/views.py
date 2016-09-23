from django.shortcuts import render, redirect
from .models import Poke
from ..mylogin.models import Users

# Create your views here.

def checkloggedin(request):
    return 'userid' in request.session

def index(request):
    if not checkloggedin(request):
        return redirect('/')
    print request.session['userid']
    userid = request.session['userid']
    context = {}
    context['allusers'] = Users.objects.all()
    context['count'] = Poke.objects.pokefromcount(userid)
    context['pokers'] = Poke.objects.pokedfrom(userid)
    context['pokerscount'] = Poke.objects.pokerscount(userid)
    return render(request, 'mypokeapp/index.html', context)

def makepoke(request):
    if not checkloggedin(request):
        return redirect('/')
    if request.method == 'POST':
        Poke.objects.registerpoke(request.POST)
        return redirect('/pokes')
    return redirect('/pokes')

