from django.urls import path, include
#from django.conf.urls import include
from . import views
from rest_framework import routers

from .views import ProfileList


#
# router = routers.DefaultRouter()
# router.register(r'profiles',
#                 views.ProfileList, basename='Profiles')
#
#

urlpatterns = [

    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>', views.ProfileDetail.as_view()),

    # path('profiles/',
    #      ProfileListCreateAPIView.as_view(),
    #      name='profile-list'),
    #ath(r'', include(router.urls)),

    ]