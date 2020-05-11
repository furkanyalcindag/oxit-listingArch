from django.conf.urls import url

from kurye.Views import DashboardViews, UserViews, CityViews, TaskViews, RequestViews, CourierViews

app_name = 'kurye'

urlpatterns = [

    # Dashboard
    url(r'dashboard/admin-dashboard/$', DashboardViews.return_admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/company-dashboard/$', DashboardViews.return_company_dashboard, name='kullanıcı-dashboard'),
    url(r'dashboard/courier-dashboard/$', DashboardViews.return_courier_dashboard, name='kurye-dashboard'),

    # Kurye
    url(r'Courier/add-courier/$', UserViews.add_courier, name='kurye ekle'),
    url(r'Courier/courier-list/$', UserViews.list_courier, name='kurye listesi'),
    url(r'Courier/assigned-tasks-list/$', CourierViews.assigned_task, name='kurye atanan gorevler'),

    # Müşteri Firma
    url(r'add-customer/$', UserViews.add_customer, name='musteri ekle'),
    url(r'customer-list/$', UserViews.customer_list, name='musteri listesi'),

    # İlçe
    url(r'ilce-getir/$', CityViews.get_districts, name="ilce-getir"),

    # Kullanıcı Firma
    url(r'add-company/$', UserViews.add_company, name='kullanıcı-firma ekle'),
    url(r'company-list/$', UserViews.company_list, name='kullanıcı listesi'),

    # Görev
    url(r'pending-requests/(?P<pk>\d+)$', TaskViews.requests, name='talepler'),
    url(r'add-task/(?P<pk>\d+)$', TaskViews.add_task, name='gorev ata'),
    url(r'active-tasks/$', TaskViews.active_tasks, name='aktif gorevler'),

    # Talep
    url(r'request/add-request/$', RequestViews.new_user_add_request, name='yeni kullanıcıyla talep olustur'),
    url(r'request/create-request/$', RequestViews.registered_user_add_request,
        name='kayıtlı kullanıcıyla talep olustur'),
    url(r'dashboard/requests/$', RequestViews.return_pending_request, name='bekleyen talepler'),
    url(r'dashboard/admin-dashboard/request-approve/$', RequestViews.pendingRequestActive, name="talep-onayla"),
    url(r'dashboard/admin-dashboard/request-delete/(?P<pk>\d+)$', RequestViews.pending_request_delete,
        name='talep-sil'),
    url(r'dashboard/approved-request/$', RequestViews.return_approved_requests, name='onaylanan talepler'),

]
