from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from listArch.models.Category import Category
from listArch.models.CategoryDesc import CategoryDesc
from listArch.services.general_methods import category_parent_show


def add_category(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        try:

            category_tr = request.POST['category_description[tr][name]']
            category_eng = request.POST['category_description[eng][name]']

            category = Category(name=category_tr)
            category.save()

            if request.POST['category_parent'] == "":
                category.is_parent = True
                category.save()
            else:
                category.parent = Category.objects.get(pk=request.POST['category_parent'])
                category.save()

            category_desc = CategoryDesc(category=category, description=category_eng, lang_code=2)
            category_desc.save()

            messages.success(request, "Kategori Başarıyla eklendi.")
        except Exception as e:
            print(e)

    return render(request, 'category/add-category.html', {'categories': categories})


def return_categories(request):
    cat_array = []
    try:
        categories = Category.objects.all()

        for category in categories:
            cat_dict = dict()
            parent_cat = category_parent_show(category)
            cat_dict['category_name'] = parent_cat
            cat_dict['category'] = category
            cat_array.append(cat_dict)
    except Exception as e:
        print(e)

    return render(request, 'category/category-list.html', {'categories': cat_array})


def update_category(request, pk):
    category = Category.objects.filter(pk=pk)
    categories = Category.objects.all()
    category_parent = ""
    category_desc = ""
    cat_array = []

    try:
        category_parent = category_parent_show(category[0])
        category_desc = CategoryDesc.objects.filter(category=category[0])

        for cat in categories:
            cat_dict = dict()
            parent_cat = category_parent_show(cat)
            cat_dict['category_name'] = parent_cat
            cat_dict['category'] = cat
            cat_array.append(cat_dict)

        if request.method == 'POST':

            category_tr = request.POST['category_description[tr][name]']
            category_eng = request.POST['category_description[eng][name]']

            category[0].name = category_tr
            category[0].save()

            if request.POST['category_parent'] == "":
                category[0].parent = None
                category[0].is_parent = True
                category[0].save()
            else:
                category[0].parent = Category.objects.get(pk=request.POST['category_parent'])
                category[0].save()

            category_desc[0].description = category_eng
            category_desc[0].save()

            messages.success(request, "Kategori Başarıyla Düzenlendi.")
            return redirect('listArch:kategori-listesi')
    except Exception as e:
        print(e)

    return render(request, 'category/category-update.html',
                  {'category_desc': category_desc[0], 'parent': category_parent,
                   'categories': cat_array, 'category': category[0]})


def delete_category(request):
    if request.POST:
        try:

            category_id = request.POST['category_id']
            category = Category.objects.get(pk=category_id)
            category.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
