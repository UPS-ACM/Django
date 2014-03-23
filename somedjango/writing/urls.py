from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from writing import views

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'writing/login.html'}, name = 'login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/writing/'}, name = 'logout'),
#    url(r'^test_export/$', views.returnCSV),
    url(r'^$', views.IndexView, name='index'),
    url(r'^add_user/$', views.add_user, name = 'add_user'),
    url(r'^(?P<name>[\w|\W]+)/(?P<floor>[\w|\W]+)/$', views.bin, name = 'goto_bin'),
    url(r'^(?P<name>[\w|\W]+)/$', views.building, name = 'goto_building'),
)
