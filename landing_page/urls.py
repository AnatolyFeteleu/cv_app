from django.conf.urls import url
from django.contrib.auth import views as contrib_views
from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^administration/login/$', contrib_views.login, name='login'),
    url(r'^administration/logout/$', contrib_views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^cv/$', views.ResumeView.as_view(), name='cv'),
    url(r'^portfolio/$', views.PortfolioView.as_view(), name='portfolio'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^thanks/$', views.ThanksView.as_view(), name='thanks'),
]
