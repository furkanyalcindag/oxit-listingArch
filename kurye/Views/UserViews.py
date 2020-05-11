from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User

from kurye.Forms.CompanyForm import CompanyForm
from kurye.Forms.CustomerForm import CustomerForm

from kurye.Forms.UserForm import UserForm
from kurye.Forms.ProfileForm import ProfileForm
from kurye.models.Courier import Courier
from kurye.models.Customer import Customer
from kurye.models.Company import Company
from kurye.models.Profile import Profile


def add_courier(request):
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

    return render(request, 'Courier/add-courier.html', {'user_form': user_form, 'profile_form': profile_form})


def list_courier(request):
    couriers = Courier.objects.all()
    return render(request, 'Courier/courier-list.html', {'couriers': couriers})


def add_customer(request):
    customer_form = CustomerForm()

    if request.method == 'POST':

        customer_form = CustomerForm(request.POST)

        if customer_form.is_valid():

            customer = Customer(customer=customer_form.cleaned_data['customer'],
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


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'CustomerCompany/customer-list.html', {'customers': customers})


def add_company(request):
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
            profile.isContract = profile_form.cleaned_data['isContract']
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

            return redirect('kurye:kullanıcı-firma ekle')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'Company/add-company.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'company_form': company_form})


def company_list(request):
    companies = Company.objects.all()
    return render(request, 'Company/company-list.html', {'companies': companies})
