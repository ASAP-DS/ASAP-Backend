from django.urls import path
from . import views

urlpatterns = [
    path('sort_early_start/', views.sort_early_start),
    path('add_comment/', views.add_comment),
    path('<int:pk>/comments/', views.CommentSearchJobList.as_view()),
    path('<int:pk>/comments/<int:pk2>', views.CommentSearchJobDetail.as_view()),
    path('posts/', views.SearchJobPostList.as_view()),
    path('posts/<int:pk>', views.SearchJobPostDetail.as_view())
]

