"""cv_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from landing_page import views
from rest_framework import routers
from . import settings


router = routers.DefaultRouter()
router.register(r'rest/users', views.UserViewSet)
router.register(r'rest/cv', views.CVViewSet)
router.register(r'rest/other', views.OtherViewSet)  # Error need fix
router.register(r'rest/language', views.LanguageViewSet)
router.register(r'rest/company', views.CompanyViewSet)
router.register(r'rest/education', views.EducationViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('landing_page.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Added route for media files
