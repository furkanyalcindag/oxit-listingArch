from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

from inoks.models import Profile
from inoks.serializers.ApiSerializer import SponsorApproveSerializer


@login_required
def return_profil_settings(request):
    return render(request, 'ayarlar/profil-ayarlari.html')


@login_required
def return_system_settings(request):
    return render(request, 'ayarlar/sistem-ayarlari.html')


@api_view(http_method_names=['POST'])
def sponsor_isexist(request):
    try:
        isExist = False
        adSoyad = ''
        sponsor = request.POST['sponsor']

        profile = Profile.objects.filter(pk=sponsor)

        if len(profile) > 0:
            isExist = True
            adSoyad = profile[0].user.first_name[0] + '****** ' + profile[0].user.last_name[0] + '******'

        situation = dict()
        situation['situation'] = isExist

        data = SponsorApproveSerializer(situation)

        responseData = dict()
        responseData['isExist'] = data.data

        if profile[0].pk == 1:
            isExist = False

        if isExist:
            return JsonResponse({'status': 'Success', 'msg': 'Sponsor Doğrulandı', 'isExist': True, 'adSoyad': adSoyad})
        else:
            return JsonResponse({'status': 'Success', 'msg': 'Sponsor Bulunamadı', 'isExist': False})

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': 'Sponsor Bulunamadı', 'isExist': False})
