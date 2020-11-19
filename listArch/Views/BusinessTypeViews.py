from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from listArch.Forms.BusinessTypeForm import BusinessTypeForm
from listArch.models import BusinessType, BusinessTypeDesc, Company
from listArch.services import general_methods


def add_businessType(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    business_types = BusinessTypeDesc.objects.filter(lang_code=1)
    form = BusinessTypeForm()
    try:
        if request.method == 'POST':
            form = BusinessTypeForm(request.POST)
            if form.is_valid():
                business_type = BusinessType(key=form.cleaned_data['key'],
                                             isProduct_based=form.cleaned_data['isProduct_based'])
                business_type.save()

                business_tr = BusinessTypeDesc(business_type=business_type, description=form.cleaned_data['key'],
                                               lang_code=1)
                business_tr.save()

                business_eng = BusinessTypeDesc(business_type=business_type, description=request.POST['eng-type'],
                                                lang_code=2)
                business_eng.save()

                messages.success(request, "Profil Adı Başarıyla Kayıt Edildi.")
                return redirect('listArch:profil-adi-ekle')
            else:
                messages.success(request, "Alanları kontrol ediniz.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'businessType/add-businessType.html', {'business_types': business_types, 'form': form})


def update_businessType(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    business_type = BusinessType.objects.get(pk=pk)
    business_types = BusinessTypeDesc.objects.filter(lang_code=1)
    business_tr = BusinessTypeDesc.objects.filter(lang_code=1).filter(business_type=business_type)
    business_eng = BusinessTypeDesc.objects.filter(lang_code=2).filter(business_type=business_type)

    form = BusinessTypeForm(request.POST or None, instance=business_type)

    if request.method == 'POST':
        try:
            business_type.key = form.cleaned_data['key']
            business_type.isProduct_based = form.cleaned_data['isProduct_based']
            business_type.save()
            for business_tr in business_tr:
                business_tr.description = form.cleaned_data['key']
                business_tr.save()
            for business_eng in business_eng:
                business_eng.description = request.POST['eng-type']
                business_eng.save()

            messages.success(request, "Profil Adı Başarıyla Güncellendi.")
            return redirect('listArch:profil-adi-ekle')
        except Exception as e:
            print(e)
            return redirect('listArch:admin-error-sayfasi')
    return render(request, 'businessType/update-bussinessType.html',
                  {'business_types': business_types, 'form': form, 'business_tr': business_tr[0],
                   'business_eng': business_eng[0]})


def delete_business_type(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            business_type_id = request.POST['id']
            business_type = BusinessType.objects.get(pk=business_type_id)
            company_business_type = Company.objects.filter(business_type=business_type)
            if company_business_type.count() == 0:
                business_type.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            else:
                company_name = ''
                for company in company_business_type:
                    company_name = company.name + '-' + company_name
                return JsonResponse({'error': 'Success',
                                     'messages': 'Profil Bilgisi silinemez !! ' + company_name + ' firmalarında tanımlıdır.'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
