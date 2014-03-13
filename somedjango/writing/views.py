from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

#from writing.models import Paper, Comments, PaperForm, Building
from writing.models import Building, Bin, BinStatus, Floor

@login_required(login_url='/writing/login/')
def IndexView(request):
	get_locations = Building.objects.all()
	return render(request, 'writing/index.html', {'get_locations' : get_locations})

@login_required(login_url='/writing/login/')
def building(request, name):
    get_locations = Floor.objects.filter(building__name = name)
    return render(request, 'writing/building.html', {'get_locations' : get_locations})

@login_required(login_url='/writing/login/')
def Bin(request, name, floor):
    get_bins = Bin.objects.filter(building__name = name).filter(floor__name = floor)
    return render(request, 'writing/building.html', {'get_bins' : get_bins, 'name' : name})


##@login_required(login_url='/writing/login/')
##def IndexView(request):
##	if request.method == 'POST':
##        	Paper.delete(Paper.objects.get(title = request.POST['thepaper']))
##	get_papers = Paper.objects.filter(by_user = request.user).order_by('-time')
##	return render(request, 'writing/index.html', {'get_papers' : get_papers})

@login_required(login_url='/writing/login/')
def paper(request, t):
    get_paper = get_object_or_404(Paper, title=t)
    return render(request, 'writing/paper.html', {'get_paper': get_paper})

@login_required(login_url='/writing/login/')
def add_paper(request):
    if request.method == 'POST':
        form = PaperForm(request.POST, instance = Paper(by_user = request.user))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/writing/')
    else:
        form = PaperForm()

    return render(request, 'writing/addpaper.html', {'form': form})

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
	    form.save()
	    usr = authenticate(username = request.POST['username'], password = 				request.POST['password1'])
	    login(request, usr)
            return HttpResponseRedirect('/writing/')
    else:
        form = UserCreationForm()

    return render(request, 'writing/add_user.html', {'form': form})
