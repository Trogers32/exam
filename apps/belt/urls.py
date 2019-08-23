from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView
                    
urlpatterns = [
    url(r'^$', views.home),
    url(r'^/new$', views.ctrip),
    url(r'^/add_trip$', views.addtrip),
    url(r'^/(?P<num>\d+)$', views.viewtrip),
    url(r'^/join/(?P<num>\d+)$', views.jointrip),
    url(r'^/subedit/(?P<num>\d+)$', views.edit),
    url(r'^/edit/(?P<num>\d+)$', views.edit_trip),
    url(r'^/cancel/(?P<num>\d+)$', views.canceltrip), 
    url(r'^/remove/(?P<num>\d+)$', views.removetrip),
    url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index')
]