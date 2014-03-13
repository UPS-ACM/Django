from django.contrib import admin
#from writing.models import Paper, Comments
from writing.models import Building, Bin, BinStatus, Floor
    
#admin.site.register(Paper)
#admin.site.register(Comments)


admin.site.register(Building)
admin.site.register(Bin)
admin.site.register(BinStatus)
admin.site.register(Floor)