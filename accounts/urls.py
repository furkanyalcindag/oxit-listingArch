# import patterns as patterns
from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = "accounts"

urlpatterns = [

    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='forgot'),
    url(r'logout/$', views.pagelogout, name='logout'),


]
