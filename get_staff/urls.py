from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
#from .views import GetStaffPostViewSet

# router = DefaultRouter()
# router.register('post', GetStaffPostViewSet, basename='post')

urlpatterns = [  # /get_staff/

    #path('', include(router.urls)),

    #path('posts/', views.get_staff_list)
    path('posts/', views.GetStaffPostList.as_view()),
    path('posts/<int:pk>', views.GetStaffPostDetail.as_view())
    ]