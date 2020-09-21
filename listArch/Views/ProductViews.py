from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from listArch.Forms.DefinitionDescriptionForm import DefinitionDescriptionForm
from listArch.Forms.DefinitionForm import DefinitionForm
from listArch.Forms.ProductFileForm import ProductFileForm
from listArch.Forms.ProductForm import ProductForm
from listArch.Forms.ProductImageForm import ProductImageForm
from listArch.Forms.RelatedProductForm import RelatedProductForm
from listArch.models import ProductFile, RelatedProduct, OptionDesc, OptionValue
from listArch.models.Company import Company
from listArch.models.Definition import Definition
from listArch.models.DefinitionDescription import DefinitionDescription
from listArch.models.Product import Product
from listArch.models.Image import Image
from listArch.models.Category import Category
from listArch.models.ProductDefinition import ProductDefinition
from listArch.models.ProductDesc import ProductDesc
from listArch.models.ProductOptionValue import ProductOptionValue
from listArch.models.Option import Option
from listArch.models.ProductImage import ProductImage
from listArch.serializers.ProductDefinitionSerializer import ProductDefinitionSerializer
from listArch.serializers.ProductSerializer import ProductSerializer
from listArch.services import general_methods
from listArch.services.general_methods import category_parent_show


def add_product(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    options = Option.objects.all()
    product_form = ProductForm()
    companies = Company.objects.filter(user__is_active=True)
    file_form = ProductFileForm()
    relatedProduct_form = RelatedProductForm()

    if request.method == 'POST':
        file_form = ProductFileForm(request.POST, request.FILES)
        product_form = ProductForm(request.POST or None)
        product_image_form = ProductImageForm(request.POST or None, request.FILES)
        relatedProduct_form = RelatedProductForm(request.POST or None)

        try:

            if product_form.is_valid() and product_image_form.is_valid():

                company = Company.objects.get(pk=int(request.POST['product-company']))
                product = Product(name=request.POST['product_description[tr][name]'], company=company,
                                  code=product_form.cleaned_data['code'],
                                  isActive=product_form.cleaned_data['isActive'],
                                  isSponsor=product_form.cleaned_data['isSponsor'],
                                  company_code=product_form.cleaned_data['company_code'],
                                  isAdvert=product_form.cleaned_data['isAdvert'])
                product.save()
                product.cover_image = request.FILES['cover_image']
                product.save()

                product_desc = ProductDesc(product=product, description=request.POST['product_description[eng][name]'],
                                           lang_code=2)
                product_desc.save()

                product_desc2 = ProductDesc(product=product, description=request.POST['product_description[tr][name]'],
                                            lang_code=1)
                product_desc2.save()

                for category in product_form.cleaned_data['category']:
                    product.category.add(category)

                image_row = int(request.POST['image_row'])
                i = 0
                while i < image_row:
                    image = Image(image=product_image_form.files['product_image[' + str(i) + '][image]'])
                    image.save()
                    product_image = ProductImage(product=product, image=image)
                    product_image.save()
                    i = i + 1

                if request.POST['value-row'] != "":
                    value_row = request.POST['value-row']
                    j = 0
                    product_option_value = ProductOptionValue.objects.filter(product=product)
                    while j <= int(value_row):
                        value = OptionValue.objects.filter(pk=int(request.POST['option-key-value[' + str(j) + ']']))
                        product_option_value = ProductOptionValue(product=product, option_value=value[0])
                        product_option_value.save()
                        j = j + 1

                if request.POST['option_range_count'] != "":
                    option_range = request.POST['option_range_count']
                    if option_range != "":
                        x = 0
                        while x <= int(option_range):
                            option_value = OptionValue.objects.get(option=Option.objects.get(
                                pk=int(request.POST['option_range_id' + str(x) + ''])))
                            product_option = ProductOptionValue(product=product, option_value=option_value,
                                                                range_value=request.POST['range_value'+str(x)+''])
                            product_option.save()
                            x = x + 1

                if relatedProduct_form.cleaned_data['related_product'] != None:
                    for new_product in relatedProduct_form.cleaned_data['related_product']:
                        related_product = RelatedProduct(product=product, related_product=new_product)
                        related_product.save()

                if file_form.cleaned_data['file'] != None:
                    for file in file_form.cleaned_data['file']:
                        product_file = ProductFile(product=product, file=file)
                        product_file.save()

                messages.success(request, "Ürün Başarıyla eklendi.")
                return redirect('listArch:urun-ekle')

        except Exception as e:
            print(e)

    return render(request, 'product/add-product.html',
                  {'options': options, 'product_form': product_form,
                   'companies': companies, 'file_form': file_form, 'related_form': relatedProduct_form})


def product_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    products = Product.objects.all()
    product_array = []
    for product in products:
        product_dict = dict()

        product_image = ProductImage.objects.filter(product=product)
        product_option_value = ProductOptionValue.objects.filter(product=product)
        product_dict['image'] = product.cover_image
        product_dict['product'] = product
        product_dict['values'] = product_option_value
        product_dict['files'] = ProductFile.objects.filter(product=product)

        product_array.append(product_dict)

    return render(request, 'product/product-list.html', {'products': product_array})


def product_edit(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    product = Product.objects.get(pk=pk)
    product_array = []
    options = Option.objects.all()
    companies = Company.objects.filter(user__is_active=True)
    product_image = ProductImage()
    product_option_value = ProductOptionValue()
    cat_array = []
    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    product_image_form = ProductImageForm(request.POST or None, request.FILES)
    categories = Category.objects.all()
    product_definitions = ProductDefinition.objects.filter(product=product)
    product_files = ProductFile.objects.filter(product=product)
    product_file_form = ProductFileForm(request.POST, request.FILES)
    related_products = RelatedProduct.objects.filter(product=product)
    relatedProduct_form = RelatedProductForm(request.POST or None)
    try:
        for category in categories:
            cat_dict = dict()
            parent_cat = category_parent_show(category)
            cat_dict['category_name'] = parent_cat
            cat_dict['category'] = category
            cat_array.append(cat_dict)

        product_dict = dict()
        product_option_value = ProductOptionValue.objects.filter(product=product)
        product_image = ProductImage.objects.filter(product=product)
        product_desc = ProductDesc.objects.filter(product=product).filter(lang_code=1)
        product_desc2 = ProductDesc.objects.filter(product=product).filter(lang_code=2)

        product_dict['images'] = product_image
        product_dict['values'] = product_option_value
        product_dict['product'] = product
        if product_desc.count() > 0:
            product_dict['product_desc'] = product_desc[0].description
        if ProductImage.objects.filter(product=product).count() > 0:
            product_dict['image'] = ProductImage.objects.filter(product=product)[0].image.image
        product_array.append(product_dict)

        if request.method == 'POST':

            company = Company.objects.get(pk=int(request.POST['product-company']))

            product.company = company
            product.isActive = product_form.cleaned_data['isActive']
            product.isSponsor = product_form.cleaned_data['isSponsor']
            product.isAdvert = product_form.cleaned_data['isAdvert']

            product.code = product_form.cleaned_data['code']
            product.cover_image = product_form.cleaned_data['cover_image']
            product.company_code = product_form.cleaned_data['company_code']
            product.name = request.POST['product_description[tr][name]']
            product.save()

            product_desc[0].product = product
            product_desc[0].description = request.POST['product_description[tr][name]']
            product_desc[0].save()

            product_desc2[0].description = request.POST['product_description[eng][name]']
            product_desc2[0].save()

            for f in request.FILES.getlist('input2[]'):
                image = Image(image=f)
                image.save()
                productImages = ProductImage(image=image, product=product)
                productImages.save()

            product.category.clear()
            for category in product_form.cleaned_data['category']:
                product.category.add(category)

            if request.POST['value-row'] != "":
                value_row = request.POST['value-row']
                j = 0
                product_option_value = ProductOptionValue.objects.filter(product=product)

                while j <= int(value_row):
                    value = OptionValue.objects.filter(pk=int(request.POST['option-key-value[' + str(j) + ']']))
                    product_option_value = ProductOptionValue(product=product, option_value=value[0])
                    product_option_value.save()
                    j = j + 1

            if request.POST['option_range_count'] != "":
                option_range = request.POST['option_range_count']
                if option_range != "":
                    x = 0
                    while x <= int(option_range):
                        option_value = OptionValue.objects.get(option=Option.objects.get(
                            pk=int(request.POST['option_range_id' + str(x) + ''])))
                        product_option = ProductOptionValue(product=product, option_value=option_value,range_value=request.POST['range_value'+str(x)+''])
                        product_option.save()
                        x = x + 1

            if relatedProduct_form.cleaned_data != {}:
                for new_product in relatedProduct_form.cleaned_data['related_product']:
                    if related_products:
                        for related_product in related_products:
                            if product != related_product:
                                related_product = RelatedProduct(product=product, related_product=new_product)
                                related_product.save()
                    else:
                        related_product = RelatedProduct(product=product, related_product=new_product)
                        related_product.save()

            if product_file_form.cleaned_data['file'] != None:

                for file in product_file_form.cleaned_data['file']:
                    if product_files:
                        for product_file in product_files:
                            if file != product_file.file:
                                product_file = ProductFile(product=product, file=file)
                                product_file.save()
                    else:
                        product_file = ProductFile(product=product, file=file)
                        product_file.save()

            messages.success(request, "Ürün Başarıyla Düzenlendi.")

            return redirect('listArch:urunler')
    except Exception as e:
        print(e)
    return render(request, 'product/product-edit.html',
                  {'product': product_array[0], 'options': options, 'product_form': product_form,
                   'companies': companies, 'loop': product_image.count(), 'value_row': product_option_value.count(),
                   'categories': cat_array, 'product_image_form': product_image_form,
                   'related_product_form': relatedProduct_form,
                   'product_definitions': product_definitions, 'product_file_form': product_file_form
                   })


@login_required
def product_image_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            image_id = request.POST.get('image_id')
            image = Image.objects.get(pk=image_id)
            product_image = ProductImage.objects.filter(image=image)
            image.delete()
            product_image.delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def product_option_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            option_value_id = request.POST.get('option_id')
            product_option = ProductOptionValue.objects.filter(pk=int(option_value_id))
            product_option[0].delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def add_productDefinition(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    definitionDesc_form = DefinitionDescriptionForm()
    try:
        if request.method == 'POST':
            definitionDesc_form = DefinitionDescriptionForm(request.POST)
            definition_form = DefinitionForm(request.POST)

            definition = Definition(key=request.POST['title[tr]'])
            definition.save()

            definitionDesc = DefinitionDescription(definition=definition, lang_code=1,
                                                   title_desc=request.POST['title[tr]'],
                                                   description=request.POST['content[tr]'])
            definitionDesc.save()

            definitionDesc2 = DefinitionDescription(definition=definition, lang_code=2,
                                                    title_desc=request.POST['title[eng]'],
                                                    description=request.POST['content[eng]'])
            definitionDesc2.save()

            product = Product.objects.get(pk=pk)

            product_definition = ProductDefinition(product=product, definition=definition)
            product_definition.save()

            messages.success(request, "Açıklama Başarıyla Kayıt Edildi.")
            return redirect('listArch:urunler')


    except Exception as e:
        print(e)
    return render(request, 'product/add-product-definition.html',
                  {'definitionDesc_form': definitionDesc_form})


@api_view(http_method_names=['POST'])
def get_product_definition(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            product_id = request.POST.get('product_id')
            product_definitions = ProductDefinition.objects.filter(product_id=product_id)
            array = []
            for product_definition in product_definitions:
                desc = \
                    DefinitionDescription.objects.filter(definition=product_definition.definition).filter(lang_code=1)[
                        0]
                array.append(desc)

            data = ProductDefinitionSerializer(array, many=True)

            responseData = dict()
            responseData['product_definitions'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def product_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            product_id = request.POST['product_id']
            product = Product.objects.filter(pk=product_id)
            product[0].delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_products(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            company_id = request.POST.get('company_id')
            products = Product.objects.filter(isActive=True).filter(company=Company.objects.get(pk=int(company_id)))

            data = ProductSerializer(products, many=True)

            responseData = dict()
            responseData['urunler'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
