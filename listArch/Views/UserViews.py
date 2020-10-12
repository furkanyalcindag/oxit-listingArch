from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.shortcuts import render, redirect
from accounts.forms import ResetPassword
from listArch.Forms.CompanyForm import CompanyForm
from listArch.Forms.CustomerForm import CustomerForm
from listArch.Forms.CustomerUpdateForm import CustomerUpdateForm
from listArch.Forms.UserRegisterForm import UserRegisterForm
from listArch.Forms.UserUpdateForm import UserUpdateForm
from listArch.models import Company, BlogImage, Customer, List, ListProduct, Category
from listArch.models.CompanyBlog import CompanyBlog
from listArch.models.CompanyDefinition import CompanyDefinition
from listArch.models.CompanySocialAccount import CompanySocialAccount
from listArch.models.DefinitionDescription import DefinitionDescription
from listArch.services import general_methods


@login_required
# Profile
def company_information(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    current_user = request.user
    user = User.objects.get(pk=current_user.pk)
    groups = Group.objects.filter(user=user)
    company = Company.objects.get(user=user)
    socials = CompanySocialAccount.objects.filter(company=company)
    definitions = CompanyDefinition.objects.filter(company=company)
    definition_array = []
    if definitions.count() > 0:
        for definition in definitions:
            definition_desc = \
                DefinitionDescription.objects.filter(definition=definition.definition).filter(lang_code=1)[0]

            definition_array.append(definition_desc)

    blogs = CompanyBlog.objects.filter(company=company)
    blog_image = BlogImage.objects.filter(blog__companyblog__company=company)

    return render(request, 'profile.html',
                  {'company': company, 'socials': socials, 'definitions': definition_array, 'blogs': blogs})


def register_customer(request):
    user_form = UserRegisterForm()

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST or None)

        data = request.POST.copy()
        data['username'] = data['email']

        if user_form.is_valid():

            if request.POST['password'] == request.POST['password2']:
                user = user_form.save(commit=False)
                user.username = user.email
                user.save()
                group = Group.objects.get(name='Musteri')
                user2 = user_form.save()
                user2.groups.add(group)
                user.save()
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                customer = Customer(user=user)
                customer.save()
                if request.POST['checkvalue'] == 'true':
                    customer.isCompany = True
                    customer.companyName = request.POST['company-name']
                    customer.companyMail = request.POST['company-email']
                    customer.companyAddress = request.POST['company-address']
                    customer.companyPhone = request.POST['company-phone']
                    customer.save()
                else:
                    customer.isCompany = False
                    customer.save()

                user = auth.authenticate(username=user2.username, password=user2.password)

                if user is not None:
                    # correct username and password login the user
                    auth.login(request, user)

                return redirect('listArch:index')


            else:
                messages.warning(request, 'Girdiğiniz şifreler eşleşmemektedir.')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'User/user-register.html',
                  {'user_form': user_form})



def user_login(request):
    if request.user.is_authenticated is True:
        return redirect('listArch:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            if user.groups.all()[0].name == 'Musteri':
                return redirect('listArch:index')

            else:
                return redirect('accounts:logout')

        else:
            messages.add_message(request, messages.SUCCESS, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return redirect('listArch:kullanici-giris-yap')
    return render(request, 'User/user-login.html')


def user_logout(request):
    logout(request)
    return redirect('listArch:index')


def user_lists(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('listArch:kullanici-giris-yap')
    user = request.user
    customer = Customer.objects.get(user=user)
    lists = List.objects.filter(user=user)
    if customer.isCompany:
        company = Company.objects.get(user=user)
        return render(request, 'User/user-list-product.html',
                      {'customer': customer, 'company': company, 'lists': lists})

    return render(request, 'User/user-list-product.html', {'customer': customer, 'lists': lists})


def user_company_update(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('listArch:kullanici-giris-yap')
    user = request.user
    customer = Customer.objects.get(user=user)

    customer_form = CustomerUpdateForm(request.POST or None, instance=customer)
    user_form = UserUpdateForm(request.POST or None, instance=user)

    form = ResetPassword(request.user, request.POST)

    try:
        if request.method == 'POST':

            if user_form.is_valid() and customer_form.is_valid():
                user.first_name = user_form.cleaned_data['first_name']
                user.last_name = user_form.cleaned_data['last_name']
                user.email = user_form.cleaned_data['email']
                user.username = user_form.cleaned_data['email']
                user.is_active = True
                user.save()

                customer.companyMail = customer_form.cleaned_data['companyMail']
                customer.companyAddress = customer_form.cleaned_data['companyAddress']
                customer.companyPhone = customer_form.cleaned_data['companyPhone']
                customer.companyName = customer_form.cleaned_data['companyName']
                customer.isCompany = True
                customer.save()

                messages.warning(request, 'Bilgileriniz Güncellendi.')
            else:
                messages.warning(request, 'Alanları Kontrol Ediniz.')
    except Exception as e:
        print(e)

    return render(request, 'User/user_company.html',
                  {'user_form': user_form, 'customer_form': customer_form, 'form': form, 'customer': customer})


def user_listing(request):
    user_lists=List.objects.filter(user=request.user)
    products = ListProduct.objects.filter(list__user=request.user).values('product__category__id').annotate(dcount=Count('product'))
    array = []
    for product in products:
        dict_product = dict()
        category = Category.objects.filter(pk=int(product['product__category__id']))
        if category.count() > 0:
            category_products = ListProduct.objects.filter(product__category=category[0])
            dict_product['products'] = category_products
            dict_product['category'] = category[0]


            array.append(dict_product)

    return render(request, 'User/user-list-product.html', {'lists': array,'user_lists':user_lists})


