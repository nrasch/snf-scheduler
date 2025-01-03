from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root),
    path('snfs/', views.SNFListCreate.as_view(), name='snf-list-create'),
    path('snfs/<int:pk>/', views.SNFDetail.as_view(), name='snf-detail'),
]