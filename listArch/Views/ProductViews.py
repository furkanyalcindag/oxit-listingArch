from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from listArch.models import ProductPerform, GraphicValue, GraphicValueDesc, Value, ChartValue
from listArch.models.OptionValue import OptionValue
from listArch.models.ProductVideo import ProductVideo
from listArch.models.Video import Video
from listArch.Forms.GraphicValueForm import GraphicValueForm
from listArch.Forms.ProductForm import ProductForm
from listArch.Forms.ProductImageForm import ProductImageForm
from listArch.Forms.VideoForm import VideoForm
from listArch.models.Chart import Chart
from listArch.models.ChartDesc import ChartDesc
from listArch.models.Company import Company
from listArch.models.Definition import Definition
from listArch.models.DefinitionDescription import DefinitionDescription
from listArch.models.Product import Product
from listArch.models.Category import Category
from listArch.models.ProductChart import ProductChart
from listArch.models.ProductDefinition import ProductDefinition
from listArch.models.ProductDesc import ProductDesc
from listArch.models.ProductOptionValue import ProductOptionValue
from listArch.models.Option import Option
from listArch.models.ProductImage import ProductImage
from listArch.serializers.ProductDefinitionSerializer import ProductDefinitionSerializer
from listArch.serializers.ProductSerializer import ProductSerializer
from listArch.services import general_methods
from listArch.services.general_methods import category_parent_show
from listArch.models.Image import Image


