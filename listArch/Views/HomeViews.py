import json
from django.db.models import Count, Q, QuerySet
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from listArch.models import ProductOptionValue, Option, OptionValue, Company, IntroductionPage, \
    IntroductionPageDesc, CategoryDesc, BlogDesc, CompanyBlog, RelatedProduct, \
    OptionValueDesc, List, CompanyRetail, Contact, AboutDesc, ProductDesc, OptionDesc, ProductPerform, GraphicValueDesc, \
    ProductChart, ChartValue, Value, ChartDesc, Profile, BusinessType, ProfileBlog, BlogImage, ProfileBlogDesc, \
    BusinessTypeDesc, ProductVideo, ServiceDesc, Collection, CollectionProduct, IntroductionTitle
from listArch.models.CompanyDefinition import CompanyDefinition
from listArch.models.IntroductionTitleDesc import IntroductionTitleDesc
from listArch.models.CompanySocialAccount import CompanySocialAccount
from listArch.models.DefinitionDescription import DefinitionDescription
from listArch.models.Product import Product
from listArch.models.Category import Category
from listArch.models.ProductDefinition import ProductDefinition
from listArch.models.ProductImage import ProductImage
from listArch.serializers.CompanySerializer import CompanySerializer
from listArch.serializers.IntroductionPageDescSerializer import IntroductionPageDescSerializer
from listArch.serializers.ProductDescSerializer import ProductDescSerializer
from listArch.serializers.ProductSerializer import ProductSerializer
from listArch.serializers.ProductValueSerializer import ProductValueSerializer
from oxiterp.settings.base import home_lang_code


def base2(request):
    category_parent = CategoryDesc.objects.filter(category__is_parent=True).filter(category__isActive=True).filter(
        lang_code=home_lang_code).order_by(
        'category__order')[:6]
    categories = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(category__isActive=True)
    companies = Company.objects.all()

    return render(request, 'home/index.html',
                  {'categories': categories, 'brands': companies, 'category_parent': category_parent})


def get_company_products(request, pk):
    array = []
    options_value = OptionValue.objects.values('option', 'option__type').annotate(count=Count('value'))
    for option in options_value:
        option_dict = dict()
        option_dict['option'] = Option.objects.filter(pk=option['option'])[0]
        option_dict['values'] = OptionValue.objects.filter(option__id=option['option'])
        array.append(option_dict)

    company = Company.objects.get(pk=pk)
    company_products = Product.objects.filter(company=company).filter(isActive=True).order_by('?')[:3]
    categories = Category.objects.all()
    return render(request, 'home/company-products.html',
                  {'products': company_products, 'options': array, 'categories': categories, 'company': company})


