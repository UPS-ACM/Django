from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

#from writing.models import Paper, Comments, PaperForm, Building
from writing.models import Building, Bin, BinStatus, Floor

#
import csv

@login_required(login_url='/writing/login/')
def IndexView(request):
	get_locations = Building.objects.all()
	return render(request, 'writing/index.html', {'get_locations' : get_locations})

@login_required(login_url='/writing/login/')
def building(request, name):
    get_locations = Floor.objects.filter(building__name = name)
    return render(request, 'writing/building.html', {'get_locations' : get_locations})

@login_required(login_url='/writing/login/')
def bin(request, name, floor):
    # Handle a button update.
    # Get the latest status associated with the bin and if it's not the same make a new status object.
    status_get_value = 'submit'     # Avoid hardcoding this
    bin_get_value = 'bin'
    if request.method == 'GET':
        binStatus = None
        if(request.GET.get(bin_get_value, '')):
            binStatus = BinStatus.objects.filter(theBin__pk = request.GET.get(bin_get_value)).latest('time')

        # Check if the get request is correct and if a binStatus was found for the id
        if(request.GET.get(status_get_value, '') and binStatus):
            # if the status recorded isn't the same as before, make a new status object
            if(request.GET.get(status_get_value) != binStatus.status):
                new_status = BinStatus(theBin = binStatus.theBin, status = request.GET.get(status_get_value), byUser = request.user)
                try:
                    new_status.full_clean()     # validate new entry
                    new_status.save()
                except ValidationError as e:
                    pass

    #Display view

    #get_bins = BinStatus.objects.filter(theBin__building__name = name).filter(theBin__floor__name = floor)
    get_bins = Bin.objects.filter(building__name = name).filter(floor__name = floor)
    get_status = []

    # Make sure to return just the latest status. Note: Must have a status associated with the bin
    # to display anything! Otherwise just don't add the bin to the display list.
    for bin in get_bins:
        if(BinStatus.objects.filter(theBin = bin)):
            get_status.append(BinStatus.objects.filter(theBin = bin).latest("time"))

    return render(request, 'writing/bin.html', {'get_bins': get_status})

def returnCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="output.csv"'

    # query
    theBins = BinStatus.objects.order_by('-time')

    writer = csv.writer(response)
    writer.writerow(['Date', 'Building', 'Floor', 'Description', 'Status', 'User'])
    for binStatus in theBins :
        writer.writerow([binStatus.time, binStatus.theBin.building, binStatus.theBin.floor, 
            binStatus.theBin.description, binStatus.status, binStatus.byUser])

    return response


##@login_required(login_url='/writing/login/')
##def IndexView(request):
##	if request.method == 'POST':
##        	Paper.delete(Paper.objects.get(title = request.POST['thepaper']))
##	get_papers = Paper.objects.filter(by_user = request.user).order_by('-time')
##	return render(request, 'writing/index.html', {'get_papers' : get_papers})

# @login_required(login_url='/writing/login/')
# def paper(request, t):
#     get_paper = get_object_or_404(Paper, title=t)
#     return render(request, 'writing/paper.html', {'get_paper': get_paper})

# @login_required(login_url='/writing/login/')
# def add_paper(request):
#     if request.method == 'POST':
#         form = PaperForm(request.POST, instance = Paper(by_user = request.user))
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/writing/')
#     else:
#         form = PaperForm()

#     return render(request, 'writing/addpaper.html', {'form': form})

def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
	    form.save()
	    usr = authenticate(username = request.POST['username'], password = request.POST['password1'])
	    login(request, usr)
            return HttpResponseRedirect('/writing/')
    else:
        form = UserCreationForm()

    return render(request, 'writing/add_user.html', {'form': form})
