"""ASAP_Prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import include
from django.conf.urls.static import static
from rest_framework import routers

from users import views
from users.views import main




urlpatterns = [
    path('', main),
    path('jobs/', views.JobList.as_view()),
    path('users/', include('users.urls')),
    path('get_staff/', include('get_staff.urls')),

    path('api-auth', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    # path('get_staff', include('get_staff.urls')),
    # path('search_job', include('search_job.urls')),

]
#
# + static(settings.STATIC_URL, document_root=settings.STATIC_URL)