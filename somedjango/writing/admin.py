from django.contrib import admin
from writing.models import Building, Bin, BinStatus, Floor

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.conf.urls import patterns
from django import forms

import csv

class ExportForm(forms.Form):
	start = forms.DateField(label = "Start date", required = False)
	end = forms.DateField(label = "End date", required = False)
	exportAll = forms.BooleanField(label = "Export all data", required = False)

class MyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^exportForm/$', self.admin_site.admin_view(self.getCSV)),
            (r'^getCSV/$', self.admin_site.admin_view(self.getCSV)),
        )
        return my_urls + urls

    def exportForm(self, request):
		return render(request, 'admin/toCSV.html')

    def getCSV(self, request):
    	if request.GET.items():
    		form = ExportForm(request.GET)
    		if form.is_valid():
                        response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="output.csv"'

                        # query all items
                        start = form.cleaned_data['start']
                        end = form.cleaned_data['end']
                        theBins = []
                        if(request.GET.get('exportAll', '')):
                                exportAll = form.cleaned_data['exportAll']
                                theBins = BinStatus.objects.order_by('-time')

                        # query items in date range
                        elif(start and end):
                                theBins = BinStatus.objects.filter(time__range = (start, end)).order_by('-time')

                        writer = csv.writer(response)
                        writer.writerow(['Date', 'Building', 'Floor', 'Description', 'Status', 'User'])
                        for binStatus in theBins:
                                writer.writerow([binStatus.time, binStatus.theBin.building, binStatus.theBin.floor, 
                                        binStatus.theBin.description, binStatus.status, binStatus.byUser])

                        return response
    			#return HttpResponseRedirect('admin/')

    	else:
                form = ExportForm()

    	return render(request, 'admin/toCSV.html', {'form': form})


admin.site.register(Building, MyModelAdmin)
admin.site.register(Bin)
admin.site.register(BinStatus)
admin.site.register(Floor)
