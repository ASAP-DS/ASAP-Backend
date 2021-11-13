from django.urls import path, include


from rest_framework import routers

from . import views
from .views import ProfileList

#router 다시 공부하기 (나중에 바꿔보자)

urlpatterns = [

   path('profiles/', views.ProfileList.as_view()),
   path('profiles/<int:pk>', views.ProfileDetail.as_view()),
  # path('join/',views),

    ]