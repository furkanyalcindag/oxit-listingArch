from django.contrib import messages
from django.shortcuts import render

from listArch.Forms.ProductCategoryForm import ProductCategoryForm
from listArch.Forms.ProductImageForm import ProductImageForm
from listArch.models.Option import Option


def add_product(request):
    options = Option.objects.all()
    category_form = ProductCategoryForm()
    product_image_form = ProductImageForm()
    if request.method == 'POST':
        try:

            messages.success(request, "Kategori Başarıyla eklendi.")
        except Exception as e:
            print(e)

    return render(request, 'product/add-product.html',
                  {'options': options, 'category_form': category_form, 'image_form': product_image_form})
