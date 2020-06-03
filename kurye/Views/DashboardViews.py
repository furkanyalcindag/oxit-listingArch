import calendar
import datetime

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from kurye.models import Settings, EarningPayments
from kurye.models.Company import Company
from kurye.models.Courier import Courier
from kurye.models.Customer import Customer
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.Request import Request
from kurye.models.Task import Task
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.serializers.NotificationSerializer import NotificationSerializer
from kurye.services import general_methods


# Admin İşlemleri
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    today = datetime.date.today().year
    start_date = Settings.objects.get(name='start_report_year')
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    num_days = calendar.monthrange(year, month)[1]

    start = datetime.datetime.now() - datetime.timedelta(days=num_days)

    # Ay-Yıl Kurye Prim Tablosu
    dif_year = int(today) - int(start_date.value)
    array_earning_courier = []
    total = 0
    for x in range(dif_year + 1):

        report_earning_courier = EarningPayments.objects.values('earning_date', 'creationDate__month').annotate(
            sum=Sum('paymentTotal'))

        for y in report_earning_courier:
            report_year = dict()
            report_year['total'] = int(y['sum'])
            report_year['date'] = y['earning_date'].split('-')[1]
            report_year['year'] = y['earning_date'].split('-')[0]
            array_earning_courier.append(report_year)

    array_report_year = []
    for x in range(dif_year + 1):

        report_year_request = Request.objects.values('creationDate__year', 'creationDate__month').order_by(
            'creationDate__month').annotate(count=Count('creationDate__year'))

        for x in report_year_request:
            report_year = dict()
            report_year['count'] = x['count']
            report_year['date'] = x['creationDate__month']
            report_year['year'] = x['creationDate__year']
            array_report_year.append(report_year)

    start_delta = datetime.datetime.now() - datetime.timedelta(days=7)

    report_week_request = Request.objects.filter(creationDate__lte=datetime.datetime.now(),
                                                 creationDate__gte=start_delta).values('creationDate__year',
                                                                                       'creationDate__month',
                                                                                       'creationDate__day', ).order_by(
        'creationDate__day').annotate(count=Count('creationDate__day'))

    array_report_week = []
    for x in report_week_request:
        report_week = dict()
        report_week['year'] = x['creationDate__year']
        report_week['month'] = x['creationDate__month']
        report_week['day'] = x['creationDate__day']
        report_week['count'] = x['count']
        array_report_week.append(report_week)

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)

    couriers = Profile.objects.filter(user__is_active=True).filter(user__groups__name='Kurye').order_by('creationDate')[
               :6]

    # active_courier = Courier.objects.values('isActive').annotate(count=Count('isActive'))

    active_courier = TaskSituationTask.objects.values('task__courier').annotate(count=Count('task__courier')).filter(
        task_situation__name='Teslim Edildi').order_by('-count')[:6]

    courierss = []
    for courier in active_courier:
        courier_dict = dict()
        courier_dict['courier'] = Courier.objects.get(pk=int(courier['task__courier']))
        courier_dict['count'] = courier['count']
        courierss.append(courier_dict)

    completed_task = Task.objects.filter(isComplete=True)
    active_task = TaskSituationTask.objects.filter(
        Q(task_situation__name='Kurye Atandı') | Q(task_situation__name='Yolda')).filter(isActive=True)

    canceled_task = TaskSituationTask.objects.filter(task_situation__name='İptal Edildi').filter(isActive=True)

    delivered_task = TaskSituationTask.objects.filter(task_situation__name='Teslim Edildi').count()
    assigned_task = TaskSituationTask.objects.filter(task_situation__name='Kurye Atandı').count()
    on_the_road_task = TaskSituationTask.objects.filter(task_situation__name='Yolda').count()

    undeliverable_task = TaskSituationTask.objects.filter(task_situation__name='Teslim Edilemedi').count()

    unending_task = Task.objects.filter(isComplete=False)

    d = datetime.datetime.today() - datetime.timedelta(hours=0, minutes=10)
    online = User.objects.filter(last_login__gt=d).count()

    all_user = Company.objects.all().filter(profile__isActive=True).count()

    all_tasks = TaskSituationTask.objects.all().filter(isActive=True).order_by('modificationDate')[:6]

    array_report_courierCount = []
    array_report_companyCount = []

    for x in range(dif_year + 1):

        report_count_courier = Courier.objects.values('creationDate__year', 'creationDate__month').order_by(
            'creationDate__month').annotate(count=Count('creationDate__month'))
        report_count_company = Company.objects.values('creationDate__year', 'creationDate__month').order_by(
            'creationDate__month').annotate(count=Count('creationDate__month'))

        for x in report_count_company:
            report_year = dict()
            report_year['count'] = x['count']
            report_year['date'] = x['creationDate__month']
            report_year['year'] = x['creationDate__year']
            array_report_companyCount.append(report_year)

        for x in report_count_courier:
            report_year = dict()
            report_year['count'] = x['count']
            report_year['date'] = x['creationDate__month']
            report_year['year'] = x['creationDate__year']
            array_report_courierCount.append(report_year)


    return render(request, 'dashboard/admin-dashboard.html',
                  {'couriers': couriers, 'completed_task': completed_task.count(),
                   'active_task': active_task.count(),
                   'unending_task': unending_task, 'canceled_task': canceled_task.count(), 'online': online,
                   'all_user': all_user, 'all_tasks': all_tasks, 'delivered_task': delivered_task,
                   'undeliverable_task': undeliverable_task, 'on_the_road_task': on_the_road_task,
                   'assigned_task': assigned_task, 'active_courier': active_courier, 'courierss': courierss,
                   'array_report_year': array_report_year, 'array_report_week': array_report_week,
                   'array_earning_couriers': array_earning_courier, 'array_courierCount': array_report_courierCount,
                   'array_companyCount': array_report_companyCount})