def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        category = product.category.filter(is_parent=True)
        graphics = ProductPerform.objects.filter(product=product)
        product_videos = ProductVideo.objects.filter(product=product)

        service_array = []
        for service in product.company.service.all():
            service_array.append(ServiceDesc.objects.filter(lang_code=home_lang_code).filter(
                service=service)[0])

        product_chart = ProductChart.objects.filter(product=product)
        chart_array = []

        for chart in product_chart:
            chart_dict = dict()
            values = ChartValue.objects.filter(chart=chart.chart)
            value_array = []
            for value in values:
                value_dict = dict()
                value = Value.objects.filter(pk=value.value.pk)[0]
                value_dict['year'] = value.year
                value_dict['value'] = value.value
                value_array.append(value_dict)
            chart_dict['values'] = value_array
            chart_dict['product_chart'] = ChartDesc.objects.filter(lang_code=home_lang_code).filter(chart=chart.chart)[
                0].chart.pk
            chart_dict['description'] = ChartDesc.objects.filter(lang_code=home_lang_code).filter(chart=chart.chart)[
                0].description
            chart_array.append(chart_dict)

        graph_array = []
        for graph_value in graphics:
            value_dict = dict()
            value_dict['min'] = graph_value.graphValue.min
            value_dict['max'] = graph_value.graphValue.max
            value_dict['middle'] = graph_value.graphValue.middle
            value_dict['current_value'] = graph_value.graphValue.current_value
            value_dict['unit'] = graph_value.graphValue.unit
            value_dict['name'] = \
                GraphicValueDesc.objects.filter(lang_code=home_lang_code).filter(graphValue=graph_value.graphValue)[
                    0].description
            graph_array.append(value_dict)

        cat_desc = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(category=category[0])
        if cat_desc.count() > 0:
            cat_desc = cat_desc[0]
        desc_array = []
        description = ProductDefinition.objects.filter(product=product)
        for desc in description:
            desc_dict = dict()
            desc_dict['desc'] = \
                DefinitionDescription.objects.filter(definition=desc.definition).filter(lang_code=home_lang_code)[0]
            desc_array.append(desc_dict)

        company_definitions = CompanyDefinition.objects.filter().filter(company=product.company)
        company_definition_array = []
        for company_def in company_definitions:
            desc_dict = dict()
            desc_dict['desc'] = \
                DefinitionDescription.objects.filter(definition=company_def.definition).filter(
                    lang_code=home_lang_code)[
                    0]
            company_definition_array.append(desc_dict)

        product_image = ProductImage.objects.filter(product=product)

        options = ProductOptionValue.objects.filter(product=product)
        array = []
        options_value = ProductOptionValue.objects.filter(product=product).values('option_value').annotate(
            count=Count('option_value'))
        for option in options_value:
            option_dict = dict()
            if option['option_value']:

                if not OptionValue.objects.filter(pk=option['option_value'])[0].option.type == 'range':
                    product_option = \
                        OptionValueDesc.objects.filter(lang_code=home_lang_code).filter(
                            option_value_id=option['option_value'])[
                            0].option_value.option
                    option_dict['option'] = \
                        OptionDesc.objects.filter(option_id=product_option.pk).filter(lang_code=home_lang_code)[
                            0]
                    option_dict['values'] = OptionValueDesc.objects.filter(
                        option_value_id=option['option_value']).filter(
                        lang_code=home_lang_code)

                    array.append(option_dict)
                else:
                    option_dict['range_value'] = \
                        ProductOptionValue.objects.filter(product=product).filter(
                            option_value_id=option['option_value'])[0]
                    array.append(option_dict)
        socials = CompanySocialAccount.objects.filter(company=product.company)
        # distinct('product')

        return render(request, 'home/product-detail.html',
                      {'product': product, 'images': product_image, 'options': array, 'definitions': desc_array,
                       'company_definitions': company_definition_array, 'social': socials,
                       'category': cat_desc, 'services': service_array,
                       'graphics': graph_array, 'charts': chart_array,
                       'videos': product_videos,
                       })
    except Exception as e:
        print(e)
        return redirect('listArch:404-sayfasi')


