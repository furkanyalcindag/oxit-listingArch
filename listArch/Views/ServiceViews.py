from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect, render
from listArch.models import ServiceDesc, Service, Product, Company
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

    return render(request, 'Service/add_service.html', {'services': service})


def delete_service(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            service_id = request.POST['id']
            service = Service.objects.filter(pk=service_id)
            company_service = Company.objects.filter(service__in=service)
            if company_service.count() > 0:
                company_name = ''
                for company in company_service:
                    company_name = company.name + ' - ' + company_name

                return JsonResponse({'status': 'Error',
                                     'messages': 'Silmek istediğiniz hizmet ' + company_name + ' firmalarında kullanılmaktadır.'})
            else:
                service.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def update_service(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    service_all = ServiceDesc.objects.filter(lang_code=1)
    service = Service.objects.get(pk=pk)
    service_tr = ServiceDesc.objects.filter(service=service).filter(lang_code=1)
    service_eng = ServiceDesc.objects.filter(service=service).filter(lang_code=2)
    try:
        if request.method == 'POST':
            service.key = request.POST['tr-service']
            service.save()

            for tr in service_tr:
                tr.description = request.POST['tr-service']
                tr.save()

            for eng in service_eng:
                eng.description = request.POST['eng-service']
                eng.save()

            messages.success(request, "Hizmet Başarıyla Düzenlendi.")
            return redirect('listArch:hizmet-ekle')
    except Exception as e:
        print(e)

    return render(request, 'Service/update_service.html',
                  {'services': service_all, 'service_tr': service_tr, 'service_eng': service_eng})