# Kullanıcı İşlemleri
def return_company_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    company = Company.objects.get(profile=profile)
    arrayCustomers = []

    today = datetime.date.today().year
    start_date = Settings.objects.get(name='start_report_year')

    dif_year = int(today) - int(start_date.value)
    array_report_year = []
    array_report_company = []
    for x in range(dif_year + 1):

        report_year_request = Request.objects.filter(company__profile=profile).values('creationDate__year',
                                                                                      'creationDate__month').order_by(
            'creationDate__month').annotate(count=Count('creationDate__year'))

        report_company_earning = TaskSituationTask.objects.filter(task_situation__name='Teslim Edildi').filter(
            task__request__company_id=company.pk).values('task__request__company',
                                                         'task__request__creationDate__month',
                                                         'task__request__creationDate__year').annotate(
            sum=Sum('task__request__request_price'))

        for x in report_year_request:
            report_year = dict()
            report_year['count'] = x['count']
            report_year['date'] = x['creationDate__month']
            report_year['year'] = x['creationDate__year']
            array_report_year.append(report_year)

        for x in report_company_earning:
            report_year = dict()
            report_year['sum'] = int(x['sum'])
            report_year['date'] = x['task__request__creationDate__month']
            report_year['year'] = x['task__request__creationDate__year']
            array_report_company.append(report_year)

    start_delta = datetime.datetime.now() - datetime.timedelta(days=7)

    report_week_request = Request.objects.filter(company__profile=profile).filter(
        creationDate__lte=datetime.datetime.now(),
        creationDate__gte=start_delta).values('creationDate__year',
                                              'creationDate__month',
                                              'creationDate__day', ).order_by(
        'creationDate__day').annotate(count=Count('creationDate__day'))

    array_report_week = []
    for x in report_week_request:
        report_week = dict()
        report_week['year'] = x['creationDate__year']
        report_week['month'] = x['creationDate__month']
        report_week['day'] = x['creationDate__day']
        report_week['count'] = x['count']
        array_report_week.append(report_week)

    active_customers = Request.objects.values('receiver__customer').annotate(
        count=Count('receiver__customer')).order_by('-count')[:5]
    for customer in active_customers:
        customerDict = dict()
        customerDict['customer'] = Customer.objects.get(customer=customer['receiver__customer'])
        customerDict['count'] = customer['count']
        arrayCustomers.append(customerDict)

    requests = Request.objects.filter(company=company)
    requests_count = Request.objects.filter(company=company).count()
    task = []
    canceled_task = []
    completed_task = []
    successful_task = []
    unsuccessful_task = []
    active_task = []
    for request1 in requests:
        if TaskSituationTask.objects.filter(task__request_id=request1.pk).count() > 0:
            task = TaskSituationTask.objects.filter(task__request=requests[0]).filter(isActive=True).order_by(
                'creationDate')[
                   :10]
            canceled_task = TaskSituationTask.objects.filter(task__request=requests[0]).filter(isActive=True).filter(
                task_situation__name='İptal Edildi').count()
            completed_task = TaskSituationTask.objects.filter(task__request=requests[0]).filter(isActive=True).filter(
                task_situation__name='Tamamlandı').count()
            unsuccessful_task = TaskSituationTask.objects.filter(task__request=requests[0]).filter(
                isActive=True).filter(
                task_situation__name='Teslim Edilemedi').count()
            successful_task = TaskSituationTask.objects.filter(task__request=requests[0]).filter(isActive=True).filter(
                task_situation__name='Teslim Edildi').count()
            active_task = TaskSituationTask.objects.filter(task__request=requests[0]).filter(isActive=True).filter(
                Q(task_situation__name='Kurye Atandı') | Q(task_situation__name=' Kurye Yolda')).count()

    return render(request, 'dashboard/user-dashboard.html',
                  {'tasks': task, 'canceled_tasks': canceled_task, 'completed_tasks': completed_task,
                   'unsuccessful_tasks': unsuccessful_task, 'requests': requests_count,
                   'active_customers': arrayCustomers, 'array_report_week': array_report_week,
                   'array_report_year': array_report_year, 'successful_tasks': successful_task,
                   'active_requests': active_task, 'array_report_company': array_report_company
                   })


