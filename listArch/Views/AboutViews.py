from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from listArch.Forms.ContactForm import ContactForm
from listArch.Forms.HeaderTextForm import HeaderTextForm
from listArch.models.Log import Log
from listArch.models.ScrollingText import ScrollingText
from listArch.Forms.ScrollingTextForm import ScrollingTextForm
from listArch.models import About, AboutDesc, Contact, ScrollingTextDesc, HeaderTextDesc, HeaderText
from listArch.services import general_methods
from oxiterp.settings.base import home_lang_code


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
            log_content = '<p><strong style="color:red">ADMIN , HAKKIMIZDA </strong> yazısı ekledi.</p>'

            log = Log(user=request.user, content=log_content)
            log.save()

            messages.success(request, "Açıklama Başarıyla Kayıt Edildi.")
            return redirect('listArch:hakkimizda')

    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
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
            log_content = '<p><strong style="color:red">ADMIN , HAKKIMIZDA ID:' + about_id + ' </strong> yazısı sildi.</p>'
            log = Log(user=request.user, content=log_content)

            log.save()
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

            # about_tr[0] ile yapıldığında kayıt etmiyor.
            for tr in about_tr:
                tr.title_desc = request.POST['title[tr]']
                tr.description = request.POST['content[tr]']
                tr.save()

            for eng in about_eng:
                eng.title_desc = request.POST['title[eng]']
                eng.description = request.POST['content[eng]']
                eng.save()

            log_content = '<p><strong style="color:red">ADMIN , HAKKIMIZDA ID:' + str(
                about.pk) + ' </strong> yazısı güncellendi.</p>'
            log = Log(user=request.user, content=log_content)
            log.save()

            messages.success(request, "Açıklama Başarıyla Güncellendi.")
            return redirect('listArch:hakkimizda')

    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'About/update_about.html',
                  {'about_tr': about_tr[0], 'about_eng': about_eng[0]})