def product_filter_page(request, pk):
    try:
        list = ""
        if not request.user.is_anonymous:
            user = request.user
            list = List.objects.filter(user=user)

        category = Category.objects.get(pk=pk)
        cat_desc = CategoryDesc.objects.filter(category=category).filter(lang_code=home_lang_code).order_by(
            'category__order')
        parent_cat = CategoryDesc.objects.filter(category=cat_desc[0].category.parent).filter(
            lang_code=home_lang_code).order_by('category__order')
        category_desc = ""
        if cat_desc.count() > 0:
            category_desc = cat_desc[0]
        array = []
        basic_options_value = OptionValue.objects.filter(option__isBasic=True).values('option',
                                                                                      'option__type').annotate(
            count=Count('value'))
        for option in basic_options_value:
            option_dict = dict()
            option_dict['option'] = \
                OptionDesc.objects.filter(lang_code=home_lang_code).filter(option_id=option['option'])[
                    0]
            option_dict['values'] = OptionValueDesc.objects.filter(option_value__option__id=option['option']).filter(
                lang_code=home_lang_code).order_by('?')[:5]
            if len(option_dict['values']) == 0:
                option_dict['range'] = OptionValue.objects.filter(option=option['option'])[0]
            option_dict['allValues'] = OptionValueDesc.objects.filter(option_value__option__id=option['option']).filter(
                lang_code=home_lang_code)
            option_dict['count'] = OptionValueDesc.objects.filter(option_value__option__id=option['option']).filter(
                lang_code=home_lang_code).count()
            array.append(option_dict)
        advanced_options_value = OptionValue.objects.filter(option__category=category).filter(
            option__isBasic=False).values(
            'option', 'option__type').annotate(
            count=Count('value'))
        array_advanced = []
        for option in advanced_options_value:
            option_dict = dict()
            option_dict['option'] = \
                OptionDesc.objects.filter(lang_code=home_lang_code).filter(option_id=option['option'])[
                    0]
            option_dict['values'] = OptionValueDesc.objects.filter(option_value__option__id=option['option']).filter(
                lang_code=home_lang_code).order_by('?')[:5]
            if len(option_dict['values']) == 0:
                option_dict['range'] = OptionValue.objects.filter(option=option['option'])[0]
            option_dict['allValues'] = OptionValueDesc.objects.filter(option_value__option__id=option['option']).filter(
                lang_code=home_lang_code)
            option_dict['count'] = OptionValueDesc.objects.filter(option_value__option__id=option['option']).filter(
                lang_code=home_lang_code).count()
            array_advanced.append(option_dict)

        products = ProductDesc.objects.filter(product__category=category).distinct('product_id')[:50]
        advert_product = ProductDesc.objects.filter(product__isAdvert=True).filter(lang_code=home_lang_code).filter(
            product__category=category).order_by(
            'id')[:5]

        option_text = OptionDesc.objects.filter(option__type='text')
    except Exception as e:
        print(e)
        return redirect('listArch:404-sayfasi')
    return render(request, 'home/product-filter.html',
                  {'products': products, 'options': array, 'advanced_options': array_advanced,
                   'option_text': option_text, 'category': category_desc, "parent_cat": parent_cat[0],
                   'cat_desc': category_desc, 'advert_product': advert_product,
                   'lists': list})


def search_product_filter(request):
    list = ""
    try:
        if request.POST:

            parent_category = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(
                category_id=request.POST['sub_category'])
            value = request.POST['search_value']
            company = Company.objects.get(pk=request.POST['search_company'])

            search_products = ProductDesc.objects.filter(lang_code=home_lang_code).filter(
                product__isActive=True).filter(
                product__name__icontains=value).filter(product__category=parent_category[0].category).filter(
                product__company=company)

            array = []
            options_value = OptionValueDesc.objects.values('option_value__option',
                                                           'option_value__option__type').annotate(
                count=Count('option_value__value'))

            for option in options_value:
                option_dict = dict()
                option_dict['option'] = Option.objects.filter(pk=option['option_value__option'])[0]
                option_dict['values'] = OptionValue.objects.filter(option__id=option['option_value__option'])
                array.append(option_dict)
            list = ""
            if not request.user.is_anonymous:
                user = request.user
                list = List.objects.filter(user=user)

            option_text = OptionDesc.objects.filter(option__type='text')
            advert_product = ProductDesc.objects.filter(
                product__category=parent_category[0].category).filter(lang_code=home_lang_code).filter(
                product__isAdvert=True).order_by('id')[:5]

            advanced_options_value = OptionValueDesc.objects.filter(lang_code=home_lang_code).filter(
                option_value__option__category=parent_category[0].category).filter(
                option_value__option__isBasic=False).values(
                'option_value__option', 'option_value__option__type').annotate(
                count=Count('option_value__value'))
            array_advanced = []
            for option in advanced_options_value:
                option_dict = dict()
                option_dict['option'] = \
                    OptionDesc.objects.filter(lang_code=home_lang_code).filter(
                        option_id=option['option_value__option'])[
                        0]
                option_dict['values'] = OptionValueDesc.objects.filter(
                    option_value__option__id=option['option_value__option']).filter(
                    lang_code=home_lang_code).order_by('?')[:5]
                if len(option_dict['values']) == 0:
                    option_dict['range'] = OptionValue.objects.filter(option=option['option_value__option'])[0]
                option_dict['allValues'] = OptionValueDesc.objects.filter(
                    option_value__option__id=option['option_value__option']).filter(
                    lang_code=home_lang_code)
                option_dict['count'] = OptionValueDesc.objects.filter(
                    option_value__option__id=option['option_value__option']).filter(
                    lang_code=home_lang_code).count()
                array_advanced.append(option_dict)
            return render(request, 'home/product-filter.html',
                          {'products': search_products, 'options': array, 'advanced_options': array_advanced,
                           'option_text': option_text, 'category': parent_category[0],
                           'advert_product': advert_product, "parent_cat": parent_category[0],
                           'lists': list})
    except Exception as e:
        print(e)
        return render(request, 'home/notFound-page.html')

    return render(request, 'home/product-filter.html')