# Kurye İşlemleri
def return_courier_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    user = request.user
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)
    today = datetime.date.today().year
    start_date = Settings.objects.get(name='start_report_year')

    dif_year = int(today) - int(start_date.value)
    array_report_year = []
    for x in range(dif_year + 1):

        report_year_request = TaskSituationTask.objects.filter(task__courier=courier).values('creationDate__year',
                                                                                             'creationDate__month').order_by(
            'creationDate__month').annotate(count=Count('creationDate__year'))

        for x in report_year_request:
            report_year = dict()
            report_year['count'] = x['count']
            report_year['date'] = x['creationDate__month']
            report_year['year'] = x['creationDate__year']
            array_report_year.append(report_year)

    start_delta = datetime.datetime.now() - datetime.timedelta(days=7)

    report_week_request = TaskSituationTask.objects.filter(task__courier=courier).filter(
        creationDate__lte=datetime.datetime.now(),
        creationDate__gte=start_delta).values('creationDate__year',
                                              'creationDate__month',
                                              'creationDate__day', ).order_by(
        'creationDate__day').annotate(count=Count('creationDate__day'))

    array_report_week = []
    for x in report_week_request:
        report_week = dict()
        report_week['year'] = x['creationDate__year']
        report_week['month'] = x['creationDate__month']
        report_week['day'] = x['creationDate__day']
        report_week['count'] = x['count']
        array_report_week.append(report_week)

    task = TaskSituationTask.objects.filter(task__courier_id=courier.pk).filter(isActive=True).order_by('creationDate')[
           :10]
    canceled_task = TaskSituationTask.objects.filter(task__courier_id=courier.pk).filter(isActive=True).filter(
        task_situation__name='İptal Edildi').count()
    completed_task = TaskSituationTask.objects.filter(task__courier_id=courier.pk).filter(isActive=True).filter(
        task_situation__name='Tamamlandı').count()
    unsuccessful_task = TaskSituationTask.objects.filter(task__courier_id=courier.pk).filter(isActive=True).filter(
        task_situation__name='Teslim Edilemedi').count()
    successful_task = TaskSituationTask.objects.filter(task__courier_id=courier.pk).filter(isActive=True).filter(
        task_situation__name='Teslim Edildi').count()
    active_task = TaskSituationTask.objects.filter(task__courier_id=courier.pk).filter(isActive=True).filter(
        Q(task_situation__name='Kurye Atandı') | Q(task_situation__name=' Kurye Yolda')).count()

    return render(request, 'dashboard/courier-dashboard.html',
                  {'tasks': task, 'canceled_tasks': canceled_task, 'completed_tasks': completed_task,
                   'unsuccessful_tasks': unsuccessful_task,
                   'array_report_week': array_report_week,
                   'array_report_year': array_report_year, 'successful_tasks': successful_task,
                   'active_requests': active_task, })


def admin_notification(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    notification = Notification.objects.all()
    count = Notification.objects.all().count()

    if request.method == 'POST':

        check_list = request.POST['checks'].split(',')

        for check in check_list:
            notification = Notification.objects.get(pk=int(check))
            notification.delete()
        messages.success(request, 'Bildirimler Silindi')

        return redirect('kurye:bildirimler')
    return render(request, 'notifications.html', {'notifications': notification, 'count': count})


# bildirim datatable
def notifications(request):
    return render(request, 'notifications.html')


@login_required
def read_notification(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            notification_id = request.POST.get('notification_id')
            notification = Notification.objects.get(pk=notification_id)
            notification.isRead = True
            notification.save()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
