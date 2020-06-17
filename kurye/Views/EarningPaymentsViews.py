import calendar
import datetime
from decimal import Decimal
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from kurye.models.EarningPayments import EarningPayments
from kurye.models.Settings import Settings
from kurye.models.Company import Company
from kurye.models.Courier import Courier
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.services import general_methods


def courier_payment(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    date = str(year) + '-' + str(month)
    array_courier = []
    array = []
    couriers = Courier.objects.all()
    courier_dict = dict()
    if request.method == 'POST':
        array_courier = []

        month = int(request.POST['ay'])
        year = int(request.POST['yil'])
        date = request.POST['yil'] + '-' + request.POST['ay']
        num_days = calendar.monthrange(year, month)[1]

        for courier in couriers:

            courier_tasks = TaskSituationTask.objects.filter(creationDate__year=year).filter(
                creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
                task__courier_id=courier.pk)

            if courier_tasks.count() > 0:
                array.append(courier_tasks)
        for courier_task in array:

            prim = ""

            if courier_task[0].task.courier.type == 'Motorlu Kurye':
                motorlu_limit = int(Settings.objects.get(name='motorlu_kurye_limit').value)
                motorlu_prim = int(Settings.objects.get(name='motorlu_kurye_prim').value)
                if courier_task.count() >= motorlu_limit:
                    limit = courier_task.count() - motorlu_limit
                    prim = float(limit * motorlu_prim)
                    courier_dict['courier_type'] = courier_task[0].task.courier.type

            else:
                motorsuz_limit = int(Settings.objects.get(name='motorsuz_kurye_limit').value)
                motorsuz_prim = int(Settings.objects.get(name='motorsuz_kurye_prim').value)
                if courier_task.count() >= motorsuz_limit:
                    limit = courier_task.count() - motorsuz_limit
                    prim = float(limit * motorsuz_prim)
                    courier_dict['courier_type'] = courier_task[0].task.courier.type
            courier_dict['courier'] = courier_task[0].task.courier
            courier_dict['prim'] = prim
            courier_dict['count'] = courier_task.count()
            courier_dict['date'] = date
            if EarningPayments.objects.filter(payed=True).filter(creationDate__year=year).filter(
                    creationDate__month=month).filter(
                courier=courier_task[0].task.courier.courier).count() > 0:
                courier_dict['situation'] = 'Ödendi'
            else:
                courier_dict['situation'] = 'Ödenmedi'
            array_courier.append(courier_dict)

        return render(request, 'Earning/courier_payments.html',
                      {'tasks': array_courier, 'date': date, 'year': year, 'month': month})
    else:
        for courier in couriers:
            courier_tasks = TaskSituationTask.objects.filter(creationDate__year=year).filter(
                creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
                task__courier_id=courier.pk)
            if courier_tasks.count() > 0:
                array.append(courier_tasks)
        for courier_task in array:
            courier_dict = dict()
            prim = ""

            if courier_task[0].task.courier.type == 'Motorlu Kurye':
                motorlu_limit = int(Settings.objects.get(name='motorlu_kurye_limit').value)
                motorlu_prim = int(Settings.objects.get(name='motorlu_kurye_prim').value)
                if courier_task.count() >= motorlu_limit:
                    limit = courier_task.count() - motorlu_limit
                    prim = float(limit * motorlu_prim)
                    courier_dict['courier_type'] = courier_task[0].task.courier.type

            else:
                motorsuz_limit = int(Settings.objects.get(name='motorsuz_kurye_limit').value)
                motorsuz_prim = int(Settings.objects.get(name='motorsuz_kurye_prim').value)
                if courier_task.count() >= motorsuz_limit:
                    limit = courier_task.count() - motorsuz_limit
                    prim = float(limit * motorsuz_prim)
                    courier_dict['courier_type'] = courier_task[0].task.courier.type
            courier_dict['courier'] = courier_task[0].task.courier
            courier_dict['prim'] = prim
            courier_dict['count'] = courier_task.count()
            courier_dict['date'] = date
            if EarningPayments.objects.filter(creationDate__year=year).filter(
                    creationDate__month=month).filter(payed=True).filter(
                courier=courier_task[0].task.courier.courier).count() > 0:
                courier_dict['situation'] = 'Ödendi'
            else:
                courier_dict['situation'] = 'Ödenmedi'
            array_courier.append(courier_dict)

    return render(request, 'Earning/courier_payments.html',
                  {'tasks': array_courier, 'date': date, 'year': year, 'month': month})


# kurye primi ödendi yap
def pay_premium_courier(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        year = request.POST['year']
        month = request.POST['month']
        prim = request.POST['prim']
        date = request.POST['year'] + '-' + request.POST['month']

        date_current = datetime.datetime.today()
        task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
            task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
            task__courier_id=pk)
        earning_courier = EarningPayments(paymentTotal=Decimal(prim.replace(',', '.')),
                                          courier=task[0].task.courier.courier,
                                          payedDate=date_current.date(), payed=True, earning_date=date,
                                          task_count=task.count())
        earning_courier.save()

        notification = Notification()
        notification.key = 'Kurye Prim Ödeme'
        notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
        notification.message = '' + task[0].task.courier.courier.user.first_name + ' ' + task[
            0].task.courier.courier.user.last_name + ' adlı kuryeye ' + str(
            earning_courier.paymentTotal) + '₺ prim ödendi '
        notification.save()

    return redirect('kurye:kurye-odemeleri')


def company_earning_info(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    date = str(year) + '-' + str(month)
    array_earning = []
    companies = Company.objects.all()
    if request.POST:
        date = request.POST['yil'] + '-' + request.POST['ay']
        year = request.POST['yil']
        month = request.POST['ay']

        for company in companies:
            company_dict = dict()
            company_task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
                task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
                task__request__company_id=company.pk)
            earning = company_task.values(
                'task__request__company').annotate(
                sum=Sum('task__request__request_price'))
            if earning.count() > 0:
                if company_task[0].task.request.isPayed:
                    company_dict['situation'] = 'Ödendi'
                else:
                    company_dict['situation'] = 'Ödenmedi'
                company_dict['company'] = Company.objects.get(pk=int(earning[0]['task__request__company']))
                company_dict['sum'] = earning[0]['sum']
                company_dict['date'] = date
                company_dict['count'] = company_task.count()
                array_earning.append(company_dict)
                return render(request, 'Earning/company_earning.html',
                              {'earnings': array_earning, 'date': date, 'year': year, 'month': month})
    else:
        for company in companies:
            company_dict = dict()
            company_task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
                task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
                task__request__company_id=company.pk)
            earning = company_task.values(
                'task__request__company').annotate(
                sum=Sum('task__request__request_price'))
            if earning.count() > 0:
                if company_task[0].task.request.isPayed:
                    company_dict['situation'] = 'Ödendi'
                else:
                    company_dict['situation'] = 'Ödenmedi'
                company_dict['company'] = Company.objects.get(pk=int(earning[0]['task__request__company']))
                company_dict['sum'] = earning[0]['sum']
                company_dict['date'] = date
                company_dict['count'] = company_task.count()
                array_earning.append(company_dict)

    return render(request, 'Earning/company_earning.html',
                  {'earnings': array_earning, 'date': date, 'year': year, 'month': month})


