import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.shortcuts import render, redirect
from kurye.models.Company import Company
from kurye.models.Customer import Customer
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.Request import Request
from kurye.models.Task import Task
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.services import general_methods


# Admin İşlemleri
def return_admin_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    couriers = Profile.objects.filter(user__is_active=True).filter(user__groups__name='Kurye').order_by('creationDate')[
               :6]
    completed_task = Task.objects.filter(isComplete=True)
    assigned_task = TaskSituationTask.objects.filter(
        Q(task_situation__name='Kurye Atandı') | Q(task_situation__name='Yolda')).filter(isActive=True)

    canceled_task = TaskSituationTask.objects.filter(task_situation__name='İptal Edildi').filter(isActive=True)

    unending_task = Task.objects.filter(isComplete=False)

    d = datetime.datetime.today() - datetime.timedelta(hours=0, minutes=10)
    online = User.objects.filter(last_login__gt=d).count()

    all_user = Company.objects.all().filter(profile__isActive=True).count()

    all_tasks = TaskSituationTask.objects.all().filter(isActive=True).order_by('modificationDate')[:10]
    return render(request, 'dashboard/admin-dashboard.html',
                  {'couriers': couriers, 'completed_task': completed_task.count(),
                   'assigned_task': assigned_task.count(),
                   'unending_task': unending_task, 'canceled_task': canceled_task.count(), 'online': online,
                   'all_user': all_user, 'all_tasks': all_tasks})


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

    active_customers = Request.objects.values('receiver__customer').annotate(
        count=Count('receiver__customer')).order_by('-count')[:5]
    for customer in active_customers:
        customerDict = dict()
        customerDict['customer'] = Customer.objects.get(customer=customer['receiver__customer'])
        customerDict['count'] = customer['count']
        arrayCustomers.append(customerDict)

    requests = Request.objects.filter(company=company)
    tasks = []
    canceled_tasks = []
    completed_tasks = []
    unsuccessful_tasks = []

    for request1 in requests:
        task = TaskSituationTask.objects.filter(task__request=request1).filter(isActive=True).order_by('creationDate')[
               :10]
        canceled_task = TaskSituationTask.objects.filter(task__request=request1).filter(isActive=True).filter(
            task_situation__name='İptal Edildi')
        completed_task = TaskSituationTask.objects.filter(task__request=request1).filter(isActive=True).filter(
            task_situation__name='Tamamlandı')
        unsuccessful_task = TaskSituationTask.objects.filter(task__request=request1).filter(isActive=True).filter(
            task_situation__name='Teslim Edilemedi')
        if task.count() > 0:
            tasks.append(task)
        if canceled_task.count() > 0:
            canceled_tasks.append(canceled_task)
        if completed_task.count() > 0:
            completed_tasks.append(completed_task)
        if unsuccessful_task.count() > 0:
            unsuccessful_tasks.append(unsuccessful_task)

    return render(request, 'dashboard/user-dashboard.html',
                  {'tasks': tasks, 'canceled_tasks': canceled_tasks, 'completed_tasks': completed_tasks,
                   'unsuccessful_tasks': unsuccessful_tasks, 'requests': requests, 'active_customers': arrayCustomers,
                   })


# Kurye İşlemleri
def return_courier_dashboard(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'dashboard/courier-dashboard.html')


def notification(request):
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
