from django.conf.urls import url

from kurye.Views import DashboardViews

app_name = 'kurye'

urlpatterns = [

    # Dashboard
    url(r'dashboard/admin-dashboard/$', DashboardViews.return_admin_dashboard, name='admin-dashboard'),





   






]