def search_product_home(request):
    list = ""
    try:
        if request.POST:
            companies = Company.objects.all()
            parent_category = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(
                category_id=request.POST['parent_category'])
            value = request.POST['search_value']

            search_products = ProductDesc.objects.filter(product__isActive=True).filter(
                product__name__icontains=value).filter(
                product__category=parent_category[0].category).filter(lang_code=home_lang_code)
            list = ""
            if not request.user.is_anonymous:
                user = request.user
                list = List.objects.filter(user=user)

            advert_product = ProductDesc.objects.filter(
                product__category=parent_category[0].category).filter(lang_code=home_lang_code).filter(
                product__isAdvert=True).order_by('id')[:5]
            sub_categories = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(
                category__isActive=True).filter(
                category__parent=parent_category[0].category
            )

            return render(request, 'home/products.html',
                          {'products': search_products, 'companies': companies,
                           'category': parent_category[0], 'sub_category': sub_categories,
                           'advert_product': advert_product, "parent_cat": parent_category[0],
                           'lists': list})
    except Exception as e:
        print(e)
        return redirect('listArch:404-sayfasi')

    return render(request, 'home/products.html')


def get_company_info(request, pk):
    try:
        company = Company.objects.get(pk=pk)
        products = Product.objects.filter(company=company)
        retails = CompanyRetail.objects.filter(company=company)

        company_collection = Collection.objects.filter(company=company)
        collection_array = []
        for collection in company_collection:
            products = CollectionProduct.objects.filter(collection=collection)
            product_dict = dict()
            product_dict['name'] = collection.name
            product_dict['image'] = products[0].product.cover_image
            collection_array.append(product_dict)

        array = []
        company_definitions = CompanyDefinition.objects.filter(company=company)
        company_definition_array = []
        for company_def in company_definitions:
            desc_dict = dict()
            desc_dict['desc'] = \
                DefinitionDescription.objects.filter(definition=company_def.definition).filter(
                    lang_code=home_lang_code)[0]
            company_definition_array.append(desc_dict)
        category_products = Product.objects.filter(company=company).values('category').annotate(
            dcount=Count('category'))
        for category_product in category_products:
            product_categories = Product.objects.filter(company=company).filter(
                category=Category.objects.get(pk=category_product['category'])).distinct('id')
            category_dict = dict()
            category_dict['category'] = Category.objects.get(pk=category_product['category'])
            category_dict['product_category'] = product_categories[0]
            array.append(category_dict)

    except Exception as e:
        print(e)
        return redirect('listArch:404-sayfasi')

    return render(request, 'home/company_info.html',
                  {'products': products, 'company': company, 'definitions': company_definition_array,
                   'category_product': array, 'retails': retails, 'collections': collection_array})


