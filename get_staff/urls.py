from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
#from .views import GetStaffPostViewSet

# router = DefaultRouter()
# router.register('post', GetStaffPostViewSet, basename='post')

urlpatterns = [  # /get_staff/
    path('sort_high_pay/', views.sort_high_pay), #시급높은순으로 post정렬
    path('add_comment/', views.add_comment),
    path('<int:pk>/comments/', views.CommentGetStaffList.as_view()),
   path('<int:pk>/comments/<int:pk2>', views.CommentGetStaffDetail.as_view()),
    path('posts/', views.GetStaffPostList.as_view()),
    path('posts/<int:pk>', views.GetStaffPostDetail.as_view())
    ]