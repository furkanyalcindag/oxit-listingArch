from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from listArch.Forms.CompanyForm import CompanyForm
from listArch.Forms.CompanySocialForm import CompanySocialForm
from listArch.Forms.UserForm import UserForm
from listArch.Forms.UserUpdateForm import UserUpdateForm
from listArch.models import Company, SocialMedia, City
from listArch.models.CompanySocialAccount import CompanySocialAccount
from listArch.serializers.CompanySerializer import CompanySerializer
from listArch.serializers.CompanySocialSerializer import CompanySocialSerializer
from listArch.serializers.SocialMediaSerializer import SocialMediaSerializer
from listArch.services import general_methods
from listArch.services.general_methods import save_log


# Firma Ekle
def add_company(request):
    company_form = CompanyForm()
    user_form = UserForm()
    i = 0
    if request.method == 'POST':
        company_form = CompanyForm(request.POST or None, request.FILES or None)

        try:
            data = request.POST.copy()
            data['username'] = data['email']
            user_form = UserForm(data)

            if company_form.is_valid() and user_form.is_valid():

                user = user_form.save(commit=False)

                group = Group.objects.get(name='Firma')
                user2 = user_form.save()
                password = User.objects.make_random_password()
                user.set_password(password)
                user2.groups.add(group)
                user.is_active = True
                user.username = user.email
                user.save()

                social_row = int(request.POST['social_row'])

                company = Company(user=user, name=company_form.cleaned_data['name'],
                                  description=company_form.cleaned_data['description'],
                                  address=company_form.cleaned_data['address'],
                                  file=company_form.cleaned_data['file'],
                                  phone=company_form.cleaned_data['phone'],
                                  website=company_form.cleaned_data['website'],
                                  country=company_form.cleaned_data['country'],
                                  city=company_form.cleaned_data['city'],
                                  map=company_form.cleaned_data['map'],
                                  )
                company.save()

                while i <= social_row:
                    social = SocialMedia(name=request.POST['company_social[' + str(i) + '][name]'],
                                         link=request.POST['company_social[' + str(i) + '][link]'])
                    social.save()
                    company_social = CompanySocialAccount(company=company, social_account=social)
                    company_social.save()
                    i = i + 1

                    subject, from_email, to = 'OXIT Kullanıcı Giriş Bilgileri', 'burcu.dogan@oxityazilim.com', user2.email
                    text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
                    html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/">oxit.com.tr</a></p>'
                    html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
                    html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    messages.success(request, 'Firma Bilgileri Başarıyla Kayıt Edilmiştir.')
                    return redirect('listArch:firma-ekle')

            else:
                messages.success(request, 'Alanları Kontrol Ediniz.')

        except Exception as e:
            print(e)

    return render(request, 'company/add-company.html', {'company_form': company_form, 'user_form': user_form})


def return_companies(request):
    return render(request, 'company/company-list.html')


@api_view()
def getCompany(request, pk):
    company = Company.objects.filter(pk=pk)
    data = CompanySerializer(company, many=True)

    responseData = {}
    responseData['company'] = data.data
    responseData['company'][0]
    return JsonResponse(responseData, safe=True)


# Firma Düzenle
@login_required
def update_company(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company = Company.objects.get(pk=pk)
    user_form = UserUpdateForm(request.POST or None, instance=company.user)
    company_form = CompanyForm(request.POST or None, instance=company)
    social_accounts = CompanySocialAccount.objects.filter(company=company)
    i = 0

    if request.method == 'POST':

        try:
            if user_form.is_valid() and company_form.is_valid():
                company.user.first_name = user_form.cleaned_data['first_name']
                company.user.last_name = user_form.cleaned_data['last_name']
                company.user.email = user_form.cleaned_data['email']
                company.user.username = user_form.cleaned_data['email']
                company.user.is_active = True
                company.user.save()
                company_form.save()

                social_row = int(request.POST['row_number'])

                if social_accounts.count() > 0:
                    i = social_row
                    while i < social_accounts.count():
                        social = SocialMedia(name=request.POST['company_social[' + str(i + 1) + '][name]'],
                                     link=request.POST['company_social[' + str(i + 1) + '][link]'])
                        social.save()
                        company_social = CompanySocialAccount(company=company, social_account=social)
                        company_social.save()
                        i = i + 1
                else:
                    i=social_accounts.count()
                    while i <= social_row:
                        social = SocialMedia(name=request.POST['company_social[' + str(i) + '][name]'],
                                 link=request.POST['company_social[' + str(i) + '][link]'])
                        social.save()
                        company_social = CompanySocialAccount(company=company, social_account=social)
                        company_social.save()
                        i = i + 1

                messages.success(request, 'Firma Başarıyla Güncellenmiştir.')
                return redirect('listArch:firma-listesi')
            else:
                messages.warning(request, 'Alanları Kontrol Edin.')
        except Exception as e:
            print(e)

    return render(request, 'company/update-company.html',
                  {'company_form': company_form, 'user_form': user_form, 'social_accounts': social_accounts,
                   'loop': social_accounts.count()
                   })


@api_view()
def getSocialAccount(request, pk):
    socialAccount = SocialMedia.objects.filter(pk=pk)
    data = SocialMediaSerializer(socialAccount, many=True)

    responseData = {}
    responseData['socialMedia'] = data.data
    responseData['socialMedia'][0]
    return JsonResponse(responseData, safe=True)


@api_view()
def getSocialMedia(request, pk):
    company_accounts = CompanySocialAccount.objects.filter(company=Company.objects.get(pk=pk))
    data = CompanySocialSerializer(company_accounts, many=True)

    responseData = {}
    responseData['company_accounts'] = data.data
    responseData['company_accounts'][0]
    return JsonResponse(responseData, safe=True)


@api_view(http_method_names=['POST'])
def edit_social_account(request):
    if request.POST:
        try:

            social_account_id = request.POST.get('social_id')
            social_accounts = SocialMedia.objects.filter(pk=social_account_id)

            company_accounts = CompanySocialAccount.objects.filter(social_account=social_accounts[0])

            name = request.POST['name']
            link = request.POST['link']

            for social_account in social_accounts:

                social_account.link = link
                social_account.name = name
                social_account.save()
                for company_account in company_accounts:
                    company_account.social_account = social_account
                    company_account.save()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
