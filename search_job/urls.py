from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.SearchJobPostList.as_view()),
    path('posts/<int:pk>', views.SearchJobPostDetail.as_view())
]