from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView
                    
urlpatterns = [
    url(r'^$', views.home),
    url(r'^user$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index')
]