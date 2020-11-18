import os

from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.context_processors import media
from rest_framework.decorators import api_view

from listArch.Forms.FileDescForm import FileDescForm
from listArch.Forms.FileForm import FileForm
from listArch.models.FileDesc import FileDesc
from listArch.models.File import File
from listArch.serializers.FileSerializer import FileSerializer
from listArch.services import general_methods
from oxiterp.settings.base import BASE_DIR


def add_file(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    file_form = FileForm()
    fileDesc_form = FileDescForm()
    if request.method == 'POST':
        file_form = FileForm(request.POST, request.FILES)
        fileDesc_form = FileDescForm(request.POST, request.FILES)
        if file_form.is_valid() and fileDesc_form.is_valid():
            file = File(file=file_form.cleaned_data['file'], file_title=file_form.cleaned_data['file_title'],
                        file_type=file_form.cleaned_data['file_type'])
            file.save()
            file_desc = FileDesc(file=file, lang_code=1, file_title=fileDesc_form.cleaned_data['file_title'])
            file_desc.save()

            file_desc2 = FileDesc(file=file, lang_code=2, file_title=file_form.cleaned_data['file_title'])
            file_desc2.save()

            messages.success(request, "Dosya başarıyla eklendi.")
            return redirect('listArch:dosya-ekle')

    return render(request, 'File/add-file.html', {'file_form': file_form, 'file_desc_form': fileDesc_form})


def files(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    files = FileDesc.objects.filter(lang_code=1)
    return render(request, 'File/files.html', {'files': files})


def delete_file(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            file_id = request.POST['file_id']
            file = File.objects.get(pk=file_id)
            file.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def update_file(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    file = File.objects.get(pk=pk)
    name = file.file
    file_desc = FileDesc.objects.filter(lang_code=1).filter(file_id=file.pk)
    file_desc2 = FileDesc.objects.filter(lang_code=2).filter(file_id=file.pk)

    file_form = FileForm(request.POST or None, request.FILES or None, instance=file)
    fileDesc_form = FileDescForm(request.POST or None, request.FILES or None, instance=file_desc[0])
    fileDesc_form2 = FileDescForm(request.POST or None, request.FILES or None, instance=file_desc2[0])

    if request.method == 'POST':
        if file_form.is_valid() and fileDesc_form.is_valid():
            file.file = file_form.cleaned_data['file']
            file.file_title = request.POST['file_title[tr]']
            file.save()

            file_desc[0].file_title = request.POST['file_title[tr]']
            file_desc[0].save()

            file_desc2[0].file_title = request.POST['file_title[eng]']
            file_desc2[0].save()

            os.remove(name.path)

            messages.success(request, "Dosya başarıyla güncellendi.")
            return redirect('listArch:dosyalar')

    return render(request, 'File/file-update.html',
                  {'file_form': file_form, 'file_desc_form': fileDesc_form, 'fileDesc_form2': fileDesc_form2,
                   'file_desc': file_desc[0], 'file_desc2': file_desc2[0]})


@api_view(http_method_names=['POST'])
def get_file(request):
    if request.POST:
        try:

            file_name = request.POST.get('file_name')
            if file_name == '':
                file = []
            else:
                file = FileDesc.objects.filter(file_title__icontains=file_name)

            data = FileSerializer(file, many=True)

            responseData = dict()
            responseData['files'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
