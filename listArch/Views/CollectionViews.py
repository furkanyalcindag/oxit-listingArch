from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect, render

from listArch.models import Product, Company, Collection, CollectionProduct
from listArch.serializers.ProductSerializer import ProductSerializer
from listArch.services import general_methods


def add_collection(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            company = Company.objects.get(pk=int(request.POST['company_id']))
            collection = Collection(company=company, name=request.POST['name'])
            collection.save()
            return JsonResponse({'status': 'Success', 'id': collection.pk, 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def add_collection_company(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    company = ""
    company_products = ""
    collections = ""
    try:
        company = Company.objects.get(pk=pk)
        company_products = Product.objects.filter(company=company)
        collections = Collection.objects.filter(company=company)

    except Exception as e:
        print(e)
    return render(request, 'Collection/add_collection_company.html',
                  {'company_products': company_products, 'company': company.pk, 'collections': collections})


def add_product_to_collection(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:
            product = Product.objects.get(pk=request.POST['product'])
            collection_id = request.POST['collection_id']
            collection = Collection.objects.get(pk=collection_id)

            products = CollectionProduct.objects.filter(collection=collection).filter(product=product)
            if products.count() == 0:
                collection_product = CollectionProduct(collection=collection, product=product)
                collection_product.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
            else:
                return JsonResponse({'status': 'Warning', 'messages': 'Bu ürün koleksiyonda zaten var'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def get_collection(request):
    if request.POST:
        try:

            collection_id = request.POST.get('collection')
            collection = Collection.objects.get(pk=collection_id)
            products = Product.objects.filter(company=collection.company)

            data = ProductSerializer(products, many=True)

            responseData = dict()
            responseData['products'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
