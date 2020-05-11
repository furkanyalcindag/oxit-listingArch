from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from kurye.Forms.CustomerForm import CustomerForm
from kurye.Forms.ProfileForm import ProfileForm
from kurye.Forms.RegisteredUserRequestForm import RegisteredUserRequestForm
from kurye.Forms.RequestForm import RequestForm
from kurye.Forms.UserForm import UserForm
from kurye.models import Profile, Company
from kurye.models.Customer import Customer
from kurye.models.Request import Request
from kurye.models.RequestSituations import RequestSituations
from kurye.serializers.RequestSerializer import RequestSerializer
from kurye.services import general_methods
from kurye.services.general_methods import activeRequest


# Yeni müşteriyle talep oluşturma
def new_user_add_request(request):
    request_form = RequestForm()
    customer_form = CustomerForm()
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.filter(profile=profile)

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

            request1 = Request(receiver=customer,

                               payment_type=request_form.cleaned_data['payment_type'],
                               totalPrice=request_form.cleaned_data['totalPrice'],
                               exitDate=request_form.cleaned_data['exitDate'],
                               exitTime=request_form.cleaned_data['exitTime'],
                               description=request_form.cleaned_data['description'],

                               )
            request1.save()
            request1.request_situation.add(RequestSituations.objects.get(name='Onay Bekliyor'))
            request1.company = company[0]
            request1.save()

            messages.success(request, 'Talebiniz Bşarıyla Oluşturulmuştur')
            return redirect('kurye:yeni kullanıcıyla talep olustur')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz.')
    return render(request, 'Request/new-user-add-request.html',
                  {'request_form': request_form, 'customer_form': customer_form})


# Kayıtlı müşteriyle Talep oluşturma
def registered_user_add_request(request):
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
            request1.request_situation.add(RequestSituations.objects.get(name='Onay Bekliyor'))
            request1.company = company[0]
            request1.save()

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
    requests = Request.objects.filter(isApprove=False).order_by('creationDate')

    request_situations = RequestSituations.objects.all()
    return render(request, 'Request/pending-requests.html',
                  {'requests': requests, 'request_situations': request_situations})


# talep tamamla
@login_required
def return_approved_requests(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    approved_requests = Request.objects.filter(isApprove=True).order_by('creationDate')
    request_situations = RequestSituations.objects.all()

    return render(request, 'Request/approved-request.html',
                  {'approved_requests': approved_requests, 'request_situations': request_situations})


# Talep Onayla
@login_required
def pendingRequestActive(request):
    if request.POST:
        try:

            user_id = request.POST.get('user_id')

            activeRequest(request, int(user_id))

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Request.DoesNotExist:

            return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


# Talep Sil
@login_required
def pending_request_delete(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Request.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Request.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
