from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('snf/', views.snf, name='snf'),
    path('delete-snf/', views.delete_snf, name='delete_snf'),
    path('add-snf/', views.add_snf, name='add_snf'),
]