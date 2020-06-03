import calendar
import datetime
from decimal import Decimal

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from unicodedata import decimal

from kurye.models import Settings, Neighborhood, EarningPayments
from kurye.models.Company import Company
from kurye.models.Courier import Courier
from kurye.models.EarningCompany import EarningCompany
from kurye.models.Request import Request
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.services import general_methods
from kurye.services.general_methods import return_month


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
    if request.method == 'POST':
        array_courier = []
        couriers = Courier.objects.all()
        month = int(request.POST['ay'])
        year = int(request.POST['yil'])
        date = request.POST['yil'] + '-' + request.POST['ay']
        num_days = calendar.monthrange(year, month)[1]

        datetime_start = datetime.datetime(int(request.POST['yil']), int(request.POST['ay']), 1, 0, 0)
        datetime_end = datetime.datetime(int(request.POST['yil']), int(request.POST['ay']), num_days, 23, 59)

        # if (datetime_current - datetime_start).days >= calendar.monthrange(year, month)[1]:
        # if EarningPayments.objects.filter(earning_date=date).count() < TaskSituationTask.objects.filter(task_situation__name='Teslim Edildi').filter(creationDate__range=(datetime_start, datetime_end)).count():

        array = []
        for courier in couriers:
            courier_tasks = TaskSituationTask.objects.filter(creationDate__year=year).filter(
                creationDate__month=month).filter(task_situation__name='Teslim Edildi').filter(
                task__courier_id=courier.pk)
            if courier_tasks.count() > 0:
                array.append(courier_tasks)
        for courier_task in array:
            courier_dict = dict()
            prim = ""

            if courier_task[0].task.courier.type == 'Motorlu':
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
            if EarningPayments.objects.filter(payed=True).filter(
                    courier=courier_task[0].task.courier.courier).count() > 0:
                courier_dict['situation'] = 'Ödendi'
            else:
                courier_dict['situation'] = 'Ödenmedi'
            array_courier.append(courier_dict)

        # earning = EarningPayments(courier=courier.courier, paymentTotal=prim, earning_date=date,task_count=courier_task.count())
        # earning.save()

        # earning_couriers = EarningPayments.objects.filter(earning_date=date)
    # else:
    # earning_couriers = EarningPayments.objects.filter(earning_date=date)

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

    return redirect('kurye:kurye-odemeleri')


def company_earning(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    array_company = []
    datetime_current = datetime.datetime.today()

    year = datetime_current.year
    month = datetime_current.month
    date = str(year) + '-' + str(month)

    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    today = str(year) + '-' + return_month(month)
    num_days = calendar.monthrange(year, month)[1]
    group = Group.objects.filter(name='Kullanıcı')
    earning_companies = ""

    if request.method == 'POST':

        date = request.POST['yil'] + '-' + request.POST['ay']
        datetime_start = datetime.datetime(int(request.POST['yil']), int(request.POST['ay']), 1, 0, 0)

        datetime_end = datetime.datetime(int(request.POST['yil']), int(request.POST['ay']), num_days, 23, 59)

        companies = TaskSituationTask.objects.filter(task_situation__name='Teslim Edildi').filter(
            creationDate__range=(datetime_start, datetime_end)).values(
            'task__request__company',
            'task__request__neighborhood').annotate(
            count=Count('task__request__neighborhood'))

        task_company = TaskSituationTask.objects.filter(task_situation__name='Teslim Edildi').filter(
            creationDate__range=(datetime_start, datetime_end)).values(
            'task__request__company').annotate(
            count=Count('task__request__company'))

        if (datetime_current - datetime_start).days >= calendar.monthrange(year, month)[1]:
            if EarningCompany.objects.filter(earning_date=date).count() != task_company.count():

                for x in companies:
                    company = Company.objects.get(pk=int(x['task__request__company']))
                    neighborhood = Neighborhood.objects.get(pk=int(x['task__request__neighborhood']))
                    payment_amount = neighborhood.price * int(x['count'])
                    if EarningCompany.objects.filter(company=company.profile).count() > 0:
                        earning_company = EarningCompany.objects.filter(company=company.profile)[0]
                        earning_company.paymentTotal = earning_company.paymentTotal + payment_amount
                        earning_company.task_count = earning_company.task_count + int(x['count'])
                        earning_company.save()
                    else:
                        earning = EarningCompany(company=company.profile, paymentTotal=payment_amount,
                                                 earning_date=date,
                                                 task_count=int(x['count']))
                        earning.save()
            earning_companies = EarningCompany.objects.filter(earning_date=date)
    else:
        earning_companies = EarningCompany.objects.filter(earning_date=date)

    return render(request, 'Earning/company_earning.html')


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
    if request.POST:
        date = request.POST['yil'] + '-' + request.POST['ay']
        year = request.POST['yil']
        month = request.POST['ay']
        companies = Company.objects.all()
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
        for company_task in company_task:
            company_task.task.request.isPayed = True
            company_task.task.request.payedDate = current_date.date()
            company_task.task.request.save()

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
