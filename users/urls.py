
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='base'),
    path('signup/', views.signup, name='signup'),
    path('log/', views.login_views, name='log'),
]
