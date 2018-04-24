from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'goodday'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path('logout/', auth_views.logout, {'template_name': 'accounts/logout.html'}, name='logout'), #template_name redirects the default to my page at accounts/logout
]
