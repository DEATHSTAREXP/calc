from django.urls import path
from . import views

urlpatterns = [
    path('', views.matrix_calculator, name='calcapp'),
]