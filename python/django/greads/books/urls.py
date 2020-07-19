from django.urls import path

from . import views

urlpatterns = [
    path('', views.parse_goodreads_urls, name='parse_goodreads_urls'),
]