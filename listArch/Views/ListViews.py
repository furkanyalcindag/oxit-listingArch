from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from listArch.models import ListProduct, Product, ProductDesc, Customer, Company
from listArch.models.List import List
from listArch.services import general_methods


def addList(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    try:

        if request.method == 'POST':
            list = List(list_name=request.POST['list_name'], user=request.user, type=request.POST['list_type'],
                        description=request.POST['description'])
            list.save()

            reference_list = request.POST['reference_list']
            if reference_list != 'Yok' and reference_list != 'Bağlantılı Liste':
                list.reference_list = List.objects.get(list_name=reference_list)
                list.save()

            product_id = request.POST['product']
            product = Product.objects.get(pk=product_id)

            product_list = ListProduct(list=list, product=product)
            product_list.save()

            messages.success(request, "Listenize ürün eklendi")
            return redirect('listArch:kullanici-listeleri')


    except Exception as e:
        print(e)
    return redirect('listArch:kullanici-listeleri')


def delete_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            list_id = request.POST['list_id']
            list = List.objects.get(pk=list_id)
            list.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def list_detail(request, pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    user_list = List.objects.filter(user=user)
    list = List.objects.get(pk=pk)
    list_product = ListProduct.objects.filter(list=list)
    return render(request, 'User/list-detail.html',
                  {'list_product': list_product, 'list': list, 'customer': customer, 'user_list': user_list})


def print_list_page(request, pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    user_list = List.objects.filter(user=user)
    list = List.objects.get(pk=pk)
    list_product = ListProduct.objects.filter(list=list)
    company=Company.objects.get(user=user)
    return render(request, 'User/list_print_page.html',
                  {'list_product': list_product, 'list': list, 'customer': customer, 'user_list': user_list,'company':company})


def add_product_list(request):
    if request.POST:
        try:
            list_id = request.POST['list_id']
            product_id = request.POST['product_id']
            list = List.objects.filter(pk=list_id)
            list_product = ListProduct(list=list[0], product=Product.objects.filter(pk=product_id)[0])
            list_product.save()
            messages.success(request, "Ürün Listenize Başarıyla Eklendi.")
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