# Kullanıcı-Odemelerim-Sayfası
def company_payments(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    date = str(year) + '-' + str(month)
    array_earning = []
    user = request.user
    profile = Profile.objects.get(user=user)

    company = Company.objects.get(profile=profile)
    company_dict = dict()
    if request.POST:
        date = request.POST['yil'] + '-' + request.POST['ay']
        year = request.POST['yil']
        month = request.POST['ay']

        company_task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
            task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
            task__request__company=company)
        earning = company_task.values(
            'task__request__company').annotate(
            sum=Sum('task__request__request_price'))
        if earning.count() > 0:
            if company_task[0].task.request.isPayed:
                company_dict['situation'] = 'Ödendi'
            else:
                company_dict['situation'] = 'Ödenmedi'
            company_dict['company'] = Company.objects.get(pk=int(earning[0]['task__request__company']))
            company_dict['sum'] = earning[0]['sum']
            company_dict['date'] = date
            company_dict['count'] = company_task.count()
            array_earning.append(company_dict)
            return render(request, 'Earning/company_earning.html',
                          {'earnings': array_earning, 'date': date, 'year': year, 'month': month})
    else:
        company_task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
            task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
            task__request__company=company)
        earning = company_task.values(
            'task__request__company').annotate(
            sum=Sum('task__request__request_price'))
        if earning.count() > 0:
            if company_task[0].task.request.isPayed:
                company_dict['situation'] = 'Ödendi'
            else:
                company_dict['situation'] = 'Ödenmedi'
            company_dict['company'] = Company.objects.get(pk=int(earning[0]['task__request__company']))
            company_dict['sum'] = earning[0]['sum']
            company_dict['date'] = date
            company_dict['count'] = company_task.count()
            array_earning.append(company_dict)
    return render(request, 'Earning/company_earning.html',
                  {'earnings': array_earning, 'date': date, 'year': year, 'month': month})


# kullanıcı ödendi yap
def pay_payment_company(request, pk, year, month):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        year = year
        month = month
        current_date = datetime.datetime.today()
        company_task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
            task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
            task__request__company_id=pk)
        for company_taskk in company_task:
            company_taskk.task.request.isPayed = True
            company_taskk.task.request.payedDate = current_date.date()
            company_taskk.task.request.save()

        notification = Notification()
        notification.key = 'Firma Ödeme'
        notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
        notification.message = '' + company_task[0].task.request.company.companyName + ' adlı firma ' + str(
            year) + '-' + str(month) + ' tarihli ödemesini yaptı '
        notification.save()

    return redirect('kurye:kullanici-odemeleri')


# kullanıcı ödenmedi yap
def undo_payment_company(request, pk, year, month):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        year = year
        month = month
        company_task = TaskSituationTask.objects.filter(task__request__creationDate__year=year).filter(
            task__request__creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
            task__request__company_id=pk)
        for task in company_task:
            task.task.request.isPayed = False
            task.task.request.payedDate = None
            task.task.request.save()

        notification = Notification()
        notification.key = 'Firma Prim Ödeme'
        notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
        notification.message = '' + company_task[
            0].task.request.company.companyName + ' adlı firmanın ödendi durumu ödenmedi olarak güncellendi '
        notification.save()

    return redirect('kurye:kullanici-odemeleri')


@login_required
def payment_company(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            company_id = request.POST.get('company_id')
            year = request.POST.get('year')
            month = request.POST.get('month')

            pay_payment_company(request, int(company_id), year, month)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@login_required
def payment_company_undo(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            company_id = request.POST.get('company_id')
            year = request.POST.get('year')
            month = request.POST.get('month')

            undo_payment_company(request, int(company_id), year, month)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})