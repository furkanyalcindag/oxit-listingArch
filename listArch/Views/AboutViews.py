from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from listArch.Forms.ContactForm import ContactForm
from listArch.Forms.HeaderTextForm import HeaderTextForm
from listArch.models.ScrollingText import ScrollingText
from listArch.Forms.ScrollingTextForm import ScrollingTextForm
from listArch.models import About, AboutDesc, Contact, ScrollingTextDesc, HeaderTextDesc, HeaderText
from listArch.services import general_methods


def add_about(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        if request.method == 'POST':
            about = About(key=request.POST['title[tr]'])
            about.save()

            if request.POST['isActive'] == 'on':
                about.isActive = True
                about.save()

            aboutDesc = AboutDesc(about=about, lang_code=1,
                                  title_desc=request.POST['title[tr]'],
                                  description=request.POST['content[tr]'])
            aboutDesc.save()

            aboutDesc2 = AboutDesc(about=about, lang_code=2,
                                   title_desc=request.POST['title[eng]'],
                                   description=request.POST['content[eng]'])
            aboutDesc2.save()

            messages.success(request, "Açıklama Başarıyla Kayıt Edildi.")
            return redirect('listArch:hakkimizda')

    except Exception as e:
        print(e)
    return render(request, 'About/add-about.html')


def about(request):
    about = About.objects.all()
    return render(request, 'About/about-list.html', {'abouts': about})


def delete_about(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            about_id = request.POST['about_id']
            about = About.objects.get(pk=about_id)
            about.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def about_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    about = About.objects.get(pk=pk)
    about_tr = AboutDesc.objects.filter(about=about).filter(lang_code=1).filter(about__isActive=True)
    about_eng = AboutDesc.objects.filter(about=about).filter(lang_code=2).filter(about__isActive=True)
    try:

        if request.method == 'POST':
            about.key = request.POST['title[tr]']
            about.save()

            about_tr[0].title_desc = request.POST['title[tr]']
            about_tr[0].description = request.POST['content[tr]']
            about_tr[0].save()

            about_eng[0].title_desc = request.POST['title[eng]']
            about_eng[0].description = request.POST['content[eng]']
            about_eng[0].save()

            messages.success(request, "Açıklama Başarıyla Güncellendi.")
            return redirect('listArch:hakkimizda-guncelle', pk)

    except Exception as e:
        print(e)
    return render(request, 'product/add-product-definition.html', {'about_tr': about_tr[0], 'about_eng': about_eng[0]})


def add_contact(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    form = ContactForm()
    try:

        if request.method == 'POST':
            form = ContactForm(request.POST)
            contact = Contact(email=form.cleaned_data['email'], phone=form.cleaned_data['phone'],
                              isActive=form.cleaned_data['isActive'])
            contact.save()

            messages.success(request, "İletişim Bilgileri Kayıt Edildi.")
            return redirect('listArch:iletisim-bilgisi')

    except Exception as e:
        print(e)
    return render(request, 'About/add-contact.html', {'form': form})


def update_contact(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    contact = Contact.objects.get(pk=pk)
    form = ContactForm(request.POST or None, instance=contact)
    try:
        if request.method == 'POST':
            contact.phone = form.cleaned_data['phone']
            contact.email = form.cleaned_data['email']
            contact.isActive = form.cleaned_data['isActive']
            contact.save()

            messages.success(request, "İletişim Bilgileri Kayıt Edildi.")
            return redirect('listArch:iletisim-bilgisi')

    except Exception as e:
        print(e)
    return render(request, 'About/add-contact.html', {'form': form})


def get_contact(request):
    contact = Contact.objects.all()
    return render(request, 'About/contact.html', {'contact': contact})


def delete_contact(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            contact_id = request.POST['contact_id']
            contact = Contact.objects.get(pk=contact_id)
            contact.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def add_scrolling(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    form = ScrollingTextForm()
    try:

        if request.method == 'POST':
            form = ScrollingTextForm(request.POST)

            scrolling_text = ScrollingText(key=request.POST['scrolling[tr]'],
                                           isActive=form.cleaned_data['isActive'])
            scrolling_text.save()

            scrolling_tr = ScrollingTextDesc(text=scrolling_text, description=request.POST['scrolling[tr]'],
                                             lang_code=1, subTextDesc=request.POST['subText[tr]'])
            scrolling_tr.save()

            scrolling_eng = ScrollingTextDesc(text=scrolling_text, description=request.POST['scrolling[eng]'],
                                              lang_code=2, subTextDesc=request.POST['subText[eng]'])
            scrolling_eng.save()

            messages.success(request, "Yazı Kayıt Edildi.")
            return redirect('listArch:kayan-yazi')

    except Exception as e:
        print(e)

    return render(request, 'About/add-scrolling-text.html', {'form': form})


def scrolling(request):
    scrolling_tr = ScrollingTextDesc.objects.filter(lang_code=1)
    return render(request, 'About/scrolling-text.html', {'scrolling_texts': scrolling_tr})


def update_scrolling(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    scrolling = ScrollingText.objects.filter(pk=pk)
    form = ScrollingTextForm(request.POST or None, instance=scrolling[0])
    scrolling_tr = ScrollingTextDesc.objects.filter(lang_code=1, text_id=pk)[0]
    scrolling_eng = ScrollingTextDesc.objects.filter(lang_code=2, text_id=pk)[0]

    try:

        if request.method == 'POST' and form.is_valid():
            scrolling[0].key = request.POST['scrolling[tr]']
            scrolling[0].isActive = form.cleaned_data['isActive']
            scrolling[0].save()

            scrolling_tr.description = request.POST['scrolling[tr]']
            scrolling_tr.subTextDesc = request.POST['subText[tr]']
            scrolling_tr.save()

            scrolling_eng.description = request.POST['scrolling[eng]']
            scrolling_eng.subTextDesc = request.POST['subText[eng]']
            scrolling_eng.save()

            messages.success(request, "Yazı Kayıt Edildi.")

    except Exception as e:
        print(e)

    return render(request, 'About/add-scrolling-text.html',
                  {'scrolling_tr': scrolling_tr, 'scrolling_eng': scrolling_eng, 'form': form})


def delete_scrolling(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            id = request.POST['id']
            text = ScrollingText.objects.get(pk=id)
            text.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def add_header_text(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    form = HeaderTextForm()
    try:
        if request.method == 'POST':
            form = HeaderTextForm(request.POST)

            headerText = HeaderText(key=request.POST['content[tr]'], isActive=form.cleaned_data['isActive'])
            headerText.save()

            headerTextDesc = HeaderTextDesc(headerText=headerText, lang_code=1,
                                            description=request.POST['content[tr]'])
            headerTextDesc.save()

            headerTextDesc2 = HeaderTextDesc(headerText=headerText, lang_code=2,
                                             description=request.POST['content[eng]'])
            headerTextDesc2.save()

            messages.success(request, "Üst Menü Yazısı Başarıyla Kayıt Edildi.")
            return redirect('listArch:ust-menu-yazi')

    except Exception as e:
        print(e)
    return render(request, 'About/add-header-text.html', {'form': form})


def headerText(request):
    headerText_tr = HeaderTextDesc.objects.filter(lang_code=1)
    return render(request, 'About/header-text.html', {'headerText': headerText_tr})


def update_headerText(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    headerText = HeaderText.objects.get(pk=pk)
    header_tr = HeaderTextDesc.objects.filter(headerText__isActive=True).filter(headerText=headerText).filter(
        lang_code=1)
    header_eng = HeaderTextDesc.objects.filter(headerText__isActive=True).filter(headerText=headerText).filter(
        lang_code=2)

    form = HeaderTextForm(request.POST or None, instance=HeaderText)
    try:

        if request.method == 'POST':
            headerText.key = request.POST['content[tr]']
            headerText.isActive = form.cleaned_data['isActive']
            headerText.save()

            header_tr[0].description = request.POST['content[tr]']
            header_tr[0].save()

            header_eng[0].description = request.POST['content[eng]']
            header_eng[0].save()

            messages.success(request, "Üst Menü Yazısı Başarıyla Güncellendi.")
            return redirect('listArch:ust-menu-yazi')

    except Exception as e:
        print(e)
    return render(request, 'About/update-headerText.html',
                  {'header_tr': header_tr[0], 'header_eng': header_eng[0], 'form': form})


def delete_headerText(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            id = request.POST['id']
            text = HeaderText.objects.get(pk=id)
            text.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