def add_contact(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    form = ContactForm()
    try:

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                contact = Contact(email=form.cleaned_data['email'], phone=form.cleaned_data['phone'],
                                  isActive=form.cleaned_data['isActive'])
                contact.save()

                log_content = '<p><strong style="color:red">ADMIN , İLETİŞİM ID:' + contact.pk + ' </strong> bilgisi ekledi.</p>'
                log = Log(user=request.user, content=log_content)
                log.save()

                messages.success(request, "İletişim Bilgileri Kayıt Edildi.")
                return redirect('listArch:iletisim-bilgisi')
            else:
                messages.success(request, "Alanları Kontrol Edin.")


    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
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
            if form.is_valid():
                contact.phone = form.cleaned_data['phone']
                contact.email = form.cleaned_data['email']
                contact.isActive = form.cleaned_data['isActive']
                contact.save()

                log_content = '<p><strong style="color:red">ADMIN , İLETİŞİM ID:' + str(
                    contact.pk) + ' </strong> bilgisini güncelledi.</p>'
                log = Log(user=request.user, content=log_content)
                log.save()

                messages.success(request, "İletişim Bilgileri Kayıt Edildi.")
                return redirect('listArch:iletisim-bilgisi')
            else:
                messages.success(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
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
            log_content = '<p><strong style="color:red">ADMIN , İLETİŞİM:' + contact.phone + ' - ' + contact.email + ' </strong> bilgisini sildi.</p>'
            contact.delete()

            log = Log(user=request.user, content=log_content)
            log.save()

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
            if form.is_valid():
                scrolling_text = ScrollingText(key=request.POST['scrolling[tr]'],
                                               isActive=form.cleaned_data['isActive'])
                scrolling_text.save()

                scrolling_tr = ScrollingTextDesc(text=scrolling_text, description=request.POST['scrolling[tr]'],
                                                 lang_code=1, subTextDesc=request.POST['subText[tr]'])
                scrolling_tr.save()

                scrolling_eng = ScrollingTextDesc(text=scrolling_text, description=request.POST['scrolling[eng]'],
                                                  lang_code=2, subTextDesc=request.POST['subText[eng]'])
                scrolling_eng.save()

                log_content = '<p><strong style="color:red">ADMIN , Search Yazı:' + scrolling_tr.description + ' </strong> bilgisini ekledi.</p>'
                log = Log(user=request.user, content=log_content)
                log.save()

                messages.success(request, "Yazı Kayıt Edildi.")
                return redirect('listArch:kayan-yazi')
            else:
                messages.success(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')

    return render(request, 'About/add-scrolling-text.html', {'form': form})


def scrolling(request):
    scrolling_tr = ScrollingTextDesc.objects.filter(lang_code=1)
    return render(request, 'About/scrolling-text.html', {'scrolling_texts': scrolling_tr})


def update_scrolling(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    scrolling = ScrollingText.objects.get(pk=pk)
    form = ScrollingTextForm(request.POST or None, instance=scrolling)
    scrolling_tr = ScrollingTextDesc.objects.filter(lang_code=1, text_id=pk)
    scrolling_eng = ScrollingTextDesc.objects.filter(lang_code=2, text_id=pk)

    try:

        if request.method == 'POST':
            if form.is_valid():
                scrolling.key = request.POST['scrolling[tr]']
                scrolling.isActive = form.cleaned_data['isActive']
                scrolling.save()

                for tr in scrolling_tr:
                    tr.description = request.POST['scrolling[tr]']
                    tr.subTextDesc = request.POST['subText[tr]']
                    tr.save()
                for eng in scrolling_eng:
                    eng.description = request.POST['scrolling[eng]']
                    eng.subTextDesc = request.POST['subText[eng]']
                    eng.save()

                log_content = '<p><strong style="color:red">ADMIN , Search Yazı:' + str(
                    scrolling.pk) + ' </strong> bilgisini güncelledi.</p>'
                log = Log(user=request.user, content=log_content)
                log.save()
                messages.success(request, "Yazı Kayıt Edildi.")
                return redirect('listArch:kayan-yazi')

            else:
                messages.success(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    if scrolling_eng.count() > 0 and scrolling_tr.count() > 0:
        return render(request, 'About/add-scrolling-text.html',
                  {'scrolling_tr': scrolling_tr[0], 'scrolling_eng': scrolling_eng[0], 'form': form})
    else:
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
            log_content = '<p><strong style="color:red">ADMIN , Search Yazı:' + text.key + ' </strong> bilgisini sildi.</p>'
            text.delete()

            log = Log(user=request.user, content=log_content)
            log.save()
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
            if form.is_valid():
                headerText = HeaderText(key=request.POST['content[tr]'], isActive=form.cleaned_data['isActive'])
                headerText.save()

                headerTextDesc = HeaderTextDesc(headerText=headerText, lang_code=1,
                                                description=request.POST['content[tr]'])
                headerTextDesc.save()

                headerTextDesc2 = HeaderTextDesc(headerText=headerText, lang_code=2,
                                                 description=request.POST['content[eng]'])
                headerTextDesc2.save()

                log_content = '<p><strong style="color:red">ADMIN , Üst Menü Yazısı:' + headerTextDesc.description + ' </strong>  ekledi.</p>'
                log = Log(user=request.user, content=log_content)
                log.save()

                messages.success(request, "Üst Menü Yazısı Başarıyla Kayıt Edildi.")
                return redirect('listArch:ust-menu-yazi')
            else:
                messages.success(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
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
    form = HeaderTextForm(request.POST or None, instance=headerText)

    try:
        if HeaderTextDesc.objects.filter(lang_code=home_lang_code).count() > 0:

            if request.method == 'POST':
                if form.is_valid():
                    headerText.key = request.POST['content[tr]']
                    headerText.isActive = form.cleaned_data['isActive']
                    headerText.save()

                    for tr in header_tr:
                        tr.description = request.POST['content[tr]']
                        tr.save()
                    for eng in header_eng:
                        eng.description = request.POST['content[eng]']
                        eng.save()

                    log_content = '<p><strong style="color:red">ADMIN , Üst Menü Yazısını </strong> güncelledi.</p>'
                    log = Log(user=request.user, content=log_content)
                    log.save()

                    messages.success(request, "Üst Menü Yazısı Başarıyla Güncellendi.")
                    return redirect('listArch:ust-menu-yazi')
                else:
                    messages.success(request, "Alanları Kontrol Edin.")
    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')
    return render(request, 'About/update-headerText.html',
                  {'header_tr': header_tr, 'header_eng': header_eng, 'form': form})


def delete_headerText(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            id = request.POST['id']
            text = HeaderText.objects.get(pk=id)
            log_content = '<p><strong style="color:red">ADMIN , Üst Menü Yazı ID: ' + text.pk + ' </strong> güncelledi.</p>'

            text.delete()

            log = Log(user=request.user, content=log_content)
            log.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def admin_error_page(request):
    return render(request, 'admin-404.html')
