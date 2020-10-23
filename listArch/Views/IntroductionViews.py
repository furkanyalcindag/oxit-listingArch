from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render

from listArch.Forms.IntroductionProductForm import IntroductionProductForm
from listArch.Forms.IntroductionDescForm import IntroductionDescForm
from listArch.Forms.IntroductionForm import IntroductionForm
from listArch.models import IntroductionPage, IntroductionPageDesc, IntroductionProduct, IntroductionTitle
from listArch.models.IntroductionTitleDesc import IntroductionTitleDesc
from listArch.services import general_methods


def add_introduction_desc(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    introduction_form = IntroductionForm()
    introduction_desc_form = IntroductionDescForm()
    introduction_product_form = IntroductionProductForm()
    try:
        if request.method == 'POST':
            introduction_form = IntroductionForm(request.POST)
            introduction_desc_form = IntroductionDescForm(request.POST, request.FILES)
            introduction_product_form = IntroductionProductForm(request.POST)

            if introduction_form.is_valid() and introduction_desc_form.is_valid() and introduction_product_form.is_valid():

                introduction = IntroductionPage(key=introduction_form.cleaned_data['key'],
                                                category=introduction_form.cleaned_data['category'],
                                                isActive=introduction_form.cleaned_data['isActive'],
                                                title=introduction_form.cleaned_data['title'])
                introduction.save()

                introduction_desc = IntroductionPageDesc(introduction=introduction,
                                                         description=introduction_form.cleaned_data['key'], lang_code=1)
                introduction_desc.save()

                introduction_desc2 = IntroductionPageDesc(introduction=introduction,
                                                          description=introduction_desc_form.cleaned_data[
                                                              'description'], lang_code=2)
                introduction_desc2.save()

                for product in introduction_product_form.cleaned_data['product']:
                    introduction_product = IntroductionProduct(introduction=introduction, product=product)
                    introduction_product.save()

                messages.success(request, " Bilgiler Başarıyla Kayıt Edildi.")
                return redirect('listArch:tanitim-sayfasina-oge-ekle')
            else:
                messages.success(request, "Alanları kontrol ediniz.")

    except Exception as e:
        print(e)
    return render(request, 'Introduct/add-introduction-element.html',
                  {'introduction_form': introduction_form, 'introduction_desc_form': introduction_desc_form,
                   'introduction_product_form': introduction_product_form})


def update_introduction_desc(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    introduction = IntroductionPage.objects.get(pk=pk)
    introduction_form = IntroductionForm(request.POST or None, instance=introduction)

    introduction_tr = IntroductionPageDesc.objects.filter(introduction=introduction).filter(lang_code=1)
    introduction_eng = IntroductionPageDesc.objects.filter(introduction=introduction).filter(lang_code=2)
    introduction_desc_form = IntroductionDescForm(request.POST or None, instance=introduction_eng[0])

    products = IntroductionProduct.objects.filter(introduction=introduction)
    introduction_product_form = IntroductionProductForm(request.POST or None)
    try:
        if request.method == 'POST':

            if introduction_form.is_valid() and introduction_desc_form.is_valid() and introduction_product_form.is_valid():

                introduction.key = introduction_form.cleaned_data['key']
                introduction.category = introduction_form.cleaned_data['category']
                introduction.isActive = introduction_form.cleaned_data['isActive']
                introduction.title = introduction_form.cleaned_data['title']
                introduction.save()

                introduction_tr[0].description = introduction_form.cleaned_data['key']
                introduction_tr[0].save()

                introduction_eng[0].description = introduction_desc_form.cleaned_data['description']
                introduction_eng[0].save()

                for product in products:
                    product.delete()

                for product in introduction_product_form.cleaned_data['product']:
                    introduction_product = IntroductionProduct(introduction=introduction, product=product)
                    introduction_product.save()

                messages.success(request, "Bilgiler Başarıyla Kayıt Edildi.")
                return redirect('listArch:tanitim-urunleri')
            else:
                messages.success(request, "Alanları kontrol ediniz.")

    except Exception as e:
        print(e)
    return render(request, 'Introduct/add-introduction-element.html',
                  {'introduction_form': introduction_form, 'introduction_desc_form': introduction_desc_form,
                   'introduction_product_form': introduction_product_form})


def introduction_products(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    introductions = IntroductionProduct.objects.values('introduction').annotate(dcount=Count('product'))
    array = []
    for introduction in introductions:
        dict_introduction = dict()
        dict_introduction['introduction'] = IntroductionPage.objects.get(pk=introduction['introduction'])
        dict_introduction['products'] = IntroductionProduct.objects.filter(
            introduction=IntroductionPage.objects.get(pk=introduction['introduction']))
        array.append(dict_introduction)
    return render(request, 'Introduct/introductions.html', {'introductions': array})


def add_introduction_page_title(request):
    try:
        if request.method == 'POST':
            tr = request.POST['title_[tr]']
            eng = request.POST['title_[eng]']

            introduction_title = IntroductionTitle(key=tr)
            introduction_title.save()

            title_tr = IntroductionTitleDesc(title=introduction_title, lang_code=1, description=tr)
            title_tr.save()

            title_eng = IntroductionTitleDesc(title=introduction_title, lang_code=2, description=eng)
            title_eng.save()

            messages.success(request, "Başlık Kayıt Edildi.")
            return redirect('listArch:tanitim-urunleri-ana-baslik')

    except Exception as e:
        print(e)
    return render(request, 'Introduct/add-introduct-page-title.html')


def introduction_title(request):
    title_tr = IntroductionTitleDesc.objects.filter(lang_code=1)
    return render(request, 'Introduct/introduction-title.html', {'titles': title_tr, })


def update_introduction_page_title(request, pk):
    title = IntroductionTitle.objects.get(pk=pk)
    title_tr = IntroductionTitleDesc.objects.filter(lang_code=1).filter(title=title)[0]
    title_eng = IntroductionTitleDesc.objects.filter(lang_code=2).filter(title=title)[0]

    try:

        if request.method == 'POST':
            tr = request.POST['title_[tr]']
            eng = request.POST['title_[eng]']

            title_tr.description = tr
            title_tr.save()

            title_eng.description = eng
            title_eng.save()

            messages.success(request, "Başlık Kayıt Edildi.")
            return redirect('listArch:tanitim-urunleri-ana-baslik')

    except Exception as e:
        print(e)
    return render(request, 'Introduct/update-title.html', {'title_tr': title_tr, 'title_eng': title_eng})


def delete_introduction(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            id = request.POST['id']
            introduction = IntroductionTitle.objects.get(pk=id)
            introduction.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
