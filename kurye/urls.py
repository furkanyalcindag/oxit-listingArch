from django.conf.urls import url

from kurye.Views import DashboardViews, UserViews, CityViews, TaskViews, RequestViews, CourierViews

app_name = 'kurye'

urlpatterns = [

    # Dashboard
    url(r'dashboard/admin-dashboard/$', DashboardViews.return_admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/company-dashboard/$', DashboardViews.return_company_dashboard, name='kullanıcı-dashboard'),
    url(r'dashboard/courier-dashboard/$', CourierViews.assigned_task, name='kurye-dashboard'),

    # Kurye
    url(r'Courier/add-courier/$', UserViews.add_courier, name='kurye ekle'),
    url(r'Courier/courier-list/$', CourierViews.courier_list, name='kurye listesi'),
    url(r'Courier/assigned-tasks-list/$', CourierViews.assigned_task, name='kurye atanan gorevler'),
    url(r'Courier/ending-tasks/$', CourierViews.courier_ending_tasks, name='kurye tamamlanan gorevler'),
    url(r'Courier/tasks/$', CourierViews.courier_tasks, name='kurye gorevler'),
    url(r'getCourier/(?P<pk>\d+)$', CourierViews.getCourier, name='kurye getir'),

    # Müşteri Firma
    url(r'add-customer/$', UserViews.add_customer, name='musteri ekle'),
    url(r'customer-list/$', UserViews.customer_list, name='musteri listesi'),
    url(r'customer-delete/(?P<pk>\d+)$', UserViews.customer_delete, name='musteri-sil'),

    # İlçe
    url(r'ilce-getir/$', CityViews.get_districts, name="ilce-getir"),

    # Kullanıcı Firma
    url(r'add-company/$', UserViews.add_company, name='kullanıcı firma ekle'),
    url(r'company-list/$', UserViews.company_list, name='kullanıcı listesi'),

    # Görev
    url(r'select-request/(?P<pk>\d+)$', TaskViews.requests, name='talepler'),
    url(r'add-task/(?P<pk>\d+)$', TaskViews.add_task, name='gorev ata'),
    url(r'completed-task/$', TaskViews.return_completed_task, name='tamamlanan gorevler'),
    url(r'active-task/$', TaskViews.return_active_task, name='aktif gorevler'),
    url(r'canceled-tasks/$', TaskViews.return_canceled_task, name='kullanıcı iptal edilen gorevler'),
    url(r'getTask/(?P<pk>\d+)$', TaskViews.getTask, name='gorev getir'),
    url(r'assign-courier/$', TaskViews.assign_courier, name='kurye sec'),

    # Talep
    url(r'request/add-request/$', RequestViews.new_user_add_request, name='yeni kullanıcıyla talep olustur'),
    url(r'request/create-request/$', RequestViews.registered_user_add_request,
        name='kayıtlı kullanıcıyla talep olustur'),
    url(r'dashboard/requests/$', RequestViews.return_pending_request, name='bekleyen talepler'),
    url(r'dashboard/admin-dashboard/request-approve/$', RequestViews.pendingRequestActive, name="talep-onayla"),

    url(r'dashboard/admin-dashboard/request-delete/(?P<pk>\d+)$', RequestViews.pending_request_delete,
        name='talep-sil'),
    url(r'dashboard/approved-request/$', RequestViews.return_approved_requests, name='onaylanan talepler'),
    url(r'User/active-requests/$', RequestViews.return_company_requests, name='kullanıcı aktif talepleri'),
    url(r'User/ending-tasks/$', RequestViews.return_company_ending_tasks, name='kullanıcının biten talepleri'),
    url(r'User/cancel-task/(?P<pk>\d+)$', RequestViews.cancel_requests, name='kullanıcı talabi iptal et'),
    url(r'User/complete-task/(?P<pk>\d+)$', TaskViews.taskComplete, name="görevi bitir"),
    url(r'getRequest/(?P<pk>\d+)$', RequestViews.getRequest, name='talep getir'),

    # Admin ekle
    url(r'add-admin/$', UserViews.add_admin, name='admin-ekle'),
    url(r'change-password/$', UserViews.user_change_password, name='sifre-guncelle'),

    # Profil
    url(r'profile/$', UserViews.users_information, name='profil'),

    #bildirim
    url(r'bildirimler', DashboardViews.notification, name='bildirimler'),

]
