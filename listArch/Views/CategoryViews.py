from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from listArch.Forms.CategoryForm import CategoryForm
from listArch.models.Category import Category
from listArch.models.CategoryDesc import CategoryDesc
from listArch.services import general_methods
from listArch.services.general_methods import category_parent_show


def add_category(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categories = Category.objects.all()
    category_form = CategoryForm()
    try:
        if request.method == 'POST':
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():

                category_tr = request.POST['category_description[tr][name]']
                category_eng = request.POST['category_description[eng][name]']

                category = Category(name=category_tr, isActive=category_form.cleaned_data['isActive'],
                                    isBasic=category_form.cleaned_data['isBasic'],
                                    order=category_form.cleaned_data['order'], icon=request.FILES['icon'])
                category.save()

                if request.POST['category_parent'] == "":
                    category.is_parent = True
                    category.save()
                else:
                    category.parent = Category.objects.get(pk=request.POST['category_parent'])
                    category.save()

                content_tr = request.POST['content[tr]']
                content_eng = request.POST['content[eng]']

                category_desc = CategoryDesc(category=category, description=category_eng, lang_code=2,
                                             definition=content_eng, page_description=request.POST['description[eng]'])
                category_desc.save()

                category_desc2 = CategoryDesc(category=category, description=category_tr, lang_code=1,
                                              definition=content_tr, page_description=request.POST['description[tr]'])
                category_desc2.save()

                messages.success(request, "Kategori Başarıyla eklendi.")
                return redirect('listArch:kategori-ekle')
            else:
                messages.warning(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'category/add-category.html', {'categories': categories, 'category_form': category_form})


def return_categories(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    cat_array = []
    try:
        categories = CategoryDesc.objects.filter(lang_code=1).order_by('-description').filter(category__isActive=True)

        for category in categories:
            cat_dict = dict()
            parent_cat = category_parent_show(category.category)
            cat_dict['category_name'] = parent_cat
            cat_dict['category'] = category.category
            cat_array.append(cat_dict)
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'category/category-list.html', {'categories': cat_array})


def update_category(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    category = Category.objects.get(pk=pk)
    categories = Category.objects.all()
    category_parent = ""
    category_desc1 = ""
    category_desc2 = ""

    cat_array = []
    category_form = CategoryForm(request.POST or None, request.FILES or None, instance=category)

    try:
        if category.parent:
            category_parent = category.parent.name
        else:
            category_parent = ""
        category_desc1 = CategoryDesc.objects.filter(category=category).filter(lang_code=1)
        category_desc2 = CategoryDesc.objects.filter(category=category).filter(lang_code=2)

        for cat in categories:
            cat_dict = dict()
            parent_cat = category_parent_show(cat)
            parent = parent_cat.split(' > ')
            if parent.__len__() == 2:
                cat_dict['category_name'] = parent[0]
            elif parent.__len__() == 3:
                cat_dict['category_name'] = parent[1]
            elif parent.__len__() == 4:
                cat_dict['category_name'] = parent[2]

            cat_dict['category'] = cat
            cat_array.append(cat_dict)

        if request.method == 'POST':
            if category_form.is_valid():

                category_eng = request.POST['category_description[eng][name]']
                category_tr = request.POST['category_description[tr][name]']

                category.isActive = category_form.cleaned_data['isActive']
                category.isBasic = category_form.cleaned_data['isBasic']
                category.order = category_form.cleaned_data['order']
                category.icon = category_form.cleaned_data['icon']
                category.name = category_tr

                category.save()

                # TR
                for category_desc_tr in category_desc1:
                    category_desc_tr.description = category_tr
                    category_desc_tr.definition = request.POST['content[tr]']
                    category_desc_tr.page_description = request.POST['description[tr]']
                    category_desc_tr.save()

                # ENG
                for category_desc_eng in category_desc2:
                    category_desc_eng.description = category_eng
                    category_desc_eng.definition = request.POST['content[eng]']
                    category_desc_eng.page_description = request.POST['description[eng]']
                    category_desc_eng.save()

                if category.isBasic:
                    category.parent = None
                    category.is_parent = True
                    category.icon = category_form.cleaned_data['icon']
                    category.save()
                else:
                    category.parent = Category.objects.get(pk=request.POST['category_parent'])
                    category.save()

                messages.success(request, "Kategori Başarıyla Düzenlendi.")
                return redirect('listArch:kategori-listesi')
            else:
                messages.success(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')

    return render(request, 'category/category-update.html',
                  {'parent': category_parent, 'category_tr': category_desc1[0],
                   'category_eng': category_desc2[0],
                   'categories': cat_array, 'category': category, 'category_form': category_form})


def delete_category(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            category_id = request.POST['category_id']
            category = Category.objects.get(pk=category_id)
            if not category.is_parent:
                category.isActive = False
                category.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Error', 'messages': 'Alt Kategori Silinemez !! '})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
