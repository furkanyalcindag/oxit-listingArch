from django.conf.urls import url

from listArch.Views import OptionViews, CategoryViews, ProductViews, DashboardViews, CompanyViews, APIViews

app_name = 'listArch'

urlpatterns = [

    # Dashboards
    url(r'dashboard/admin-dashboard/$', DashboardViews.admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/user-dashboard/$', DashboardViews.user_dashboard, name='kullanici-dashboard'),
    url(r'dashboard/company-dashboard/$', DashboardViews.company_dashboard, name='firma-dashboard'),

    # Option
    url(r'add-option/$', OptionViews.add_option, name='secenek-ekle'),
    url(r'options/$', OptionViews.feature_list, name='secenekler'),
    url(r'option-update/(?P<pk>\d+)$', OptionViews.update_option, name='secenek-guncelle'),

    url(r'get-option/$', OptionViews.get_option, name='secenek-getir'),
    url(r'get-option-value/$', OptionViews.get_option_values, name='secenek-degerlerini-getir'),

    # Category
    url(r'add-category/$', CategoryViews.add_category, name='kategori-ekle'),
    url(r'update-category/(?P<pk>\d+)$', CategoryViews.update_category, name='kategori-duzenle'),
    url(r'update-category/$', CategoryViews.delete_category, name='kategori-sil'),

    url(r'category-list/$', CategoryViews.return_categories, name='kategori-listesi'),

    # Product
    url(r'add-product/$', ProductViews.add_product, name='urun-ekle'),
    url(r'product-list/$', ProductViews.product_list, name='urunler'),
    url(r'edit-product/(?P<pk>\d+)$', ProductViews.product_edit, name='urun-duzenle'),

    # Company
    url(r'add-company/$', CompanyViews.add_company, name='firma-ekle'),
    url(r'company-list/$', CompanyViews.return_companies, name='firma-listesi'),
    url(r'get-api-companies/$', APIViews.GetCompany.as_view(), name='firma-list-api'),
    url(r'get-company/(?P<pk>\d+)$', CompanyViews.getCompany, name='firma-aciklamasi-getir'),
    url(r'update-company/(?P<pk>\d+)$', CompanyViews.update_company, name='firma-düzenle'),
    url(r'get-company-social-account/(?P<pk>\d+)$', CompanyViews.getSocialAccount, name='firma-sosyalMedya-hesap-getir'),
    url(r'get-company-social/(?P<pk>\d+)$', CompanyViews.getSocialMedia,
        name='firma-sosyalMedya-getir'),

    url(r'company-social-edit/$', CompanyViews.edit_social_account,
        name='firma-sosyalMedya-düzenle'),

]
