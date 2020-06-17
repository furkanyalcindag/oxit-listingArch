from django.conf.urls import url

from kurye.Views import DashboardViews, UserViews, CityViews, TaskViews, RequestViews, CourierViews, APIViews, LogView, \
    ReportViews, EarningPaymentsViews

app_name = 'kurye'

urlpatterns = [

    # Dashboard
    url(r'dashboard/admin-dashboard/$', DashboardViews.return_admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/company-dashboard/$', DashboardViews.return_company_dashboard, name='kullanıcı-dashboard'),
    url(r'dashboard/courier-dashboard/$', DashboardViews.return_courier_dashboard, name='kurye-dashboard'),

    # Kurye
    url(r'Courier/add-courier/$', UserViews.add_courier, name='kurye ekle'),
    url(r'Courier/courier-list/$', CourierViews.courier_list, name='kurye listesi'),
    url(r'Courier/assigned-tasks-list/$', CourierViews.assigned_task, name='kurye atanan gorevler'),
    url(r'Courier/update-task/$', CourierViews.assigned_task, name='kurye-gorev-guncelle'),
    url(r'Courier/ending-tasks/$', CourierViews.courier_ending_tasks, name='kurye tamamlanan gorevler'),
    url(r'Courier/tasks/$', CourierViews.courier_tasks, name='kurye gorevler'),
    url(r'getCourier/(?P<pk>\d+)$', CourierViews.getCourier, name='kurye getir'),
    url(r'courier-delete/$', UserViews.courier_delete, name='kurye-sil'),
    url(r'courier-update/(?P<pk>\d+)$', UserViews.update_courier, name='kurye-guncelle'),

    # Kullanıcının Müşterileri
    url(r'add-customer/$', UserViews.add_customer, name='musteri ekle'),
    url(r'customer-list/$', UserViews.customer_list, name='musteri listesi'),
    url(r'customer-delete/$', UserViews.customer_delete, name='musteri-sil'),
    url(r'customer-update/(?P<pk>\d+)$', UserViews.update_customer, name='musteri-guncelle'),

    # Personel (admin)
    url(r'add-personal/$', UserViews.add_personal, name='personel-ekle'),
    url(r'personal-list/$', UserViews.personel_list, name='personel-listesi'),
    url(r'personal-delete/$', UserViews.personal_delete, name='personel-sil'),

    # İlçe/Mahalle
    url(r'ilce-getir/$', CityViews.get_districts, name="ilce-getir"),
    url(r'mahalle-getir/$', CityViews.get_neighborhood, name="mahalle-getir"),

    # Mahalle Ekle
    url(r'add-neighborhood/$', CityViews.add_neighborhood, name="mahalle-ekle"),
    url(r'neighborhood-update/(?P<pk>\d+)$', CityViews.update_neighborhood, name='mahalle-fiyati-guncelle'),
    url(r'neighborhoods/$', CityViews.neighborhoods, name='mahalleler'),

    url(r'get-neighborhoods-api/$', APIViews.GetNeighborhood.as_view(), name='api-neighborhoods-list'),

    # Kullanıcı Firma
    url(r'add-company/$', UserViews.add_company, name='kullanıcı firma ekle'),
    url(r'update-company/(?P<pk>\d+)$', UserViews.update_company, name='kullanıcı-firma-guncelle'),

    url(r'delete-company/$', UserViews.company_delete, name='kullanıcı-firma-sil'),

    # Görev
    url(r'select-request/(?P<pk>\d+)$', TaskViews.requests, name='talepler'),
    url(r'add-task/(?P<pk>\d+)$', TaskViews.add_task, name='gorev ata'),
    url(r'completed-task/$', TaskViews.return_completed_task, name='tamamlanan gorevler'),
    url(r'completed-task-api/$', APIViews.GetCompletedTask.as_view(), name='gorevler-api'),

    url(r'active-task/$', TaskViews.return_active_task, name='aktif gorevler'),
    url(r'tasks-canceled/$', TaskViews.return_canceled_task, name='kullanıcı iptal edilen gorevler'),
    url(r'cancel-tasks-api/$', APIViews.GetCanceledTask.as_view(), name='api-iptal-edilen-gorevler'),

    url(r'getTask/(?P<pk>\d+)$', TaskViews.getTask, name='gorev getir'),
    url(r'assign-courier/$', TaskViews.assign_courier, name='kurye sec'),
    url(r'assign-task-other-courier/(?P<pk>\d+)$', TaskViews.other_assign_courier_task, name='yeniden-kurye-ata'),
    url(r'task-detail/(?P<pk>\d+)$', TaskViews.getTaskDetail, name='gorev-durum-detaylari-timeline'),
    url(r'detail/(?P<pk>\d+)(?P<id>\d+)$', TaskViews.getDetailTaskCourier, name='gorev-detay-kurye'),

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
    url(r'User/all-requests/$', RequestViews.company_all_requests, name='kullanici-talepleri'),

    url(r'getRequest/(?P<pk>\d+)$', RequestViews.getRequest, name='talep getir'),

    # Admin ekle
    url(r'add-admin/$', UserViews.add_admin, name='admin-ekle'),
    url(r'change-password/$', UserViews.user_change_password, name='sifre-guncelle'),

    # Profil
    url(r'profile/$', UserViews.users_information, name='profil'),

    # Bildirim
    url(r'get-notifications-api/$', APIViews.GetNotification.as_view(), name='api-notifications'),
    url(r'notifications/$', DashboardViews.notifications, name='bildirimler'),
    url(r'delete-notifications/$', DashboardViews.delete_notification, name='bildirimleri-sil'),

    url(r'make-read-notification/$', DashboardViews.read_notification, name='bildirim-okundu-yap'),

    url(r'api-get-logs/$', APIViews.GetLogs.as_view(), name='api-logs'),
    url(r'logs/$', LogView.logs, name='log'),

    url(r'api-get-company-list/$', APIViews.GetCompany.as_view(), name='api-company-list'),
    url(r'company-list/$', UserViews.companies, name='kullanıcı listesi'),

    url(r'report/$', ReportViews.request_report, name='talep-raporları'),
    url(r'api-get-request-report/$', APIViews.GetRequestReport.as_view(), name='api-talep-rapor'),

    # Ödeme
    url(r'courier-payments/$', EarningPaymentsViews.courier_payment, name='kurye-odemeleri'),
    url(r'pay-premium-courier/(?P<pk>\d+)$', EarningPaymentsViews.pay_premium_courier, name='kurye-prim-ode'),
    url(r'company-payments/$', EarningPaymentsViews.company_earning_info, name='kullanici-odemeleri'),
    url(r'Company/company-payment/$', EarningPaymentsViews.company_payments, name='kullanicinin-odemeleri'),

    url(r'company-paid/(?P<pk>\d+)(?P<year>\d+)(?P<month>\d+)$', EarningPaymentsViews.pay_payment_company,
        name='kullanici-odendi-yap'),
    url(r'payment-company/$', EarningPaymentsViews.payment_company, name='kullanici-payment'),
    url(r'undo-payment-company/(?P<pk>\d+)(?P<year>\d+)(?P<month>\d+)$', EarningPaymentsViews.undo_payment_company,
        name='kullanici-odenmedi-yap'),
    url(r'payment-company-undo/$', EarningPaymentsViews.payment_company_undo, name='kullanici-odeme-geri-al'),

    url(r'prim-limit-list/$', CourierViews.prim_limit_list, name='prim-limit-listesi'),
    url(r'prim-limit-update/(?P<pk>\d+)$', CourierViews.update_courier_prim_limit, name='prim-limit-guncelle'),

]
