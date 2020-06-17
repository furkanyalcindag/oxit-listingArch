from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from accounts.forms import ResetPassword
from kurye.Forms.CompanyForm import CompanyForm
from kurye.Forms.CourierForm import CourierForm
from kurye.Forms.CustomerForm import CustomerForm
from kurye.Forms.CustomerUpdateForm import CustomerUpdateForm
from kurye.Forms.ProfileUpdateForm import ProfileUpdateForm
from kurye.Forms.UserForm import UserForm
from kurye.Forms.ProfileForm import ProfileForm
from kurye.Forms.UserUpdateForm import UserUpdateForm
from kurye.models import Neighborhood
from kurye.models.City import City
from kurye.models.Courier import Courier
from kurye.models.Customer import Customer
from kurye.models.Company import Company
from kurye.models.Personal import Personal
from kurye.models.Profile import Profile
from kurye.services import general_methods
from kurye.services.general_methods import save_log


@login_required
# Profile
def users_information(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    user = User.objects.get(pk=current_user.pk)
    groups = Group.objects.filter(user=user)
    company_form = None
    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile = Profile.objects.get(user=user)
    profile_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
    if groups[0].name == 'Admin' or groups[0].name == 'Kullanıcı':
        company = Company.objects.get(profile=profile)
        company_form = CompanyForm(request.POST or None, instance=company)
    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():

            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.email = user_form.cleaned_data['email']
            user.is_active = True
            user.save()
            profile_form.save()
            if groups[0].name == 'Admin' or groups[0].name == 'Kullanıcı':
                company_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı ' + \
                          groups[0].name + ' profilini günceledi</p>'

            save_log(profile.pk, log_content)

            return redirect('kurye:profil')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'User/kullanici-bilgileri.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district,
                   'company_form': company_form, 'profile_image': profile.profileImage})


# Admin Kurye Ekleme
@login_required
def add_courier(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    profile_form = ProfileForm()
    user_form = UserForm()
    current_user = request.user
    current_profile = Profile.objects.get(user=current_user)
    courier_form = CourierForm()
    cities = City.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)

        profile_form = ProfileForm(request.POST, request.FILES)
        courier_form = CourierForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid() and courier_form.is_valid():

            user = user_form.save(commit=False)
            group = Group.objects.get(name='Kurye')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.username = user.email
            user.save()

            profile = Profile(user=user, tc=profile_form.cleaned_data['tc'],
                              mobilePhone=profile_form.cleaned_data['mobilePhone'],
                              profileImage=profile_form.cleaned_data['profileImage'],
                              city=profile_form.cleaned_data['city'],
                              district=profile_form.cleaned_data['district'],
                              neighborhood=profile_form.cleaned_data['neighborhood'],
                              address=profile_form.cleaned_data['address']
                              )
            profile.isActive = True
            profile.save()

            courier = Courier(courier=profile, type=courier_form.cleaned_data['type'])

            courier.save()

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">Kurye</strong> eklendi.</p>'

            save_log(current_profile.pk, log_content)

            subject, from_email, to = 'GVERCİN Kurye Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong><a href="http://127.0.0.1:8000/">gvercin.com</a></p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Kurye Başarıyla Kayıt Edilmiştir.')

            return redirect('kurye:kurye ekle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'Courier/add-courier.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'courier_form': courier_form,
                   'cities': cities})


# Kurye Güncelle
@login_required
def update_courier(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    courier = Courier.objects.get(pk=pk)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=courier.courier)
    user_form = UserUpdateForm(request.POST or None, instance=courier.courier.user)
    courier_form = CourierForm(request.POST or None, instance=courier)
    user = request.user
    current_profile = Profile.objects.get(user=user)
    company=Company.objects.get(profile=current_profile)

    if request.method == 'POST':

        if profile_form.is_valid() and user_form.is_valid() and courier_form.is_valid():

            user_form.save()
            profile_form.save()
            courier_form.save()

            log_content = '<p><strong style="color:red">' + courier.courier.user.first_name + ' ' + courier.courier.user.last_name + '</strong> adlı <strong style="color:red">Kurye </strong> guncellendi.</p>'

            save_log(current_profile.pk, log_content)

            messages.success(request, 'Kurye Başarıyla Güncellenmiştir.')

            return redirect('kurye:kurye listesi')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    cities = City.objects.all()

    return render(request, 'Courier/add-courier.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'courier_form': courier_form,
                   'ilce': courier.courier.district, 'mahalle': courier.courier.neighborhood, 'cities': cities})