def add_product(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    options = Option.objects.all()
    product_form = ProductForm()
    companies = Company.objects.filter(user__is_active=True)

    if request.method == 'POST':

        product_form = ProductForm(request.POST or None)
        product_image_form = ProductImageForm(request.POST or None, request.FILES)
        product_video_form = VideoForm(request.POST or None, request.FILES)

        try:
            if product_form.is_valid() and product_image_form.is_valid() and product_video_form.is_valid():

                company = Company.objects.get(pk=int(request.POST['product-company']))
                product = Product(name=request.POST['product_description[tr][name]'], company=company,
                                  code=product_form.cleaned_data['code'],
                                  isActive=product_form.cleaned_data['isActive'],
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

                for related_product in product_form.cleaned_data['related_product']:
                    product.related_product.add(related_product)

                for category in product_form.cleaned_data['category']:
                    product.category.add(category)

                for file in product_form.cleaned_data['file']:
                    product.file.add(file)

                count = request.POST['image_row']
                count = count.split(',')
                array = []
                for count in count:
                    array.append(count)

                for i in array:
                    image = Image(image=product_image_form.files['product_image[' + str(i) + '][image]'])
                    image.save()
                    product_image = ProductImage(product=product, image=image)
                    product_image.save()

                video_count = request.POST['video_row']
                if video_count != '':
                    video_count = video_count.split(',')
                    array = []
                    for count in video_count:
                        array.append(count)

                    for i in array:
                        video = Video(file=product_video_form.files['product[' + str(i) + '][video]'],
                                      file_key=request.POST['product[' + str(i) + '][key]'])
                        video.save()
                        product_video = ProductVideo(product=product, video=video)
                        product_video.save()

                if request.POST['value-row'] != "":
                    count = request.POST['value-row']
                    count = count.split(',')
                    array = []
                    for count in count:
                        array.append(count)

                    product_option_value = ProductOptionValue.objects.filter(product=product)
                    for value in product_option_value:
                        value.delete()

                    for j in array:
                        value = OptionValue.objects.filter(pk=int(request.POST['option-key-value[' + str(j) + ']']))
                        product_option_value = ProductOptionValue(product=product, option_value=value[0])
                        product_option_value.save()

                if request.POST['option_range_count'] != "":
                    option_range = request.POST['option_range_count']
                    if option_range != "":
                        x = 0
                        while x <= int(option_range):
                            option_value = OptionValue.objects.get(option=Option.objects.get(
                                pk=int(request.POST['option_range_id' + str(x) + ''])))
                            product_option = ProductOptionValue(product=product, option_value=option_value,
                                                                range_value=request.POST['range_value' + str(x) + ''])
                            product_option.save()
                            x = x + 1
                if request.POST['text-value-row'] != "":
                    option_range = request.POST['text-value-row']
                    if option_range != "":
                        x = 0
                        while x < int(option_range):
                            text_key = request.POST['text-value-row' + str(x) + '']
                            option = Option.objects.get(key=text_key)
                            product_option = ProductOptionValue(product=product, option_value=None, text_value=option)
                            product_option.save()
                            x = x + 1

                messages.success(request, "Ürün Başarıyla eklendi.")
                return redirect('listArch:urun-ekle')
            else:
                messages.success(request, "Alanları kontrol ediniz.")

        except Exception as e:
            print(e)
            messages.warning(request, "Hata!!.")

    return render(request, 'product/add-product.html',
                  {'options': options, 'product_form': product_form,
                   'companies': companies, })


def product_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    products = Product.objects.all().order_by('-id')
    product_array = []
    for product in products:
        product_dict = dict()

        product_image = ProductImage.objects.filter(product=product)
        product_option_value = ProductOptionValue.objects.filter(product=product)
        product_dict['image'] = product.cover_image
        product_dict['product'] = product
        product_dict['values'] = product_option_value

        product_array.append(product_dict)

    return render(request, 'product/product-list.html', {'products': product_array})


def product_edit(request, uuid):
    from listArch.models import Image
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    product = Product.objects.get(uuid=uuid)
    product_array = []
    options = Option.objects.all()
    companies = Company.objects.filter(user__is_active=True)
    product_image = ProductImage()
    product_option_value = ProductOptionValue()
    cat_array = []
    product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    product_image_form = ProductImageForm(request.POST or None, request.FILES)
    product_video_form = VideoForm(request.POST or None, request.FILES)
    text_value = ProductOptionValue.objects.filter(product=product)
    categories = Category.objects.all()
    product_definitions = ProductDefinition.objects.filter(product=product)
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
            product_dict['product_desc2'] = product_desc2[0].description
        if ProductImage.objects.filter(product=product).count() > 0:
            product_dict['image'] = ProductImage.objects.filter(product=product)[0].image.image
        product_array.append(product_dict)

        if request.method == 'POST':
            if product_form.is_valid() and product_image_form.is_valid():

                company = Company.objects.get(pk=int(request.POST['product-company']))

                product.company = company
                product.isActive = product_form.cleaned_data['isActive']
                product.isAdvert = product_form.cleaned_data['isAdvert']
                product.save()
                product.code = product_form.cleaned_data['code']
                product.cover_image = product_form.cleaned_data['cover_image']
                product.company_code = product_form.cleaned_data['company_code']
                product.name = request.POST['product_description[tr][name]']
                product.save()

                for tr in product_desc:
                    tr.product = product
                    tr.description = request.POST['product_description[tr][name]']
                    tr.save()

                for eng in product_desc2:
                    eng.description = request.POST['product_description[eng][name]']
                    eng.save()

                for f in request.FILES.getlist('input2[]'):
                    image = Image(image=f)
                    image.save()
                    productImages = ProductImage(image=image, product=product)
                    productImages.save()

                product.related_product.clear()
                for related_product in product_form.cleaned_data['related_product']:
                    product.related_product.add(related_product)
                product.category.clear()
                for category in product_form.cleaned_data['category']:
                    product.category.add(category)
                product.file.clear()
                for file in product_form.cleaned_data['file']:
                    product.file.add(file)

                count = request.POST['image_row']
                if count != '':
                    count = count.split(',')
                    array = []
                    for count in count:
                        array.append(count)

                    for i in array:
                        image = Image(image=product_image_form.files['product_image[' + str(i) + '][image]'])
                        image.save()
                        product_image = ProductImage(product=product, image=image)
                        product_image.save()

                count_value = request.POST['value-row']
                if count_value != '':
                    count_value = count_value.split(',')
                    array = []
                    for count in count_value:
                        array.append(count)

                    for j in array:
                        value = OptionValue.objects.filter(pk=int(request.POST['option-key-value[' + str(j) + ']']))
                        product_option_value = ProductOptionValue(product=product, option_value=value[0])
                        product_option_value.save()

                if request.POST['option_range_count'] != "":
                    option_range = request.POST['option_range_count']
                    if option_range != "":
                        x = 0
                        while x <= int(option_range):
                            option_value = OptionValue.objects.get(option=Option.objects.get(
                                pk=int(request.POST['option_range_id' + str(x) + ''])))
                            product_option = ProductOptionValue(product=product, option_value=option_value,
                                                                range_value=request.POST['range_value' + str(x) + ''])
                            product_option.save()
                            x = x + 1
                if request.POST['text-value-row'] != "":
                    option_range = request.POST['text-value-row']
                    if option_range != "":
                        x = 0
                        while x < int(option_range):
                            text_key = request.POST['text-value-row' + str(x) + '']
                            option = Option.objects.get(key=text_key)
                            product_option = ProductOptionValue(product=product, option_value=None, text_value=option)
                            product_option.save()
                            x = x + 1

                messages.success(request, "Ürün Başarıyla Düzenlendi.")

                return redirect('listArch:urunler')
            else:
                messages.warning(request, "Alanları kontrol ediniz.")

    except Exception as e:
        print(e)

    return render(request, 'product/product-edit.html',
                  {'product': product_array[0], 'options': options, 'product_form': product_form,
                   'companies': companies, 'loop': product_image.count(), 'value_row': product_option_value.count(),
                   'categories': cat_array, 'product_image_form': product_image_form,
                   'product_definitions': product_definitions,
                   'loop_value': product_option_value.count(),'text_value':text_value,
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
    try:
        if request.method == 'POST':
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
                  {})


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


def add_graphic(request, pk):
    try:
        graph_form = GraphicValueForm()
        product = Product.objects.get(pk=pk)
        graphics = ProductPerform.objects.filter(product=product)
        if request.POST:
            graph_form = GraphicValueForm(request.POST or None)

            if graph_form.is_valid():
                graphValue = GraphicValue(min=graph_form.cleaned_data['min'], max=graph_form.cleaned_data['max'],
                                          current_value=graph_form.cleaned_data['current_value'],
                                          middle=graph_form.cleaned_data['middle'],
                                          unit=graph_form.cleaned_data['unit'])
                graphValue.save()

                graph_desc = GraphicValueDesc(lang_code=1, graphValue=graphValue,
                                              description=request.POST['graphic[tr][name]'])
                graph_desc.save()

                graph_desc = GraphicValueDesc(lang_code=2, graphValue=graphValue,
                                              description=request.POST['graphic[eng][name]'])
                graph_desc.save()

                productGraph = ProductPerform(product=product, graphValue=graphValue)
                productGraph.save()
                messages.success(request, "Grafik Bilgileri Başarıyla Kayıt Edildi.")
                return redirect('listArch:urunler')
            else:
                messages.success(request, "Alanları Kontrol Ediniz.")

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': e})
    return render(request, 'product/productGraphValue.html',
                  {'graph_form': graph_form, 'product': product, 'graphic': graphics})


def add_chart_graphic(request, uuid):
    product = ""
    try:
        product = Product.objects.get(uuid=uuid)
        if request.POST:
            count = request.POST['count']
            count = count.split(',')
            array = []
            for count in count:
                array.append(count)

            i = 0
            chart = Chart(key=request.POST['graphic[tr][name]'])
            chart.save()

            chart_tr = ChartDesc(lang_code=1, description=request.POST['graphic[tr][name]'], chart=chart)
            chart_tr.save()

            chart_eng = ChartDesc(lang_code=2, description=request.POST['graphic[eng][name]'], chart=chart)
            chart_eng.save()

            for i in array:
                value = Value(year=request.POST['graphic_year[' + str(i) + ']'],
                              value=request.POST['graphic_value[' + str(i) + ']'])
                value.save()
                chart_value = ChartValue(chart=chart, value=value)
                chart_value.save()

            product_chart = ProductChart(product=product, chart=chart)
            product_chart.save()

            messages.success(request, "Grafik Bilgileri Başarıyla Kayıt Edildi.")
            return redirect('listArch:urunler')

    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': e})
    return render(request, 'product/productChartValue.html',
                  {'product': product, })
