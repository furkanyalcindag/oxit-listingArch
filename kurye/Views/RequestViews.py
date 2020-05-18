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
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.Company import Company
from kurye.models.Customer import Customer
from kurye.models.Request import Request
from kurye.models.RequestSituationRequest import RequestSituationRequest
from kurye.models.RequestSituations import RequestSituations
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.models.TaskSituations import TaskSituations
from kurye.serializers.RequestSituationSerializer import RequestSituationSerializer
from kurye.services import general_methods
from kurye.services.general_methods import activeRequest


# Yeni müşteriyle talep oluşturma
def new_user_add_request(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request_form = RequestForm()
    customer_form = CustomerForm()
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)

    if request.method == 'POST':
        request_form = RequestForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if request_form.is_valid() and customer_form.is_valid():

            customer = Customer(customer=customer_form.cleaned_data['customer'],
                                address=customer_form.cleaned_data['address'],
                                phone=customer_form.cleaned_data['phone'],
                                city=customer_form.cleaned_data['city'],
                                district=customer_form.cleaned_data['district'],

                                )
            customer.save()
            customer.company = company
            customer.save()

            request1 = Request(receiver=customer,

                               payment_type=request_form.cleaned_data['payment_type'],
                               totalPrice=request_form.cleaned_data['totalPrice'],
                               exitDate=request_form.cleaned_data['exitDate'],
                               exitTime=request_form.cleaned_data['exitTime'],
                               description=request_form.cleaned_data['description'],

                               )
            request1.save()
            situation = RequestSituationRequest(request=request1,
                                                request_situation=RequestSituations.objects.get(name='Onaylandı'),
                                                isActive=True)
            situation.save()
            request1.company = company
            request1.save()

            subject, from_email, to = '' + request1.company.companyName + ' Talep Bilgileri', 'burcu.dogan@oxityazilim.com', user.email
            text_content = 'Talep Bilgileri'
            html_content = '<p><strong>Talep No: </strong>' + str(request1.pk) + '</p>'
            html_content = html_content + '<p> <strong>Adres:</strong>' + request1.receiver.address + '</p>'
            html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + request1.receiver.customer + '</p>'
            html_content = html_content + '<p><strong>Ödenecek Tutar: </strong>' + str(request1.totalPrice) + '₺</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            notification = Notification()
            notification.key = 'Talep'
            notification.message = '' + request1.company.companyName + ' adlı kullanıcı  ' + str(
                request1.exitDate) + '   ' + str(request1.exitTime) + ' tarihinde kurye talep etti.Talep No: ' + str(
                request1.pk) + ''
            notification.save()

            messages.success(request, 'Talebiniz Başarıyla Oluşturulmuştur')
            return redirect('kurye:yeni kullanıcıyla talep olustur')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz.')
    return render(request, 'Request/new-user-add-request.html',
                  {'request_form': request_form, 'customer_form': customer_form})


# Kayıtlı müşteriyle Talep oluşturma
def registered_user_add_request(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request_form = RegisteredUserRequestForm()
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.filter(profile=profile)

    if request.method == 'POST':
        request_form = RegisteredUserRequestForm(request.POST)

        if request_form.is_valid():

            request1 = Request(
                receiver=request_form.cleaned_data['receiver'],
                payment_type=request_form.cleaned_data['payment_type'],
                totalPrice=request_form.cleaned_data['totalPrice'],
                exitDate=request_form.cleaned_data['exitDate'],
                exitTime=request_form.cleaned_data['exitTime'],
                description=request_form.cleaned_data['description'],

            )
            request1.save()

            situation = RequestSituationRequest(request=request1,
                                                request_situation=RequestSituations.objects.get(name='Onaylandı'),
                                                isActive=True)
            situation.save()

            request1.company = company[0]
            request1.save()

            subject, from_email, to = '' + request1.company.companyName + ' Talep Bilgileri', 'burcu.dogan@oxityazilim.com', user.email
            text_content = 'Talep Bilgileri'
            html_content = '<p><strong>Talep No: </strong>' + str(request1.pk) + '</p>'
            html_content = html_content + '<p> <strong>Adres:</strong>' + request1.receiver.address + '</p>'
            html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + request1.receiver.customer + '</p>'
            html_content = html_content + '<p><strong>Ödenecek Tutar: </strong>' + str(request1.totalPrice) + '₺</p>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            notification = Notification()
            notification.key = 'Talep'
            notification.message = '' + request1.company.companyName + ' adlı kullanıcı ' + str(
                request1.exitDate) + '   ' + str(request1.exitTime) + ' tarihinde kurye talep etti. Talep No: ' + str(
                request1.pk) + ''
            notification.save()

            messages.success(request, 'Talebiniz Başarıyla Oluşturulmuştur')
            return redirect('kurye:kayıtlı kullanıcıyla talep olustur')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz.')
    return render(request, 'Request/registered-user-add-request.html',
                  {'request_form': request_form})


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
def return_approved_requests(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request1 = Request.objects.filter(isApprove=True)
    task = []
    request_array = []
    for request2 in request1:
        tasks = TaskSituationTask.objects.filter(task__request=request2).filter(isActive=True)
        if tasks.count() == 0:
            request_array.append(request2)
    return render(request, 'Request/approved-request.html',
                  {'approved_requests': request_array})


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
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Request.objects.get(pk=pk)
            obj.delete()
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

    tasks = TaskSituationTask.objects.filter(task__request__company_id=company.id).filter(isActive=True)

    return render(request, 'Company/company-requests.html',
                  {'tasks': tasks})


# Kullanıcı Talebi İptal Et
@login_required
def cancel_requests(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request1 = Request.objects.get(pk=pk)
    courier_company = User.objects.get(groups__name="Admin")
    task = TaskSituationTask.objects.filter(task__request=request1).filter(task_situation__name="Kurye Atandı").filter(
        isActive=True)

    if task:

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

            task.task_situation = TaskSituations.objects.get(name="İptal Edildi")
            task.save()

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
        notification.key = 'İptal Olan Talep'
        notification.message = '' + request1.company.companyName + ' adlı kullanıcı ' + str(request1.pk) + ' nolu talebi iptal etti'
        notification.save()

        messages.success(request, 'Talebiniz İptal Edildi')
    else:
        messages.warning(request, 'Talebinize ait kurye görevlendirilmiştir.Talebiniz iptal edilememektedir')
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
        task__isComplete=False)

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
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    request = RequestSituationRequest.objects.filter(request_id=pk).filter(request_situation__name="Onaylandı")
    data = RequestSituationSerializer(request, many=True)

    responseData = {}
    responseData['request'] = data.data
    responseData['request'][0]
    return JsonResponse(responseData, safe=True)
