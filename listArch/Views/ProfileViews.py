from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import redirect, render
from listArch.Forms.ProfileForm import ProfileForm
from listArch.Forms.UserCompanyForm import UserCompanyForm
from listArch.Forms.UserForm import UserForm
from listArch.models import Profile, BusinessTypeDesc, Country
from listArch.services import general_methods
from oxiterp.settings.base import EMAIL_HOST_USER


def add_profile(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    profile_form = ProfileForm()
    user_form = UserForm()
    profile_names = BusinessTypeDesc.objects.filter(lang_code=1)
    countries = Country.objects.all()

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST or None)

        try:
            data = request.POST.copy()
            data['username'] = data['email']
            user_form = UserCompanyForm(data)

            if profile_form.is_valid() and user_form.is_valid():
                user = user_form.save(commit=False)
                group = Group.objects.get(name='Profil')
                user2 = user_form.save()
                password = User.objects.make_random_password()
                user.set_password(password)
                user2.groups.add(group)
                user.is_active = True
                user.username = user.email
                user.save()

                profile = Profile(user=user, website=profile_form.cleaned_data['website'],
                                  country=profile_form.cleaned_data['country'],
                                  address=profile_form.cleaned_data['address'],
                                  city=profile_form.cleaned_data['city'],
                                  profile_name=profile_form.cleaned_data['profile_name'],
                                  map=profile_form.cleaned_data['map'],
                                  image=profile_form.cleaned_data['image'])

                profile.save()

                subject, from_email, to = 'List Of Room Giriş Bilgileri', EMAIL_HOST_USER, user2.email
                text_content = 'Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.'
                html_content = '<p> <strong>Site adresi:</strong><a href="http://127.0.0.1:8000/">ListOfRoom</a></p>'
                html_content = html_content + '<p><strong>Kullanıcı Adı: </strong>' + user2.username + '</p>'
                html_content = html_content + '<p><strong>Şifre: </strong>' + password + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, "Profil Başarıyla Kayıt Edildi.")
                return redirect('listArch:profil-kaydet')
            else:
                messages.success(request, "Alanları Kontrol Ediniz.")
        except Exception as e:
            print(e)
    return render(request, 'Profile/add_profile.html',
                  {'profile_form': profile_form, 'user_form': user_form, 'profile_names': profile_names,
                   'countries': countries})


def profile_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'Profile/profiles.html')


def profile_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            profile_id = request.POST['profile_id']
            profile = Profile.objects.get(pk=profile_id)
            profile.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
