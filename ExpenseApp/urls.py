from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('delete/<int:id>/', views.delete, name = 'delete')
]
