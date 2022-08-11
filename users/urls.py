from django.urls import path
from . import views


urlpatterns = [
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('u/<str:pk>/', views.userProfile, name='user_profile'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('create_message/<str:pk>/', views.createMessage, name='create_message')
]
