import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from listArch.Forms.CompanyForm import CompanyForm
from listArch.Forms.UserCompanyForm import UserCompanyForm
from listArch.Forms.UserUpdateForm import UserUpdateForm
from listArch.models import Company, SocialMedia, City, Product, Category, ProductFile, ProductOptionValue, Option, \
    OptionValue, CompanyRetail
from listArch.models.CompanyDefinition import CompanyDefinition
from listArch.models.CompanySocialAccount import CompanySocialAccount
from listArch.models.Definition import Definition
from listArch.models.DefinitionDescription import DefinitionDescription
from listArch.models.ProductDefinition import ProductDefinition
from listArch.models.ProductImage import ProductImage
from listArch.serializers.CompanySerializer import CompanySerializer
from listArch.serializers.CompanySocialSerializer import CompanySocialSerializer
from listArch.serializers.SocialMediaSerializer import SocialMediaSerializer
from listArch.services import general_methods
from oxiterp.settings.base import EMAIL_HOST_USER


# Firma Ekle
def add_company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company_form = CompanyForm(initial={'date': datetime.datetime.today().strftime("%d-%b-%Y")})
    user_form = UserCompanyForm()

    company = Company.objects.all()
    if request.method == 'POST':
        company_form = CompanyForm(request.POST or None, request.FILES or None)

        try:
            data = request.POST.copy()
            data['username'] = data['email']
            user_form = UserCompanyForm(data)

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

                count = request.POST['social_row']
                count = count.split(',')
                array = []
                for count in count:
                    array.append(count)

                company = Company(user=user, name=company_form.cleaned_data['name'],
                                  userDescription=company_form.cleaned_data['userDescription'],
                                  address=company_form.cleaned_data['address'],
                                  logo=company_form.cleaned_data['logo'],
                                  phone=company_form.cleaned_data['phone'],
                                  website=company_form.cleaned_data['website'],
                                  country=company_form.cleaned_data['country'],
                                  map=company_form.cleaned_data['map'],
                                  noOfEmployees=company_form.cleaned_data['noOfEmployees'],
                                  annualSales=company_form.cleaned_data['annualSales'],
                                  date=company_form.cleaned_data['date'],
                                  address_link=company_form.cleaned_data['address_link'],
                                  business_type=company_form.cleaned_data['business_type'],
                                  isSponsor=company_form.cleaned_data['isSponsor']

                                  )
                company.save()

                for service in company_form.cleaned_data['service']:
                    company.service.add(service)

                if request.POST['retail'] == 'news':
                    name = request.POST['retail-name']
                    logo = request.POST['retail-logo']
                    retail_company = CompanyRetail(company=company, name=name, logo=logo)
                    retail_company.save()
                    company.retail = retail_company
                    company.save()
                elif request.POST['retail'] == '':
                    print('mağaza yok')
                else:
                    retail = Company.objects.get(pk=int(request.POST['retail']))
                    retail_company = CompanyRetail(company=retail, name=retail.name, logo=retail.logo)
                    retail_company.save()

                if request.POST['company_social[0][name]'] != "":
                    for i in array:
                        social = SocialMedia(name=request.POST['company_social[' + str(i) + '][name]'],
                                             link=request.POST['company_social[' + str(i) + '][link]'])
                        social.save()
                        company_social = CompanySocialAccount(company=company, social_account=social)
                        company_social.save()

                subject, from_email, to = 'OXIT Kullanıcı Giriş Bilgileri', EMAIL_HOST_USER, user2.email
                text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
                html_content = '<p> <strong>Site adresi:</strong> <a href="http://http://185.86.4.199:8082/">oxit.com.tr</a></p>'
                html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
                html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Firma Bilgileri Başarıyla Kayıt Edilmiştir.')
                return redirect('listArch:firma-ekle')
            else:
                messages.warning(request, 'Alanları Kontrol Ediniz.')

        except Exception as e:
            print(e)

    return render(request, 'company/add-company.html',
                  {'company_form': company_form, 'user_form': user_form, 'company': company,
                   })


