import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from kurye.Forms.CustomerForm import CustomerForm
from kurye.Forms.RegisteredUserRequestForm import RegisteredUserRequestForm
from kurye.Forms.RequestForm import RequestForm
from kurye.models import Neighborhood
from kurye.models.City import City
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.Company import Company
from kurye.models.Customer import Customer
from kurye.models.Request import Request
from kurye.models.RequestSituationRequest import RequestSituationRequest
from kurye.models.RequestSituations import RequestSituations
from kurye.models.Task import Task
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.models.TaskSituations import TaskSituations
from kurye.serializers.RequestSituationSerializer import RequestSituationSerializer
from kurye.services import general_methods
from kurye.services.general_methods import activeRequest, save_log


# Yeni müşteriyle talep oluşturma
def new_user_add_request(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request_form = RequestForm(initial={'exitDate': datetime.datetime.today().strftime('%Y-%m-%d'),
                                        'exitTime': datetime.datetime.today().strftime('%H:%M')})
    customer_form = CustomerForm()
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    cities = City.objects.all()
    today = datetime.date.today()

    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        customer_form = CustomerForm(request.POST)
        city_id = request.POST['city']
        city = City.objects.get(pk=city_id)

        if request_form.is_valid() and customer_form.is_valid():

            if request_form.cleaned_data['exitDate'] < datetime.date.today():
                messages.warning(request, 'Geçmiş Tarihli Talep Oluşturamazsınız.')
                return redirect('kurye:yeni kullanıcıyla talep olustur')
            elif request_form.cleaned_data['exitTime'] > datetime.datetime.now().time():
                customer = Customer(customer=customer_form.cleaned_data['customer'],
                                    address=customer_form.cleaned_data['address'],
                                    phone=customer_form.cleaned_data['phone'],
                                    city=city,
                                    district=customer_form.cleaned_data['district'],
                                    neighborhood=customer_form.cleaned_data['neighborhood'],

                                    )
                customer.save()
                customer.company = company
                customer.save()
                price = ""
                discount_price = 0
                neighborhood_name = customer.neighborhood
                neighborhood = Neighborhood.objects.filter(neighborhood_name=neighborhood_name)
                for neighborhood in neighborhood:
                    price = neighborhood.price
                    discount_price = price - (price * company.discount / 100)
                # Mahalleye göre fiyat

                request1 = Request(receiver=customer,
                                   payment_type=request_form.cleaned_data['payment_type'],
                                   totalPrice=request_form.cleaned_data['totalPrice'],
                                   exitTime=request_form.cleaned_data['exitTime'],
                                   description=request_form.cleaned_data['description'],
                                   request_price=price, discount_price=discount_price,)
                request1.save()

                if request_form.cleaned_data['exitDate']:
                    request1.exitDate = request_form.cleaned_data['exitDate']
                    request1.save()
                else:
                    request1.exitDate = datetime.datetime.now()
                    request1.save()

                situation = RequestSituationRequest(request=request1,
                                                    request_situation=RequestSituations.objects.get(name='Onaylandı'),
                                                    isActive=True)
                situation.save()
                request1.company = company
                request1.save()

                log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                              groups[0].name + ', ' + str(request1.pk) + '</strong> nolu talebi oluşturdu</p>'

                save_log(profile.pk, log_content)

                subject, from_email, to = '' + request1.company.companyName + ' Talep Bilgileri', 'burcu.dogan@oxityazilim.com', user.email
                text_content = 'Talep Bilgileri'
                html_content = '<p><strong>Talep No: </strong>' + str(request1.pk) + '</p>'
                html_content = html_content + '<p> <strong>Adres:</strong>' + request1.receiver.address + '</p>'
                html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + request1.receiver.customer + '</p>'
                html_content = html_content + '<p><strong>Ödenecek Tutar: </strong>' + str(
                    request1.totalPrice) + '₺</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                notification = Notification()
                notification.key = 'Talep'
                notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
                notification.message = '' + request1.company.companyName + ' adlı kullanıcı  ' + str(
                    request1.exitDate) + '   ' + str(
                    request1.exitTime) + ' tarihinde kurye talep etti.Talep No: ' + str(
                    request1.pk) + ''
                notification.save()

                messages.success(request,
                                 'Talebiniz Başarıyla Oluşturulmuştur. En Kısa Sürede Kurye görevlendirilecektir.')
                return redirect('kurye:yeni kullanıcıyla talep olustur')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz.')

    return render(request, 'Request/new-user-add-request.html',
                  {'request_form': request_form, 'customer_form': customer_form, 'cities': cities, 'today': today})


# Kayıtlı müşteriyle Talep oluşturma
def registered_user_add_request(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request_form = RequestForm(initial={'exitDate': datetime.datetime.today().strftime('%Y-%m-%d'),
                                        'exitTime': datetime.datetime.today().strftime('%H:%M')})
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    company = Company.objects.filter(profile=profile)
    today = datetime.date.today()
    receivers = Customer.objects.filter(company_id=company[0].pk).filter(isActive=True)
    date = datetime.date.today()
    cities = City.objects.all()
    neighborhood = Neighborhood.objects.all()
    if request.method == 'POST':
        request_form = RegisteredUserRequestForm(request.POST)

        if request_form.is_valid():

            if request_form.cleaned_data['exitDate'] < datetime.date.today():
                messages.warning(request, 'Geçmiş Tarihli Talep Oluşturamazsınız.')
                return redirect('kurye:yeni kullanıcıyla talep olustur')
            elif request_form.cleaned_data['exitTime'] > datetime.datetime.now().time():

                customer = Customer.objects.get(pk=int(request.POST['receiver']))

                request1 = Request(
                    exitTime=request_form.cleaned_data['exitTime'],
                    receiver=customer,
                    payment_type=request_form.cleaned_data['payment_type'],
                    totalPrice=request_form.cleaned_data['totalPrice'],
                    description=request_form.cleaned_data['description'],

                )
                request1.save()

                if request.POST['address-value']:

                    city = City.objects.get(pk=int(request.POST['city']))
                    request1.city = city
                    request1.district = request.POST['ilce']
                    neighborhood = Neighborhood.objects.get(neighborhood_name=request.POST['mahalle'])
                    request1.neighborhood = neighborhood
                    request1.request_price = neighborhood.price
                    price = neighborhood.price
                    request1.discount_price = price - (price * company[0].discount / 100)
                    request1.address = request.POST['address']
                    request1.save()

                else:
                    neighborhood = Neighborhood.objects.get(neighborhood_name=customer.neighborhood)
                    price = neighborhood.price  # Mahalleye göre fiyat
                    request1.request_price = price
                    request1.discount_price = price - (price * company[0].discount / 100)
                    request1.save()

                if request_form.cleaned_data['exitDate']:
                    request1.exitDate = request_form.cleaned_data['exitDate']
                    request1.save()
                else:
                    request1.exitDate = datetime.datetime.now()
                    request1.save()

                situation = RequestSituationRequest(request=request1,
                                                    request_situation=RequestSituations.objects.get(name='Onaylandı'),
                                                    isActive=True)
                situation.save()

                request1.company = company[0]
                request1.save()

                log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                              groups[0].name + ', ' + str(request1.pk) + '</strong> nolu talebi oluşturdu</p>'

                save_log(profile.pk, log_content)

                subject, from_email, to = '' + request1.company.companyName + ' Talep Bilgileri', 'burcu.dogan@oxityazilim.com', user.email
                text_content = 'Talep Bilgileri'
                html_content = '<p><strong>Talep No: </strong>' + str(request1.pk) + '</p>'
                html_content = html_content + '<p> <strong>Adres:</strong>' + request1.receiver.address + '</p>'
                html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + request1.receiver.customer + '</p>'
                html_content = html_content + '<p><strong>Ödenecek Tutar: </strong>' + str(
                    request1.totalPrice) + '₺</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                notification = Notification()
                notification.key = 'Talep'
                notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
                notification.message = '' + request1.company.companyName + ' adlı kullanıcı ' + str(
                    request1.exitDate) + '   ' + str(
                    request1.exitTime) + ' tarihinde kurye talep etti. Talep No: ' + str(
                    request1.pk) + ''
                notification.save()

                messages.success(request,
                                 'Talebiniz Başarıyla Oluşturulmuştur.En Kısa Sürede Kurye görevlendirilecektir.')
                return redirect('kurye:kayıtlı kullanıcıyla talep olustur')
            else:
                messages.warning(request, 'Bugün İçin Çıkış Zamanını Mevcut Saat Aralığında Seçiniz.')

        else:
            messages.warning(request, 'Alanları Kontrol Ediniz.')

    return render(request, 'Request/registered-user-add-request.html',
                  {'request_form': request_form, 'today': today, 'receivers': receivers, 'date': date, 'cities': cities,
                   'neigborhoods': neighborhood})


# Bekleyen Talepler
@login_required
def return_pending_request(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    requests = Request.objects.filter(isApprove=False).order_by('creationDate')

    request_situations = RequestSituations.objects.all()
    return render(request, 'Request/pending-requests.html',
                  {'requests': requests, 'request_situations': request_situations})


# Onaylanmış Talepler
@login_required
def return_company_canceled_requests(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    requests = RequestSituationRequest.objects.filter(isActive=True).filter(request_situation__name='İptal Edildi')

    return render(request, 'Request/company-canceled-request.html',
                  {'requests': requests})


# Talep Onayla
@login_required
def pendingRequestActive(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            request_id = request.POST.get('request_id')

            activeRequest(request, int(request_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Request.DoesNotExist:

            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


# Talep Sil
@login_required
def pending_request_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Request.objects.get(pk=pk)
            obj.delete()

            log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                          groups[0].name + ' , ' + str(pk) + '</strong> nolu talebi sildi</p>'

            save_log(profile.pk, log_content)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Request.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


# Kullanıcının Aktif Talepleri
@login_required
def return_company_requests(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)

    tasks = TaskSituationTask.objects.filter(isActive=True).filter(task__request__company_id=company.id).order_by(
        '-creationDate')

    return render(request, 'Company/company-requests.html',
                  {'tasks': tasks})


# Kullanıcının Talepleri
@login_required
def company_all_requests(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    requests = []
    all_requests = RequestSituationRequest.objects.filter(request__company_id=company.pk).order_by('-creationDate')
    for request1 in all_requests:
        task = TaskSituationTask.objects.filter(task__request__company=company).filter(task__request=request1.request)
        if task.count() <= 0:
            requests.append(request1)

    return render(request, 'Company/company-all-requests.html', {'requests': requests})


# Kullanıcı Talebi İptal Et
@login_required
def cancel_requests(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    request1 = Request.objects.get(uuid=uuid)
    current_task = Task.objects.get(request=request1)
    courier_company = User.objects.get(groups__name="Admin")
    task = TaskSituationTask.objects.filter(task__request=request1).filter(
        Q(task_situation__name="Kurye Atandı")).filter(
        isActive=True)

    if task.count() > 0:

        active_request = RequestSituationRequest.objects.filter(request=request1).filter(isActive=True)

        # önceki talep durumu pasif yapılıyor
        for active in active_request:
            active.isActive = False
            active.save()

        # yeni talep durumu ekleniyor
        cancel_request = RequestSituationRequest(request=request1, isActive=True,
                                                 request_situation=RequestSituations.objects.get(name="İptal Edildi"))
        cancel_request.save()

        for task in task:
            task.isActive = False
            task.save()

        active_task_situation = TaskSituations.objects.get(name='İptal Edildi')
        active_task = TaskSituationTask(task=current_task, task_situation=active_task_situation,
                                        isActive=True)
        active_task.save()

        log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                      groups[0].name + ' , ' + str(request1.pk) + '</strong> nolu talebi iptal etti</p>'

        save_log(profile.pk, log_content)

        subject, from_email, to = '' + request1.company.companyName + ' Bilgilendirme', 'burcu.dogan@oxityazilim.com', courier_company.email
        html_content = 'Müşterimizin isteği doğrultusunda ' + str(request1.pk) + ' nolu talebimiz iptal edildi. '
        msg = EmailMultiAlternatives(subject, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        subject, from_email, to = '' + request1.company.companyName + ' Bilgilendirme', 'burcu.dogan@oxityazilim.com', request1.receiver.email
        html_content = 'İptal talebiniz başarıyla gerçekleştirilmiştir.'
        msg = EmailMultiAlternatives(subject, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        notification = Notification()
        notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
        notification.key = 'İptal Olan Talep'
        notification.message = '' + request1.company.companyName + ' adlı kullanıcı ' + str(
            request1.pk) + ' nolu talebi iptal etti'
        notification.save()

        messages.success(request, 'Talebiniz İptal Edildi')
    else:
        messages.warning(request, 'Kurye Yola Çıkmıştır.Talebiniz iptal edilememektedir.')
    return redirect("kurye:kullanıcı aktif talepleri")


# Kullanıcının Tamamlayacağı Talepler
@login_required
def return_company_ending_tasks(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)

    tasks = TaskSituationTask.objects.filter(task__request__company_id=company.pk).filter(
        Q(task_situation__name='Teslim Edildi') | Q(task_situation__name='Teslim Edilemedi')).filter(
        task__isComplete=False).filter(isActive=True)

    return render(request, 'Company/company-ending-requests.html',
                  {'tasks': tasks})


# İptal Edilen Talepler
@login_required
def return_canceled_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    tasks = RequestSituationRequest.objects.filter(isActive=True).filter(request_situation__name='İptal Edildi')

    return render(request, 'Task/cancel-tasks.html',
                  {'tasks': tasks})


@api_view()
def getRequest(request, pk):
    request = RequestSituationRequest.objects.filter(pk=pk)
    data = RequestSituationSerializer(request, many=True)

    responseData = {}
    responseData['request'] = data.data
    responseData['request'][0]
    return JsonResponse(responseData, safe=True)
