from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import redirect, render
from listArch.Forms.UserForm import UserForm
from listArch.models import Staff
from listArch.services import general_methods
from oxiterp.settings.base import EMAIL_HOST_USER


def register_staff(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user_form = UserForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST or None)

        data = request.POST.copy()
        data['username'] = data['email']
        user_form = UserForm(data)

        if user_form.is_valid():

            user = user_form.save(commit=False)

            group = Group.objects.get(name='Personel')
            user2 = user_form.save()
            password = User.objects.make_random_password()
            user.set_password(password)
            user2.groups.add(group)
            user.is_active = True
            user.username = user.email
            user.save()

            staff = Staff(user=user)
            staff.save()

            staff.phone = request.POST['phone']
            staff.save()

            subject, from_email, to = 'List Of Room Giriş Bilgileri', EMAIL_HOST_USER, user2.email
            text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
            html_content = '<p> <strong>Site adresi:</strong><a href="http://127.0.0.1:8000/">ListOfRoom</a></p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
            html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, 'Personel Bilgileri Başarıyla Kayıt Edildi.')

            return redirect('listArch:personeller')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'User/add_staff.html',
                  {'user_form': user_form})


def staff(request):
    staff = Staff.objects.all()
    return render(request, 'User/staff_list.html', {'staff': staff})


def passive_staff(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            staff_id = request.POST['staff_id']
            staff = Staff.objects.get(pk=staff_id)
            staff.isActive = False
            staff.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})

def active_staff(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            staff_id = request.POST['staff_id']
            staff = Staff.objects.get(pk=staff_id)
            staff.isActive = True
            staff.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
