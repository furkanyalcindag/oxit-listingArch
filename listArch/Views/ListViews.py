from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from listArch.models.List import List
from listArch.services import general_methods


def addList(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:

        if request.method == 'POST':
            list = List(list_name=request.POST['list_name'], user=request.user, type=request.POST['list_type'],
                        description=request.POST['description'])
            list.save()

            messages.success(request, "Liste Başarıyla Kayıt Edildi.")
            return redirect('listArch:kullanici-listeleri')


    except Exception as e:
        print(e)
    return redirect('listArch:kullanici-listeleri')


def delete_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            list_id = request.POST['list_id']
            list = List.objects.get(pk=list_id)
            list.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
