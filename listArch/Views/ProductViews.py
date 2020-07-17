from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from listArch.Forms.ProductCategoryForm import ProductCategoryForm
from listArch.Forms.ProductImageForm import ProductImageForm
from listArch.models.Company import Company
from listArch.models.Product import Product
from listArch.models.Image import Image
from listArch.models.ProductCategory import ProductCategory
from listArch.models.Category import Category
from listArch.models.ProductDesc import ProductDesc
from listArch.models.OptionValue import OptionValue
from listArch.models.ProductOptionValue import ProductOptionValue
from listArch.models.Option import Option
from listArch.models.ProductImage import ProductImage
from listArch.services.general_methods import category_parent_show


def add_product(request):
    options = Option.objects.all()
    category_form = ProductCategoryForm()
    companies = Company.objects.filter(user__is_active=True)
    if request.method == 'POST':
        category_form = ProductCategoryForm(request.POST or None)
        product_image_form = ProductImageForm(request.POST or None, request.FILES)
        try:

            if category_form.is_valid() and product_image_form.is_valid():

                company = Company.objects.get(pk=int(request.POST['product-company']))
                product = Product(name=request.POST['product_description[tr][name]'], company=company,
                                  code=request.POST['product-code'])
                product.save()

                product_desc = ProductDesc(product=product, description=request.POST['product_description[eng][name]'],
                                           lang_code=2)
                product_desc.save()

                for category in category_form.cleaned_data['category']:
                    category = ProductCategory(product=product, category=Category.objects.get(pk=category.pk))
                    category.save()

                image_row = int(request.POST['image_row'])
                i = 0
                while i < image_row:
                    image = Image(image=product_image_form.files['product_image[' + str(i) + '][image]'],
                                  order=int(request.POST['product_image[' + str(i) + '][sort_order]']))
                    image.save()
                    product_image = ProductImage(product=product,
                                                 image=image)
                    product_image.save()
                    i = i + 1

                value_row = int(request.POST['value-row'])
                j = 0
                while j <= value_row:
                    value = OptionValue.objects.filter(pk=int(request.POST['option-key-value[' + str(j) + ']']))
                    product_option_value = ProductOptionValue(product=product, option_value=value[0])
                    product_option_value.save()
                    j = j + 1

                messages.success(request, "Ürün Başarıyla eklendi.")
        except Exception as e:
            print(e)

    return render(request, 'product/add-product.html',
                  {'options': options, 'category_form': category_form,
                   'companies': companies})


def product_list(request):
    products = Product.objects.all()
    product_array = []
    for product in products:
        product_dict = dict()

        product_image = ProductImage.objects.filter(product=product).filter(image__order=1)
        product_option_value = ProductOptionValue.objects.filter(product=product)
        product_dict['image'] = product_image[0].image
        product_dict['product'] = product
        product_dict['category'] = ProductCategory.objects.filter(product=product)
        product_dict['values'] = product_option_value

        product_array.append(product_dict)

    return render(request, 'product/product-list.html', {'products': product_array})


def product_edit(request, pk):
    products = Product.objects.filter(pk=pk)
    product_array = []
    options = Option.objects.all()
    category_form = ProductCategoryForm(request.POST or None)
    companies = Company.objects.filter(user__is_active=True)
    product_image = ProductImage()
    product_option_value = ProductOptionValue()
    cat_array = []
    product_category = ProductCategory.objects.filter(product=products[0])
    category_form = ProductCategoryForm(request.POST or None)
    product_image_form = ProductImageForm(request.POST or None, request.FILES)
    categories = Category.objects.all()

    try:
        for category in categories:
            cat_dict = dict()
            parent_cat = category_parent_show(category)
            cat_dict['category_name'] = parent_cat
            cat_dict['category'] = category
            cat_array.append(cat_dict)

        for product in products:
            product_dict = dict()
            product_option_value = ProductOptionValue.objects.filter(product=product)
            product_image = ProductImage.objects.filter(product=product)
            product_desc = ProductDesc.objects.filter(product=product)
            product_dict['images'] = product_image
            product_dict['categories'] = product_category
            product_dict['values'] = product_option_value
            product_dict['product'] = product
            product_dict['product_desc'] = product_desc[0].description
            product_dict['image'] = ProductImage.objects.filter(product=product).filter(image__order=1)[0].image.image
            product_array.append(product_dict)

        if request.method == 'POST':

            company = Company.objects.get(pk=int(request.POST['product-company']))

            for product in products:
                product.company = company
                product.code = request.POST['product-code']
                product.name = request.POST['product_description[tr][name]']
                product.save()

            product_desc = ProductDesc.objects.filter(product=products[0])
            product_desc[0].product = products[0]
            product_desc[0].description = request.POST['product_description[tr][name]']
            product_desc[0].save()

            for category in category_form.cleaned_data['category']:
                category_product = ProductCategory.objects.filter(product=products[0])
                category_product[0].category = Category.objects.get(pk=category.pk)
                category_product[0].save()

            image_row = int(request.POST['image_row'])
            i = 0
            product_images = ProductImage.objects.filter(product=products[0])
            for product_image in product_images:
                product_image.delete()

            while i < image_row:
                image = Image(image=product_image_form.files['product_image[' + str(i) + '][image]'],
                              order=int(request.POST['product_image[' + str(i) + '][sort_order]']))
                image.save()
                product_image = ProductImage(product=products[0],
                                             image=image)
                product_image.save()
                i = i + 1

            value_row = int(request.POST['value-row'])
            j = 0
            product_option_value = ProductOptionValue.objects.filter(product=products[0])
            for option_value in product_option_value:
                option_value.delete()
            while j <= value_row:
                value = OptionValue.objects.filter(pk=int(request.POST['option-key-value[' + str(j) + ']']))
                product_option_value = ProductOptionValue(product=products[0], option_value=value[0])
                product_option_value.save()
                j = j + 1

            messages.success(request, "Ürün Başarıyla Düzenlendi.")
    except Exception as e:
        print(e)

    return render(request, 'product/product-edit.html',
                  {'product': product_array[0], 'options': options, 'category_form': category_form,
                   'companies': companies, 'loop': product_image.count(), 'value_row': product_option_value.count(),
                   'categories': cat_array, 'p_category': product_category})
