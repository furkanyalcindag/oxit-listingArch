from django.conf.urls import url
from django.urls import path

from listArch.Views import OptionViews, CategoryViews, ProductViews, DashboardViews, CompanyViews, APIViews, HomeViews, \
    BlogViews, FileViews, IntroductionViews, UserViews, AboutViews, ListViews, SubscriberViews, BusinessTypeViews, \
    CollectionViews, ProfileViews, StaffViews, ServiceViews, CountryViews

app_name = 'listArch'

urlpatterns = [

    # HOME
    path(r'', HomeViews.base2, name='index'),
    url(r'user-logout/$', UserViews.user_logout, name='logout-user'),
    url(r'contact/$', HomeViews.contact_page, name='anasayfa-iletisim-sayfasi'),
    url(r'about/$', HomeViews.about_page, name='anasayfa-hakkimizda-sayfasi'),

    url(r'category-products/(?P<pk>\d+)$', HomeViews.get_company_products, name='firmanin-urunleri'),
    url(r'product-detail/(?P<slug>[-\w\d]+)/$', HomeViews.product_detail, name='urun-detay'),
    url(r'product-filter-page/(?P<pk>\d+)$', HomeViews.product_filter_page,
        name='urun-filtreleme-sayfasi'),
    url(r'product-search/$', HomeViews.get_product, name='product-search'),
    url(r'search-product-name/$', HomeViews.search_enter_product_name, name='urun-adi-arama'),
    url(r'products/(?P<pk>\d+)$', HomeViews.home_products, name='anasayfa-urunler'),

    url(r'company-info/(?P<pk>\d+)$', HomeViews.get_company_info, name='firma-bilgileri'),

    # Dashboards
    url(r'dashboard/admin-dashboard/$', DashboardViews.admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/user-dashboard/$', DashboardViews.user_dashboard, name='kullanici-dashboard'),
    url(r'dashboard/company-dashboard/$', DashboardViews.company_dashboard, name='firma-dashboard'),
    url(r'dashboard/staff-dashboard/$', DashboardViews.staff_dashboard, name='personel-dashboard'),

    # Option
    url(r'add-option/$', OptionViews.add_option, name='secenek-ekle'),
    url(r'options/$', OptionViews.feature_list, name='secenekler'),
    url(r'option-update/(?P<pk>\d+)$', OptionViews.update_option, name='secenek-guncelle'),
    url(r'option-delete/$', OptionViews.option_delete, name='secenek-sil'),

    url(r'get-option/$', OptionViews.get_option, name='secenek-getir'),
    url(r'get-option-values-desc/$', OptionViews.get_values, name='secenek-degerler-ceviri'),

    url(r'get-option-value/$', OptionViews.get_option_values, name='secenek-degerlerini-getir'),

    # Category
    url(r'add-category/$', CategoryViews.add_category, name='kategori-ekle'),
    url(r'update-category/(?P<pk>\d+)$', CategoryViews.update_category, name='kategori-duzenle'),
    url(r'delete-category/$', CategoryViews.delete_category, name='kategori-sil'),

    url(r'category-list/$', CategoryViews.return_categories, name='kategori-listesi'),

    # Product
    url(r'add-product/$', ProductViews.add_product, name='urun-ekle'),
    url(r'search-product/$', HomeViews.search_product_home, name='urun-ara'),
    url(r'filter-page-search/$', HomeViews.search_product_filter, name='filtreleme-sayfasi-search'),

    url(r'urun-getir/$', ProductViews.get_products, name='urun-getir'),

    url(r'add-product-definition/(?P<pk>\d+)$', ProductViews.add_productDefinition, name='urun-aciklama-ekle'),
    url(r'product-definition-update/(?P<pk>\d+)$', ProductViews.update_productDefinition,
        name='urun-aciklama-guncelle'),

    url(r'product-list/$', ProductViews.product_list, name='urunler'),
    url(r'edit-product/(?P<uuid>[0-9a-f-]+)$', ProductViews.product_edit, name='urun-duzenle'),
    url(r'delete-product/$', ProductViews.product_delete, name='urun-sil'),
    url(r'product-definition-delete/$', ProductViews.product_definition_delete, name='urun-aciklama-sil'),

    url(r'product-image-delete/$', ProductViews.product_image_delete, name='urun-resmi-sil'),
    url(r'delete-product-option/$', ProductViews.product_option_delete, name='urun-secenegi-sil'),
    url(r'get-product-definition/$', ProductViews.get_product_definition, name='urun-aciklamasi-getir'),
    url(r'product-apply-filter/$', HomeViews.filtered_products, name='urun-filtrele'),
    url(r'product-apply-filter-range/$', HomeViews.filtered_products_range, name='urun-filtrele-range'),
    url(r'add-product-graphic/(?P<pk>\d+)$', ProductViews.add_graphic, name='urun-performans-grafigi-ekle'),
    url(r'add-product-chart/(?P<uuid>[0-9a-f-]+)$', ProductViews.add_chart_graphic, name='urune-grafik-ekle'),

    # Company
    url(r'profile/$', UserViews.company_information, name='firma-profil'),

    url(r'add-company/$', CompanyViews.add_company, name='firma-ekle'),
    url(r'company-list/$', CompanyViews.return_companies, name='firma-listesi'),
    url(r'get-api-companies/$', APIViews.GetCompany.as_view(), name='firma-list-api'),

    url(r'get-company/(?P<pk>\d+)$', CompanyViews.getCompany, name='firma-aciklamasi-getir'),
    url(r'update-company/(?P<pk>\d+)$', CompanyViews.update_company, name='firma-düzenle'),
    url(r'company-definition-edit/(?P<pk>\d+)$', CompanyViews.get_company_definition, name='firma-aciklamasi-duzenle'),
    url(r'delete-company/$', CompanyViews.company_delete, name='firma-sil'),
    url(r'company-all-product/$', CompanyViews.return_company_products, name='firmanin-urun-listesi'),
    url(r'category-all-product/(?P<pk>\d+)$', CompanyViews.company_category_products,
        name='firmanin-kategoriye-ait-urunleri'),

    url(r'company-product-detail/(?P<pk>\d+)$', CompanyViews.company_product_detail,
        name='firmanin-urun-detay-sayfasi'),

    url(r'get-company-social-account/(?P<pk>\d+)$', CompanyViews.getSocialAccount,
        name='firma-sosyalMedya-hesap-getir'),
    url(r'get-company-social/(?P<pk>\d+)$', CompanyViews.getSocialMedia,
        name='firma-sosyalMedya-getir'),
    url(r'add-company-definition/(?P<pk>\d+)$', CompanyViews.add_companyDefinition, name='firma-aciklama-ekle'),

    url(r'company-social-edit/$', CompanyViews.edit_social_account,
        name='firma-sosyalMedya-düzenle'),
    url(r'delete-retail/$', CompanyViews.delete_retail, name='magaza-sil'),

    # Blog
    url(r'add-blog/$', BlogViews.add_blog_desc, name='blog-ekle'),
    url(r'profile-add-blog/(?P<pk>\d+)$', BlogViews.add_blog_businessType, name='profile-blog-ekle'),

    url(r'blogs/$', BlogViews.blogs, name='bloglar'),
    url(r'delete-blog/$', BlogViews.delete_blog, name='blog-sil'),
    url(r'update-blog/(?P<pk>\d+)$', BlogViews.update_blog, name='blog-duzenle'),

    # File
    url(r'add-file/$', FileViews.add_file, name='dosya-ekle'),
    url(r'files/$', FileViews.files, name='dosyalar'),
    url(r'file-delete/$', FileViews.delete_file, name='dosya-sil'),
    url(r'file-update/(?P<pk>\d+)$', FileViews.update_file, name='dosya-guncelle'),
    url(r'get-file/$', FileViews.get_file, name='dosya-getir'),

    # Introduction
    url(r'add-element-to-introduction-page/$', IntroductionViews.add_introduction_desc,
        name='tanitim-sayfasina-oge-ekle'),
    url(r'update-introduction-page/(?P<pk>\d+)$', IntroductionViews.update_introduction_desc,
        name='tanitim-sayfasi-duzenle'),
    url(r'introductions/$', IntroductionViews.introduction_products, name='tanitim-urunleri'),
    url(r'add-introduction-page-title/$', IntroductionViews.add_introduction_page_title,
        name='tanitim-urunleri-ana-baslik-ekle'),
    url(r'update-introduction-title/(?P<pk>\d+)$', IntroductionViews.update_introduction_page_title,
        name='tanitim-urunleri-ana-baslik-guncelle'),

    url(r'introduction-page-title/$', IntroductionViews.introduction_title,
        name='tanitim-urunleri-ana-baslik'),
    url(r'title-delete/$', IntroductionViews.delete_introduction_title,
        name='tanitim-urunleri-ana-baslik-sil'),
    url(r'delete-introduction/$', IntroductionViews.delete_introduction, name='tanitim-sil'),

    # About
    url(r'hakkimizda-ekle/$', AboutViews.add_about, name='hakkimizda-ekle'),
    url(r'delete-about/$', AboutViews.delete_about, name='hakkimizda-sil'),
    url(r'about-page/$', AboutViews.about, name='hakkimizda'),

    url(r'add-scrolling-text/$', AboutViews.add_scrolling, name='kayan-yazi-ekle'),
    url(r'scrolling-text/$', AboutViews.scrolling, name='kayan-yazi'),
    url(r'scrolling-delete/$', AboutViews.delete_scrolling, name='kayan-yazi-sil'),

    url(r'update-scrolling-text/(?P<pk>\d+)$', AboutViews.update_scrolling, name='kayan-yazi-guncelle'),

    # Contact
    url(r'update-about/(?P<pk>\d+)$', AboutViews.about_update, name='hakkimizda-guncelle'),
    url(r'add-contact/$', AboutViews.add_contact, name='iletisim-bilgisi-ekle'),
    url(r'update-contact/(?P<pk>\d+)$', AboutViews.update_contact, name='iletisim-bilgisi-guncelle'),
    url(r'contact-page/$', AboutViews.get_contact, name='iletisim-bilgisi'),
    url(r'contact-delete/$', AboutViews.delete_contact, name='iletisim-bilgisi-sil'),

    # Kullanıcı
    url(r'register-user/$', UserViews.register_customer, name='kullanici-kaydet'),
    url(r'login-user/$', UserViews.user_login, name='kullanici-giris-yap'),
    url(r'lists-user/$', UserViews.user_lists, name='kullanici-listesi'),
    url(r'user-listing/$', UserViews.user_listing, name='kullanici-listeleri'),
    url(r'user-company-update/$', UserViews.user_company_update, name='kullanici-firma-bilgileri-guncelle'),

    # Header
    url(r'add-header-text/$', AboutViews.add_header_text, name='ust-menu-yazi-ekle'),
    url(r'header-text/$', AboutViews.headerText, name='ust-menu-yazi'),
    url(r'update-headerText/(?P<pk>\d+)$', AboutViews.update_headerText, name='ust-menu-yazi-guncelle'),
    url(r'headerT-text-delete/$', AboutViews.delete_headerText, name='ust-menu-yazi-sil'),

    # list
    url(r'add-list/$', ListViews.addList, name='liste-olustur'),
    url(r'list/$', ListViews.list, name='listele'),

    url(r'delete-list/$', ListViews.delete_list, name='liste-sil'),
    url(r'list-detail/(?P<pk>\d+)$', ListViews.list_detail, name='liste-detay'),
    url(r'create-sheet-list/(?P<pk>\d+)$', ListViews.print_list_page, name='liste-sayfasi-olustur'),

    url(r'add-product-to-list/(?P<product_id>\d+)/(?P<list_id>\d+)$', ListViews.add_product_list,
        name='kullanici-listeye-urun-ekle'),
    url(r'remove-product-to-list/$', ListViews.remove_product_list, name='kullanici-listeden-urun-cikar'),

    # Subscribe
    url(r'add-subscriber/$', SubscriberViews.add_subscriber, name='abone-ekle'),
    url(r'approved-subscriber/$', SubscriberViews.approve_subscriber, name='abone-onayla'),
    url(r'get-api-subcriber/$', APIViews.GetSubscriber.as_view(), name='abone-list-api'),
    url(r'list-subscriber/$', SubscriberViews.subscriber_list, name='abone-listesi'),

    # businessType
    url(r'add-profile-name/$', BusinessTypeViews.add_businessType, name='profil-adi-ekle'),
    url(r'delete-business-type/$', BusinessTypeViews.delete_business_type, name='profil-adi-sil'),

    url(r'error/$', HomeViews.error_page, name='404-sayfasi'),
    url(r'404/$', AboutViews.admin_error_page, name='admin-error-sayfasi'),

    # koleksiyon
    url(r'create-collection/$', CollectionViews.add_collection, name='koleksiyon-kaydet'),
    url(r'get-collection/$', CollectionViews.get_collection, name='koleksiyon-getir'),

    url(r'add-collection-product/$', CollectionViews.add_product_to_collection, name='koleksiyona-urun-ekle'),
    url(r'add-collection-company/(?P<pk>\d+)$', CollectionViews.add_collection_company, name='firmaya-koleksiyon-ekle'),

    # Profile
    url(r'profile-add/$', ProfileViews.add_profile, name='profil-kaydet'),
    url(r'profile-get-api/$', APIViews.GetProfile.as_view(), name='profile-list-api'),
    url(r'profiller/$', ProfileViews.profile_list, name='profil-listesi'),
    url(r'delete/$', ProfileViews.profile_delete, name='profili-sil'),

    url(r'profile-page/$', HomeViews.profile_page, name='profile-page'),
    url(r'profile-page-info/$', HomeViews.profile_info, name='profile-page-info'),
    url(r'blog-page/$', HomeViews.blog_page, name='blog-page'),

    # Staff
    url(r'add-staff/$', StaffViews.register_staff, name='personel-ekle'),
    url(r'staff/$', StaffViews.staff, name='personeller'),
    url(r'staff-passive/$', StaffViews.passive_staff, name='personel-pasif-et'),
    url(r'staff-activate/$', StaffViews.active_staff, name='aktif-et-personel'),

    # Service
    url(r'add-service/$', ServiceViews.add_service, name='hizmet-ekle'),
    url(r'delete-service/$', ServiceViews.delete_service, name='hizmet-sil'),

    # Country-City
    url(r'add-country-city/$', CountryViews.add_country, name='ulke-sehir-ekle'),
    url(r'countries/$', CountryViews.countries, name='ulkeler'),

]
