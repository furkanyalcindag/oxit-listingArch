from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from listArch.Forms.ProfileForm import ProfileForm
from listArch.Forms.UserCompanyForm import UserCompanyForm
from listArch.Forms.UserForm import UserForm
from listArch.models import Profile, BusinessTypeDesc, Country
from listArch.services import general_methods


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


                messages.success(request, "Profil Başarıyla Kayıt Edildi.")
                return redirect('listArch:profil-kaydet')

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
