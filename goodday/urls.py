from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

app_name = 'goodday'
urlpatterns = [
    # ex: /goodday/
    path('', views.index, name='index'),
    # ex: /goodday/5/
    path('detail/<int:response_id>/', views.detail, name='detail'),
    # ex: /goodday/today
    path('today/', views.today, name='today'),
    # signup!
    path('goodday/', include('django.contrib.auth.urls')),
    url(r'^signup/$', views.signup, name='signup'),

]
