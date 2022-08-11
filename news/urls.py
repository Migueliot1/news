from django.urls import path
from . import views


urlpatterns = [
    path('', views.showNews, name='news_main'),
    path('article/<str:pk>/', views.showArticle, name='single_article'),
    path('dltCmt/<str:pk>/', views.deleteComment, name='delete_comment'),
    path('about/', views.aboutPage, name='about_page'),
]
