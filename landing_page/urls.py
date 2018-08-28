from django.conf.urls import url, include
from django.contrib.auth import views as contrib_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^administration/login/$', contrib_views.login, name='login'),
    url(r'^administration/logout/$', contrib_views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^cv/$', views.resume, name='cv'),
    url(r'^portfolio/$', views.portfolio, name='portfolio'),
    url(r'^contact/$', views.contact, name='contact'),
]