@login_required()
def user_change_password(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    current_profile = Profile.objects.get(user=user)
    groups = Group.objects.filter(user=user)
    if request.method == 'POST':
        form = ResetPassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Şifreniz başarıyla değiştirilmiştir.')

            log_content = '<p><strong style="color:red">' + current_profile.user.first_name + ' ' + current_profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                          groups[0].name + '</strong> şifresini güncelledi.</p>'

            save_log(current_profile.pk, log_content)

            return redirect('kurye:profil')
        else:
            for error in form.errors.keys():
                messages.warning(request, form.errors[error])

    else:
        form = ResetPassword(request.user)
    return render(request, 'User/kullanici-sifre-guncelle.html', {'form': form})


# Kullanıcı Müşteri Ekle
@login_required
def add_customer(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    customer_form = CustomerForm()
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    cities = City.objects.all()
    if request.method == 'POST':
        city_id = request.POST['city']
        city = City.objects.get(pk=city_id)
        customer_form = CustomerForm(request.POST)

        if customer_form.is_valid():

            customer = Customer(company=company, customer=customer_form.cleaned_data['customer'],
                                address=customer_form.cleaned_data['address'],
                                phone=customer_form.cleaned_data['phone'],
                                city=city,
                                district=customer_form.cleaned_data['district'],
                                email=customer_form.cleaned_data['email'],
                                neighborhood=customer_form.cleaned_data['neighborhood'],
                                )
            customer.save()

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                          groups[0].name + ', ' + customer.customer + '</strong> adında müşteri ekledi.</p>'

            save_log(profile.pk, log_content)

            messages.success(request, 'Müşteri Başarıyla Kayıt Edilmiştir.')

            return redirect('kurye:musteri ekle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'CustomerCompany/add-customer.html',
                  {'customer_form': customer_form, 'cities': cities})


# Kullanıcı Müşteri Güncelle
@login_required
def update_customer(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    customer = Customer.objects.get(pk=pk)

    customer_form = CustomerUpdateForm(request.POST or None, instance=customer)
    cities = City.objects.all()
    neighborhood_id = customer.neighborhood
    neighborhood = Neighborhood.objects.get(neighborhood_name=neighborhood_id)

    if request.method == 'POST':
        if customer_form.is_valid():
            if customer.company.profile == profile:

                city_id = request.POST['city']
                city = City.objects.get(pk=city_id)

                customer_form.save()

                log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                              groups[
                                  0].name + ', ' + customer.customer + '</strong> adında müşteri bilgilerini güncelledi.</p>'

                save_log(profile.pk, log_content)

                messages.success(request, 'Müşteri Bilgileri Başarıyla Güncellenmiştir.')

                return redirect('kurye:musteri listesi')
            else:
                messages.warning(request, 'Güncelleştirme Yapamazsınız.')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'CustomerCompany/add-customer.html',
                  {'customer_form': customer_form, 'cities': cities, 'ilce': customer.district,
                   'mahalle': customer.neighborhood})


# PERSONEL EKLE (Admin)
@login_required
def add_personal(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user_form = UserForm()
    profile_form = ProfileForm()
    cities = City.objects.all()
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    company = Company.objects.get(profile_id=profile.pk)

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)

        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            group = Group.objects.get(name='Personel')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.username = user.email
            user.save()

            profile_personel = Profile(user=user, profileImage=profile_form.cleaned_data['profileImage'],
                                       mobilePhone=profile_form.cleaned_data['mobilePhone'])
            profile_personel.isActive = True
            profile_personel.save()

            personal = Personal(profile=profile_personel, company=company)
            personal.save()

            log_content = '<p> Admin <strong style="color:red">' + user.first_name + ' ' + user.last_name + '</strong> adında personel ekledi.</p>'

            save_log(profile.pk, log_content)

            messages.success(request, 'Personel Bilgileri Başarıyla Kayıt Edilmiştir.')

            return redirect('kurye:personel-listesi')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'User/add-personal.html',
                  {'user_form': user_form, 'profile_form': profile_form})


# Personel Listesi (Admin)
def personel_list(request):
    personals = Personal.objects.filter(profile__isActive=True).filter(profile__user__groups__name='Personel')
    return render(request, 'User/personal-list.html', {'personals': personals})


@login_required
def personal_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    personal = Personal.objects.get(pk=pk)
    personal.profile.isActive = False
    personal.profile.save()

    log_content = '<p><strong style="color:red">' + user.first_name + ' ' + user.last_name + '</strong> adlı <strong style="color:red">Admin, ' + personal.profile.user.first_name + ' ' + personal.profile.user.last_name + ' </strong> adlı personeli, personellerinden kaldırdı.</p>'

    save_log(profile.pk, log_content)

    messages.success(request, 'Personel Başarıyla Silindi')
    return redirect('kurye:personel-listesi')


# KULLANICIYA AİT Müşteri Listesi
@login_required
def customer_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    customers_of_company = Customer.objects.filter(isActive=True).filter(company_id=company.pk)
    return render(request, 'CustomerCompany/customer-list.html', {'customers': customers_of_company})


# Kullanıcı EKLE
@login_required
def add_company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    profile_form = ProfileForm()
    user_form = UserForm()
    company_form = CompanyForm()
    user = request.user
    current_profile = Profile.objects.get(user=user)

    if request.method == 'POST':

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)

        profile_form = ProfileForm(request.POST, request.FILES)
        company_form = CompanyForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid() and company_form.is_valid():

            user = user_form.save(commit=False)
            group = Group.objects.get(name='Kullanıcı')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.username = user.email
            user.save()

            profile = Profile(user=user, tc=profile_form.cleaned_data['tc'],
                              profileImage=profile_form.cleaned_data['profileImage'],
                              mobilePhone=profile_form.cleaned_data['mobilePhone'],
                              address=profile_form.cleaned_data['address'],
                              city=profile_form.cleaned_data['city'],
                              phone=profile_form.cleaned_data['phone'],
                              district=profile_form.cleaned_data['district'],
                              neighborhood=profile_form.cleaned_data['neighborhood']

                              )
            profile.isActive = True
            profile.save()
            company = Company(profile=profile, companyName=company_form.cleaned_data['companyName'],
                              taxName=company_form.cleaned_data['taxName'],
                              taxNumber=company_form.cleaned_data['taxNumber'], )
            company.save()

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">Kullanıcı </strong> eklendi.</p>'

            save_log(current_profile.pk, log_content)

            subject, from_email, to = 'GVERCİN Kullanıcı Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/">gvercin.com</a></p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Firma Başarıyla Kayıt Edilmiştir.')

            return redirect('kurye:kullanıcı firma ekle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    cities = City.objects.all()

    return render(request, 'Company/add-company.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'company_form': company_form,
                   'ilce': current_profile.district, 'mahalle': current_profile.neighborhood, 'cities': cities})


