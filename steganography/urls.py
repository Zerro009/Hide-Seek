from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('on', views.steganography_on),
    path('off', views.steganography_off),
    path('analysis', views.steganography_analysis)
]
