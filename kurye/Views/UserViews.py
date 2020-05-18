from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from django.urls import resolve

from accounts.forms import ResetPassword
from kurye.Forms.CompanyForm import CompanyForm
from kurye.Forms.CustomerForm import CustomerForm
from kurye.Forms.ProfileUpdateForm import ProfileUpdateForm

from kurye.Forms.UserForm import UserForm
from kurye.Forms.ProfileForm import ProfileForm
from kurye.Forms.UserUpdateForm import UserUpdateForm
from kurye.models.Courier import Courier
from kurye.models.Customer import Customer
from kurye.models.Company import Company
from kurye.models.Profile import Profile
from kurye.services import general_methods


# Profile
@login_required
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
            user.is_active = True
            user.save()
            profile_form.save()
            if groups[0].name == 'Admin' or groups[0].name == 'Kullanıcı':
                company_form.save()

            messages.success(request, 'Profil Bilgileriniz Başarıyla Güncellenmiştir.')

            return redirect('kurye:profil')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'User/kullanici-bilgileri.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'ilce': profile.district,
                   'company_form': company_form})


# Admin Kurye Ekleme
@login_required
def add_courier(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    profile_form = ProfileForm()
    user_form = UserForm()

    if request.method == 'POST':

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)

        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid() and user_form.is_valid():

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
                              )
            profile.isActive = True
            profile.save()

            courier = Courier(courier=profile)

            courier.save()

            subject, from_email, to = 'MotoKurye Kurye Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong><a href="http://127.0.0.1:8000/">MotoKurye.net</a></p>'
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
                  {'user_form': user_form, 'profile_form': profile_form})


def user_change_password(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        form = ResetPassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Şifreniz başarıyla değiştirilmiştir.')
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
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)

    if request.method == 'POST':

        customer_form = CustomerForm(request.POST)

        if customer_form.is_valid():

            customer = Customer(company=company, customer=customer_form.cleaned_data['customer'],
                                address=customer_form.cleaned_data['address'],
                                phone=customer_form.cleaned_data['phone'],
                                city=customer_form.cleaned_data['city'],
                                district=customer_form.cleaned_data['district'],
                                email=customer_form.cleaned_data['email']
                                )
            customer.save()

            messages.success(request, 'Müşteri Başarıyla Kayıt Edilmiştir.')

            return redirect('kurye:musteri ekle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'CustomerCompany/add-customer.html',
                  {'customer_form': customer_form})


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
    customers_of_company = Customer.objects.filter(company=company)
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

                              )
            profile.isActive = True
            profile.save()
            company = Company(profile=profile, companyName=company_form.cleaned_data['companyName'],
                              taxName=company_form.cleaned_data['taxName'],
                              taxNumber=company_form.cleaned_data['taxNumber'], )
            company.save()

            subject, from_email, to = 'MotoKurye Kullanıcı Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/">MotoKurye.net</a></p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Kullanıcı Başarıyla Kayıt Edilmiştir.')

            return redirect('kurye:kullanıcı firma ekle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'Company/add-company.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'company_form': company_form})


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

            subject, from_email, to = 'MotoKurye Admin Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/">MotoKurye.net</a></p>'
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
def customer_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    customer = Customer.objects.get(pk=pk)
    customer.delete()
    messages.success(request, 'Müşteri Başarıyla Silindi')
    return redirect('kurye:musteri listesi')
