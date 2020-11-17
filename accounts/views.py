from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth, messages

from listArch import urls
from accounts.forms import ResetPassword
from listArch.services import general_methods
from oxiterp.settings.base import EMAIL_HOST_USER


def index(request):
    return render(request, 'accounts/index.html')


def login(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            if user.groups.all()[0].name == 'Admin':
                return redirect('listArch:admin-dashboard')

            elif user.groups.all()[0].name == 'Firma':
                return redirect('listArch:firma-dashboard')

            elif user.groups.all()[0].name == 'Kullanıcı':
                return redirect('listArch:kullanici-dashboard')

            elif user.groups.all()[0].name == 'Personel':
                return redirect('listArch:personel-dashboard')

            else:
                return redirect('accounts:logout')

        else:
            messages.add_message(request, messages.SUCCESS, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        obj = User.objects.filter(username=mail)
        if obj.count() != 0:
            obj = obj[0]
            password = User.objects.make_random_password()
            obj.set_password(password)
            # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            user = obj.save()
            html_content = ''
            subject, from_email, to = 'Oxit Kullanıcı Giriş Bilgileri', EMAIL_HOST_USER, obj.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/"></a>List Of Room</p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı : </strong> ' + obj.username + '</p>'
            html_content = html_content + '<p><strong>Şifre : </strong> ' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("accounts:login")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:forgot")

    return render(request, 'registration/forgot.html')

#müşteri
def user_forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        obj = User.objects.filter(username=mail)
        if obj.count() != 0:
            obj = obj[0]
            password = User.objects.make_random_password()
            obj.set_password(password)
            # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            user = obj.save()
            html_content = ''
            subject, from_email, to = 'Oxit Kullanıcı Giriş Bilgileri', EMAIL_HOST_USER, obj.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong> <a href="http://127.0.0.1:8000/"></a>GVERCİN</p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı : </strong> ' + obj.username + '</p>'
            html_content = html_content + '<p><strong>Şifre : </strong> ' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("listArch:kullanici-giris-yap")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:forgot-user")

    return render(request, 'User/user-forgot.html')


def pagelogout(request):
    logout(request)
    return redirect('accounts:login')


def groups(request):
    group = Group.objects.all()
    return render(request, 'permission/groups.html', {'groups': group})


@login_required
def permission_post(request):
    if request.POST:
        try:
            permissions = request.POST.getlist('values[]')
            group = Group.objects.get(pk=request.POST.get('group'))

            group.permissions.clear()
            group.save()
            if len(permissions) == 0:
                return JsonResponse({'status': 'Success', 'messages': 'Sınıf listesi boş'})
            else:
                for id in permissions:
                    perm = Permission.objects.get(pk=id)
                    group.permissions.add(perm)

            group.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Permission.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def change_password(request):
    group = Group.objects.get(user=request.user)
    if request.method == 'POST':
        form = ResetPassword(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Şifreniz başarıyla değiştirilmiştir.')
            if group.name == 'Kullanıcı':
                return redirect('listArch:kullanici-profil-sayfasi')
            else:
                return redirect('accounts:change_password')

        else:
            for error in form.errors.keys():
                messages.warning(request, form.errors[error])

    else:
        form = ResetPassword(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def permission(request, pk):
    general_methods.show_urls(urls.urlpatterns, 0)
    group = Group.objects.get(pk=pk)
    menu = ""
    ownMenu = ""

    groups = group.permissions.all()
    per = []
    menu2 = []

    for gr in groups:
        per.append(gr.codename)

    ownMenu = group.permissions.all()

    menu = Permission.objects.all()

    for men in menu:
        if men.codename in per:
            print("echo")
        else:
            menu2.append(men)

    return render(request, 'permission/izin-ayar.html',
                  {'menu': menu2, 'ownmenu': ownMenu, 'group': group})


