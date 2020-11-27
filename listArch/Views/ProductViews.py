from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from listArch.Forms.FileForm import FileForm
from listArch.models import ProductPerform, GraphicValue, GraphicValueDesc, Value, ChartValue, CompanyCode, File
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
from listArch.serializers.CompanyCodeSerializer import CompanyCodeSerializer
from listArch.serializers.CompanySerializer import CompanySerializer
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
        try:

            product_form = ProductForm(request.POST or None)
            product_image_form = ProductImageForm(request.POST or None, request.FILES)
            product_video_form = VideoForm(request.POST or None, request.FILES)

            if product_form.is_valid() and product_image_form.is_valid() and product_video_form.is_valid():

                company = Company.objects.get(pk=int(request.POST['product-company']))
                product = Product(name=request.POST['product_description[tr][name]'], company=company,
                                  code=product_form.cleaned_data['code'], code2=product_form.cleaned_data['code2'],
                                  isActive=product_form.cleaned_data['isActive'],
                                  company_code=product_form.cleaned_data['company_code'],
                                  isAdvert=product_form.cleaned_data['isAdvert'], code3=request.POST['company-code'])

                product.save()
                product.slug_save()
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
                count_text = request.POST['text-value-row']
                if count_text != '':
                    count_text = count_text.split(',')
                    array_text = []
                    for count in count_text:
                        array_text.append(count)

                    for x in array_text:
                        text_key = request.POST['text-value-row' + str(x) + '']
                        option = Option.objects.get(key=text_key)
                        product_option = ProductOptionValue(product=product, option_value=None, text_value=option)
                        product_option.save()

                messages.success(request, "Ürün Başarıyla eklendi.")
                return redirect('listArch:urun-ekle')
            else:
                messages.success(request, "Alanları kontrol ediniz.")

        except Exception as e:
            print(e)
            return redirect('listArch:admin-error-sayfasi')

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
    try:
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
                product.code3 = request.POST['company-code']
                product.save()

                for tr in product_desc:
                    tr.product = product
                    tr.description = request.POST['product_description[tr][name]']
                    tr.save()

                for eng in product_desc2:
                    eng.description = request.POST['product_description[eng][name]']
                    eng.save()

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
                count_text = request.POST['text-value-row']
                if count_text != '':
                    count_text = count_text.split(',')
                    array_text = []
                    for count in count_text:
                        array_text.append(count)

                    for x in array_text:
                        text_key = request.POST['text-value-row' + str(x) + '']
                        option = Option.objects.get(key=text_key)
                        product_option = ProductOptionValue(product=product, option_value=None, text_value=option)
                        product_option.save()

                messages.success(request, "Ürün Başarıyla Düzenlendi.")

                return redirect('listArch:urunler')
            else:
                messages.warning(request, "Alanları kontrol ediniz.")
        return render(request, 'product/product-edit.html',
                      {'product': product_array, 'options': options, 'product_form': product_form,
                       'companies': companies, 'loop': product_image.count(), 'value_row': product_option_value.count(),
                       'categories': cat_array, 'product_image_form': product_image_form,
                       'product_definitions': product_definitions, 'product_code': product,
                       'loop_value': product_option_value.count(), 'text_value': text_value, })
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')


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

        return render(request, 'product/add-product-definition.html', )
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')


def update_productDefinition(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    definition = Definition.objects.get(pk=pk)
    product_def = ProductDefinition.objects.get(definition=definition)
    definitionDesc = DefinitionDescription.objects.filter(definition=product_def.definition).filter(
        lang_code=1)
    definitionDesc_eng = DefinitionDescription.objects.filter(definition=product_def.definition).filter(
        lang_code=2)
    try:

        if request.method == 'POST':
            product_def.key = request.POST['title[tr]']
            product_def.save()

            for definition_tr in definitionDesc:
                definition_tr.title_desc = request.POST['title[tr]']
                definition_tr.description = request.POST['content[tr]']
                definition_tr.save()

            for definition_eng in definitionDesc_eng:
                definition_eng.title_desc = request.POST['title[eng]']
                definition_eng.description = request.POST['content[eng]']
                definition_eng.save()

            messages.success(request, "Açıklama Başarıyla Düzenlendi.")
            return redirect('listArch:urunler')

        return render(request, 'product/product-definition-update.html',
                      {'def_tr': definitionDesc[0], 'def_eng': definitionDesc_eng[0]})
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')


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


@login_required
def product_definition_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.POST:
        try:

            definition_id = request.POST['definition_id']
            product = Definition.objects.get(pk=definition_id)
            product.delete()

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


@api_view(http_method_names=['POST'])
def get_company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            company_id = request.POST.get('company_id')
            company = Company.objects.get(pk=int(company_id))
            company_codes = CompanyCode.objects.filter(company=company)

            data = CompanyCodeSerializer(company_codes, many=True)

            responseData = dict()
            responseData['firmalar'] = data.data

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
        return render(request, 'product/productGraphValue.html',
                      {'graph_form': graph_form, 'product': product, 'graphic': graphics})
    except Exception as e:

        return JsonResponse({'status': 'Fail', 'msg': e})


def add_chart_graphic(request, uuid):
    product = ""
    try:
        product = Product.objects.get(uuid=uuid)
        product_graphic = ProductChart.objects.filter(product=product)
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

        return render(request, 'product/productChartValue.html',
                      {'product': product, 'graphics': product_graphic})
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')


def add_product_file(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    file_form = FileForm()
    product = Product.objects.get(pk=pk)
    try:
        if request.method == 'POST':

            for file in request.POST['id_file']:
                product.file.add(file)

            messages.success(request, "Dosya Başarıyla Kayıt Edildi.")
            return redirect('listArch:urune-dosya-ekle', pk)

        return render(request, 'product/add-product-file.html', {'form': file_form, 'product': product})
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')


def delete_product_file(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            file_id = request.POST['file_id']
            file = File.objects.get(pk=int(file_id))
            product_file = Product.objects.get(pk=request.POST['product_id'])
            product_file.file.remove(file)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'error', 'messages': 'Dosya Silinemedi'})
