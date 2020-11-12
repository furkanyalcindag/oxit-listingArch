from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect, render

from listArch.models import ServiceDesc, Service
from listArch.services import general_methods


def add_service(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    service = ServiceDesc.objects.filter(lang_code=1)

    try:
        if request.method == 'POST':
            service = Service(key=request.POST['tr-service'])
            service.save()

            service_tr = ServiceDesc(service=service, description=request.POST['tr-service'],
                                     lang_code=1)
            service_tr.save()

            service_eng = ServiceDesc(service=service, description=request.POST['eng-service'],
                                      lang_code=2)
            service_eng.save()

            messages.success(request, "Hizmet Başarıyla Kayıt Edildi.")
            return redirect('listArch:hizmet-ekle')
    except Exception as e:

        print(e)

    return render(request, 'add_service.html', {'services': service})


def delete_service(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            service_id = request.POST['id']
            service = Service.objects.get(pk=service_id)
            service.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
