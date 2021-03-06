# import patterns as patterns
from django.conf.urls import url
from django.urls import path, re_path

from . import views

app_name = "accounts"

urlpatterns = [

    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='forgot'),
    path('forgot-user/', views.user_forgot, name='forgot-user'),

    url(r'logout/$', views.pagelogout, name='logout'),
    url(r'groups/$', views.groups, name='group'),
    url(r'permission/(?P<pk>\d+)$', views.permission, name='perm'),

    url(r'permission-save-api/$', views.permission_post, name="save-permission"),
    url(r'change-password/$', views.change_password, name='change_password'),

]
