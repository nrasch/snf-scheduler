from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.user_login, name='login'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('tokens/', views.get_tokens, name='tokens'),
]