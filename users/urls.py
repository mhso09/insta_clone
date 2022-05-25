
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
]
