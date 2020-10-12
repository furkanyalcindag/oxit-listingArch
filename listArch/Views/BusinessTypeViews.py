from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from listArch.models import BusinessType
from listArch.services import general_methods


def add_businessType(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    business_types = BusinessType.objects.all()
    try:
        if request.method == 'POST':
            business_type = BusinessType(type=request.POST['business-type'])
            business_type.save()

            messages.success(request, "Profil Adı Başarıyla Kayıt Edildi.")
            return redirect('listArch:profil-adi-ekle')

    except Exception as e:
        print(e)
    return render(request, 'businessType/add-businessType.html', {'business_types': business_types})


def update_businessType(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        try:
            business_type = BusinessType.objects.get(pk=pk)
            business_type.type = request.POST['business-type']

            business_type.save()

            messages.success(request, "Profil Adı Başarıyla Kayıt Edildi.")

        except Exception as e:
            print(e)


def delete_business_type(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            business_type_id = request.POST['id']
            business_type = BusinessType.objects.get(pk=business_type_id)
            business_type.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
