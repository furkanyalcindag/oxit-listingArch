from django.contrib import messages
from django.shortcuts import render
from listArch.models import Category
from listArch.models.CategoryDesc import CategoryDesc


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