def return_companies(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
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
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company = Company.objects.get(pk=pk)
    user_form = UserUpdateForm(request.POST or None, instance=company.user)
    company_form = CompanyForm(request.POST or None, request.FILES or None, instance=company,
                               initial={'date': company.date.strftime('%Y-%m-%d')})
    social_accounts = CompanySocialAccount.objects.filter(company=company)
    i = 0
    companies = Company.objects.all()
    retails = CompanyRetail.objects.filter(company=company)

    if request.method == 'POST':

        try:
            if user_form.is_valid() and company_form.is_valid():
                company.user.first_name = user_form.cleaned_data['first_name']
                company.user.last_name = user_form.cleaned_data['last_name']
                company.user.email = user_form.cleaned_data['email']
                company.user.username = user_form.cleaned_data['email']
                company.user.is_active = True
                company.user.save()
                company.logo = company_form.cleaned_data['logo']
                company.save()
                company_form.save()

                company.service.clear()
                for service in company_form.cleaned_data['service']:
                    company.service.add(service)

                if request.POST['retail'] == 'news':
                    name = request.POST['retail-name']
                    logo = request.FILES['retail-logo']
                    retail_company = CompanyRetail(name=name, logo=logo, company=company)
                    retail_company.save()
                elif request.POST['retail'] == '':
                    print('mağaza yok')
                else:
                    retail = Company.objects.get(pk=int(request.POST['retail']))
                    retail_company = CompanyRetail(company=company, name=retail.name, logo=retail.logo)
                    retail_company.save()

                count_value = request.POST['row_number']

                if count_value != '':
                    for social in social_accounts:
                        account = SocialMedia.objects.filter(link=social.social_account.link)
                        account.delete()
                        social.delete()
                    count_value = count_value.split(',')
                    array = []
                    for count in count_value:
                        array.append(count)

                    for i in array:
                        social = SocialMedia(name=request.POST['company_social[' + str(i) + '][name]'],
                                             link=request.POST['company_social[' + str(i) + '][link]'])
                        social.save()
                        company_social = CompanySocialAccount(company=company, social_account=social)
                        company_social.save()

                messages.success(request, 'Firma Başarıyla Güncellenmiştir.')
                return redirect('listArch:firma-listesi')
            else:
                messages.warning(request, 'Alanları Kontrol Edin.')
        except Exception as e:
            print(e)

    return render(request, 'company/update-company.html',
                  {'company_form': company_form, 'user_form': user_form, 'social_accounts': social_accounts,
                   'loop': social_accounts.count(), 'companies': companies, 'retails': retails,
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


def add_companyDefinition(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:
        if request.method == 'POST':
            definition = Definition(key=request.POST['title[tr]'])
            definition.save()

            definitionDesc = DefinitionDescription(definition=definition, lang_code=1,
                                                   title_desc=request.POST['title[tr]'],
                                                   description=request.POST['content[tr]'])
            definitionDesc.save()

            definitionDesc2 = DefinitionDescription(definition=definition, lang_code=2,
                                                    title_desc=request.POST['title[eng]'],
                                                    description=request.POST['content[eng]'])
            definitionDesc2.save()

            company = Company.objects.get(pk=pk)

            company_definition = CompanyDefinition(company=company, definition=definition)
            company_definition.save()

            messages.success(request, "Açıklama Başarıyla Kayıt Edildi.")
            return redirect('listArch:firma-listesi')

    except Exception as e:
        print(e)
    return render(request, 'product/add-product-definition.html',
                  )


@login_required
def company_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            company_id = request.POST['company_id']
            company = Company.objects.filter(pk=company_id)
            company[0].delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def return_company_products(request):
    user = request.user
    company = Company.objects.get(user=user)
    array = []
    category_products = Product.objects.filter(category__is_parent=True).filter(company=company).values(
        'category').annotate(dcount=Count('category'))
    for category_product in category_products:
        product_categories = Product.objects.filter(company=company).filter(
            category=Category.objects.get(pk=category_product['category'])).order_by('?')[:4]
        category_dict = dict()
        category_dict['category'] = Category.objects.get(pk=category_product['category'])
        category_dict['products'] = product_categories
        array.append(category_dict)
    return render(request, 'company/company-products.html', {'products': array})


def company_category_products(request, pk):
    category = Category.objects.filter(pk=pk)
    category_products = Product.objects.filter(category__in=category)
    return render(request, 'company/company-category-products.html',
                  {'category_products': category_products, 'category': category})


def company_product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    product_image = ProductImage.objects.filter(product=Product.objects.get(pk=pk))
    product_file = ProductFile.objects.filter(product=product)
    array = []
    options_value = ProductOptionValue.objects.filter(product=product).values('option_value__option').annotate(
        count=Count('option_value__value'))
    for option in options_value:
        option_dict = dict()
        option_dict['option'] = Option.objects.filter(pk=option['option_value__option'])[0]
        option_dict['values'] = OptionValue.objects.filter(
            option=Option.objects.filter(pk=option['option_value__option'])[0])
        array.append(option_dict)
    descriptions = ProductDefinition.objects.filter(product=product)
    return render(request, 'company/company-product-detail.html',
                  {'product': product, 'product_images': product_image, 'files': product_file,
                   'options': array, 'definitions': descriptions})


def delete_retail(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            retail_id = request.POST['retail_id']
            retail = CompanyRetail.objects.get(pk=retail_id)
            retail.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