@api_view(http_method_names=['POST'])
def get_product(request):
    if request.POST:
        try:
            key = request.POST.get('product_name')
            if key == '':
                product = []
                data = ProductSerializer(product, many=True).data
                responseData = dict()
                responseData['product'] = data
                return JsonResponse(responseData, safe=True)
            else:
                # products = Product.objects.filter(  Q(name__icontains=key) | Q(category__name__icontains=key) |  Q(company__name__icontains=key)).distinct('id')

                products = ProductDesc.objects.filter(Q(product__name__icontains=key)).distinct('product_id')
                company = Company.objects.filter(product__name__icontains=key)
                magazine = IntroductionPageDesc.objects.filter(description__icontains=key)

                array = []

                data = ProductDescSerializer(products, many=True).data
                data2 = CompanySerializer(company, many=True).data
                data3 = IntroductionPageDescSerializer(magazine, many=True).data

                data_dict = dict()
                data_dict['product'] = data
                data_dict['company'] = data2
                data_dict['magazine'] = data3

                array.append(data_dict)
                responseData = dict()
                responseData['product'] = array

                print(array)

                return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_category_product(request):
    if request.POST:
        try:

            product_category = request.POST.get('product_category')
            category = Category.objects.filter(pk=product_category)

            product = Product.objects.filter(
                Q(category__category__parent=category) |
                Q(category=category) | Q(category__parent=category)).order_by('?')[:50]

            data = ProductSerializer(product, many=True)

            responseData = dict()
            responseData['product'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def filtered_products(request):
    if request.POST:
        try:

            checks = request.POST['parms[var2]']
            category = request.POST['category']
            filtered_products = request.POST['filtered_products']
            product_array = []
            filtered_array = []
            if filtered_products != '':
                filter_product = filtered_products.split(',')
                for id in filter_product:
                    product = Product.objects.filter(pk=int(id))
                    if product.count() > 0:
                        product_array.append(product[0])

            id_list = checks.split(',')
            array = []
            array_filter = []
            if id_list != ['']:
                for id in id_list:
                    value = OptionValue.objects.get(pk=int(id))
                    array.append(value.pk)
                products = ProductOptionValue.objects.filter(product__category__id=category).values(
                    'product').annotate(
                    count=Count('product'))
                array_filter = []

                for product_value in products:
                    product = ProductOptionValue.objects.filter(product_id=int(product_value['product']))
                    value_array = []
                    values = ProductOptionValue.objects.filter(product=product[0].product)

                    for value in values:
                        value_array.append(value.option_value.pk)

                    if set(value_array).__and__(set(array)) == set(array):
                        array_filter.append(product[0])
            else:
                filtered_array = ProductOptionValue.objects.filter(product__category__id=category)
                for product_filter in filtered_array:
                    if product_filter in array_filter:
                        array_filter.append(product_filter)

            new_array = []
            if filtered_products != '':
                for new_product in filtered_array:
                    for product in product_array:
                        if new_product == product:
                            productOptionValue = ProductOptionValue.objects.filter(product=new_product)
                            new_array.append(productOptionValue[0])
                            break

                data = ProductValueSerializer(new_array, many=True)
            else:
                data = ProductValueSerializer(array_filter, many=True)

            responseData = dict()
            responseData['products'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def filtered(request):
    if request.POST:
        try:
            tmp = request.POST['options']
            category = request.POST['category']
            options = json.loads(tmp)
            products_1 = dict()
            products_2 = dict()
            product_list = ProductOptionValue.objects.filter(product__category=Category.objects.get(pk=category))

            filtered_products = dict()
            if len(options) > 0:
                productOptionValue = dict()
                for item in options:
                    if options.index(item) == 0:
                        if item['type'] == 'range':
                            if options.index(item) == 0:
                                productOptionValue = ProductOptionValue.objects.filter(
                                    product__category__id=int(category)).distinct(
                                    'product').filter(
                                    option_value__option__id=int(item['option_id'])).filter(
                                    range_value__gte=int(item['value'].split('-')[0])).filter(
                                    range_value__lte=int(item['value'].split('-')[1]))
                            else:
                                x = ProductOptionValue.objects.filter(
                                    option_value__option__id=int(item['option_id'])).filter(
                                    range_value__gte=int(item['value'].split('-')[0])).distinct('product').filter(
                                    range_value__lte=int(item['value'].split('-')[1]))

                                productOptionValue = x and productOptionValue


                        elif item['type'] == 'checkbox':
                            productOptionValue = ProductOptionValue.objects.filter(
                                product__category__id=int(category)).distinct(
                                'product')
                            for value in item['values']:
                                new_productOptionValue = productOptionValue.filter(
                                    option_value__id=int(value)).distinct(
                                    'product')
                                for product in new_productOptionValue:
                                    products_1[product.product.pk] = product.product.pk
                                product_list = list(products_1.values())

                            for id in product_list:
                                product = Product.objects.get(pk=id)
                                filtered_products[id] = product

                        else:
                            print(productOptionValue)
                    else:
                        product_list_2 = list()
                        products_2 = dict()
                        if item['type'] == 'range':
                            if options.index(item) == 0:
                                productOptionValue = ProductOptionValue.objects.filter(
                                    product__category__id=int(category)).distinct(
                                    'product').filter(
                                    option_value__option__id=int(item['option_id'])).filter(
                                    range_value__gte=int(item['value'].split('-')[0])).filter(
                                    range_value__lte=int(item['value'].split('-')[1]))
                            else:
                                x = ProductOptionValue.objects.filter(
                                    option_value__option__id=int(item['option_id'])).filter(
                                    range_value__gte=int(item['value'].split('-')[0])).distinct('product').filter(
                                    range_value__lte=int(item['value'].split('-')[1]))

                                productOptionValue = x and productOptionValue


                        elif item['type'] == 'checkbox':
                            if options.index(item) == 0:
                                productOptionValue = ProductOptionValue.objects.filter(
                                    product__category__id=int(category)).distinct(
                                    'product')
                            for value in item['values']:
                                new_productOptionValue = productOptionValue.filter(
                                    option_value__id=int(value)).distinct(
                                    'product')
                                for product in new_productOptionValue:
                                    products_2[product.product.pk] = product.product.pk
                                product_list_2 = list(products_2.values())

                            set1 = set(product_list)
                            products_id = set1.intersection(product_list_2)
                            filter=dict()
                            for id in products_id:
                                product = Product.objects.get(pk=id)
                                filter[id] = product

                            filtered_products=filter
                            product_list=products_id
                        else:
                            print(productOptionValue)
            else:
                filtered_products = Product.objects.filter(category__id=int(category)).distinct(
                    'id')

            data = ProductSerializer(list(filtered_products.values()), many=True)

            responseData = dict()
            responseData['products'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:
            return JsonResponse({'status': 'Fail', 'msg': e})


def search_enter_product_name(request):
    array = []
    categories = Category.objects.all()
    options_value = OptionValue.objects.values('option', 'option__type').annotate(count=Count('value'))
    for option in options_value:
        option_dict = dict()
        option_dict['option'] = Option.objects.filter(pk=option['option'])[0]
        option_dict['values'] = OptionValue.objects.filter(option__id=option['option'])
        array.append(option_dict)
    if request.method == 'GET':
        product_name = request.GET['product_name']
        products = Product.objects.filter(
            Q(name__icontains=product_name) | Q(category__name__icontains=product_name) |
            Q(company__name__icontains=product_name))

    else:
        products = []

    array_product = []
    for product in products:
        if product not in array_product:
            array_product.append(product)

    return render(request, 'home/product-filter.html',
                  {'products': array_product, 'options': array, 'categories': categories})


def home_products(request, pk):
    cat = Category.objects.filter(pk=pk)
    category = CategoryDesc.objects.filter(category=cat[0]).filter(lang_code=home_lang_code)
    sub_categories = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(category__isActive=True).filter(
        category__parent__in=cat).order_by('category__order')
    products = ProductDesc.objects.filter(lang_code=int(home_lang_code)).filter(product__category__in=cat).filter(
        product__isAdvert=True).order_by('?')[:6]

    introductions = IntroductionPage.objects.values('title').annotate(dcount=Count('product'))
    array = []
    for introduction in introductions:
        title = IntroductionTitle.objects.get(pk=introduction['title'])
        introduction_products = IntroductionPage.objects.filter(product__category__in=cat).filter(
            title=title).order_by('?')[:4]
        if introduction_products.count() > 0:
            dict_introduction = dict()
            x = IntroductionPage.objects.filter(title=title).filter(isActive=True)
            dict_introduction['introduction'] = \
                IntroductionPageDesc.objects.filter(introduction=x[0]).filter(lang_code=home_lang_code)[
                    0]
            dict_introduction['title'] = \
                IntroductionTitleDesc.objects.filter(title=title).filter(lang_code=home_lang_code)[0]

            array.append(dict_introduction)

    blogs = BlogDesc.objects.filter(lang_code=home_lang_code)
    blog_array = []
    for blog in blogs:
        product_blogs = CompanyBlog.objects.filter(product__category__in=cat).filter(blog=blog.blog)
        if product_blogs.count() > 0:
            blog_dict = dict()
            blog_dict['blog'] = blog
            blog_dict['product'] = CompanyBlog.objects.filter(product__category__in=cat).filter(blog=blog.blog)[0]
            blog_array.append(blog_dict)

    return render(request, 'home/home-products.html',
                  {'products': products, 'introductions': array, 'blogs': blog_array, 'category': category[0],
                   'sub_categories': sub_categories})


def error_page(request):
    return render(request, 'home/notFound-page.html')


def contact_page(request):
    contact = Contact.objects.filter(isActive=True)
    return render(request, 'home/contact_page.html', {'contact': contact[0]})


def about_page(request):
    about = AboutDesc.objects.filter(lang_code=home_lang_code, about__isActive=True)
    if len(about) > 0:
        return render(request, 'home/about_page.html', {'about': about[0]})
    else:

        return render(request, 'home/about_page.html', {'about': '-'})


def profile_info(request):
    profiles = BusinessTypeDesc.objects.filter(lang_code=home_lang_code).filter(business_type__isProduct_based=False)
    return render(request, 'home/profile-info.html', {'profiles': profiles})


def profile_page(request):
    profiles = BusinessTypeDesc.objects.filter(lang_code=home_lang_code).filter(business_type__isProduct_based=True)
    business_type = BusinessType.objects.filter(isProduct_based=True)
    profile_blogs = ProfileBlog.objects.all()
    blog_array = []
    for blog in profile_blogs:
        blog_dict = dict()
        blog_dict['blog_name'] = \
            BusinessTypeDesc.objects.filter(business_type=blog.profile.profile_name).filter(lang_code=home_lang_code)[0]
        blog_dict['desc'] = BlogDesc.objects.filter(blog=blog.blog).filter(lang_code=home_lang_code)[0]
        blog_dict['images'] = BlogImage.objects.filter(blog=blog.blog).order_by('?')[:1]
        blog_dict['blog'] = blog
        blog_array.append(blog_dict)
    company_blog = CompanyBlog.objects.filter(company__business_type__in=business_type)
    array_company = []
    for company_blog in company_blog:
        company_blog_dict = dict()
        company_blog_dict['company'] = company_blog
        company_blog_dict['images'] = Product.objects.filter(company=company_blog.company).order_by('?')[:2]
        company_blog_dict['blog_desc'] = \
            BlogDesc.objects.filter(blog=company_blog.blog).filter(lang_code=home_lang_code)[0]
        company_blog_dict['profile_name'] = \
            BusinessTypeDesc.objects.filter(business_type=company_blog.company.business_type).filter(
                lang_code=home_lang_code)[0]
        array_company.append(company_blog_dict)

    return render(request, 'home/profile-page.html',
                  {'profiles': profiles, 'blogs': blog_array, 'company_blogs': array_company})


def blog_page(request):
    return render(request, 'home/blog-page.html')