# Kullanıcı Firma Güncelle
@login_required
def update_company(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company = Company.objects.get(pk=pk)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=company.profile)
    user_form = UserUpdateForm(request.POST or None, instance=company.profile.user)
    company_form = CompanyForm(request.POST or None, instance=company)
    user = request.user
    current_profile = Profile.objects.get(user=user)

    if request.method == 'POST':

        if profile_form.is_valid() and user_form.is_valid() and company_form.is_valid():

            user_form.save()
            profile_form.save()
            company_form.save()

            log_content = '<p><strong style="color:red">' + company.profile.user.first_name + ' ' + company.profile.user.last_name + ' ' + company.companyName + '' + '</strong> adlı <strong style="color:red">Kullanıcı </strong> guncellendi.</p>'

            save_log(current_profile.pk, log_content)

            messages.success(request, 'Firma Başarıyla Güncellenmiştir.')

            return redirect('kurye:kullanıcı listesi')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')
    cities = City.objects.all()

    return render(request, 'Company/company-update.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'company_form': company_form,
                   'ilce': company.profile.district, 'mahalle': company.profile.neighborhood, 'cities': cities})


# Admin Ekle
def add_admin(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    profile_form = ProfileForm()
    user_form = UserForm()
    company_form = CompanyForm()

    if request.method == 'POST':

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)

        profile_form = ProfileForm(request.POST, request.FILES)
        company_form = CompanyForm(request.POST)

        if profile_form.is_valid() and user_form.is_valid() and company_form.is_valid():

            user = user_form.save(commit=False)
            group = Group.objects.get(name='Admin')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.username = user.email
            user.save()

            profile = Profile(user=user, tc=profile_form.cleaned_data['tc'],
                              profileImage=profile_form.cleaned_data['profileImage'],
                              mobilePhone=profile_form.cleaned_data['mobilePhone'],
                              address=profile_form.cleaned_data['address'],
                              city=profile_form.cleaned_data['city'],
                              phone=profile_form.cleaned_data['phone'],
                              district=profile_form.cleaned_data['district'],

                              )
            profile.isActive = True
            profile.save()
            company = Company(profile=profile, companyName=company_form.cleaned_data['companyName'],
                              taxName=company_form.cleaned_data['taxName'],
                              taxNumber=company_form.cleaned_data['taxNumber'], )
            company.save()

            subject, from_email, to = 'GVRCİN Admin Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/">gvercin.com</a></p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Admin Başarıyla Kayıt Edilmiştir.')

            return redirect('accounts:login')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'User/add-admin.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'company_form': company_form})


