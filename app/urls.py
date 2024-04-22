from django.contrib import admin
from django.urls import path
from app.views import *
from app import views

urlpatterns = [
    path('', index, name="index"),
  
]