# Admin Kullanıcı Listesi
@login_required
def company_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    companies = Company.objects.all().filter(~Q(profile_id=profile.pk))
    return render(request, 'Company/company-list.html', {'companies': companies})


# Kullanıcı Müşteri Silme
@login_required
def customer_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        pk = request.POST['customer_id']
        user = request.user
        profile = Profile.objects.get(user=user)
        customer = Customer.objects.get(pk=pk)
        customer.isActive = False
        customer.save()

        log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">Kullanıcı, ' + customer.customer + ' </strong> adlı Müşteriyi sildi.</p>'

        save_log(profile.pk, log_content)

        messages.success(request, 'Müşteri Başarıyla Silindi')
    return redirect('kurye:musteri listesi')


# kullanıcılar datatable
def companies(request):
    return render(request, 'Company/company-list.html')


@login_required
def personal_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        pk = request.POST['personal_id']
        user = request.user
        profile = Profile.objects.get(user=user)
        personal = Personal.objects.get(pk=pk)
        personal.profile.isActive = False
        personal.profile.save()

        log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong>  <strong style="color:red"> , ' + personal.profile.user.first_name + '' + personal.profile.user.last_name + ' </strong> adlı personeli sildi.</p>'

        save_log(profile.pk, log_content)

    return redirect('kurye:personel-listesi')


@login_required
def company_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            user = request.user
            profile = Profile.objects.get(user=user)
            company_id = request.POST['company_id']
            company = Company.objects.get(pk=company_id)
            company.profile.isActive = False
            company.profile.save()

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong>  <strong style="color:red"> , ' + company.companyName + ' </strong> adlı firmayı sildi.</p>'

            save_log(profile.pk, log_content)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def courier_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            user = request.user
            profile = Profile.objects.get(user=user)
            courier_id = request.POST['courier_id']
            courier = Courier.objects.get(pk=courier_id)
            courier.courier.isActive = False
            courier.courier.save()

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong>  <strong style="color:red"> , ' + courier.courier.user.first_name + '' + courier.courier.user.last_name + ' </strong> adlı firmayı sildi.</p>'

            save_log(profile.pk, log_content)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
