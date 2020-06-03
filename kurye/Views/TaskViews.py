from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import resolve
from rest_framework.decorators import api_view
from kurye.models.Profile import Profile
from kurye.models.MenuAdmin import MenuAdmin
from kurye.models.Notification import Notification
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.models.TaskSituations import TaskSituations
from kurye.models.Courier import Courier
from kurye.models.Task import Task
from kurye.models.Request import Request
from kurye.serializers.TaskSerializer import TaskSerializer
from kurye.services import general_methods
from kurye.services.general_methods import make_cancel_task, save_log


# admin Talepler
def requests(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    courier = Courier.objects.get(pk=pk)
    request1 = Request.objects.filter(isApprove=True)
    task = []
    request_array = []
    for request2 in request1:
        tasks = TaskSituationTask.objects.filter(task__request=request2).filter(isActive=True)
        if tasks.count() == 0:
            request_array.append(request2)
    return render(request, 'Request/request.html', {'requests': request_array, 'courier': courier})


# görev atama kurye seçiliyor
def add_task(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    request1 = Request.objects.get(pk=pk)
    task = Task(request=request1)
    task.save()

    if request.method == 'POST':
        situation = TaskSituationTask(task=task, task_situation=TaskSituations.objects.get(name='Kurye Atandı'),
                                      isActive=True)
        situation.save()

        c_post = request.POST['courier']
        courier = Courier.objects.get(pk=c_post)

        task.courier = courier
        task.save()
        courier.isActive = 'False'
        courier.save()

        notification = Notification.objects.filter(message__icontains='Talep No: ' + str(request1.pk)).filter(
            key__icontains='Talep')
        for notification in notification:
            notification.delete()

        log_content = '<p><strong style="color:red"> ' + groups[
            0].name + ', ' + courier.courier.user.first_name + ' ' + courier.courier.user.last_name + '</strong>adlı Kuryeyi <strong style="color:red">  ' + str(
            task.pk) + ' </strong> nolu göreve atadı.</p>'

        save_log(profile.pk, log_content)

        subject, from_email, to = 'MotoKurye Görev Bilgileri', 'burcu.dogan@oxityazilim.com', courier.courier.user.email
        text_content = 'Görev Bilgileri'
        html_content = '<p> <strong>Adres:</strong>' + task.request.receiver.address + '</p>'
        html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + task.request.receiver.customer + '</p>'
        html_content = html_content + '<p><strong>Ödenecek Tutar: </strong>' + str(task.request.totalPrice) + '₺</p>'
        html_content = html_content + '<p>Detaylı görev bilgilerinine siteminizden ulaşabilirsiniz.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request,
                         'Görev ' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' a Atandı.')
        return redirect('kurye:kurye listesi')

    return render(request, 'Task/add-task.html', {'request': request1, })


# admin Tamamlanan Görevler
@login_required
def return_completed_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    tasks = Task.objects.filter(isComplete=True)
    url_name = request.resolver_match.url_name
    app_name = resolve(request.path).app_name
    url = app_name + ':' + url_name
    obj = MenuAdmin.objects.get(url=url)

    return render(request, 'Task/completed-tasks.html',
                  {'task': tasks})


# ADMİN İptal Edilen Görevler
@login_required
def return_canceled_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    tasks = TaskSituationTask.objects.filter(isActive=True).filter(task_situation__name='İptal Edildi')
    return render(request, 'Task/cancel-tasks.html',
                  {'tasks': tasks})


# Admin Biten Görevler
@login_required
def return_ending_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    tasks = Task.objects.filter(isComplete=True)
    url_name = request.resolver_match.url_name
    app_name = resolve(request.path).app_name
    url = app_name + ':' + url_name
    obj = MenuAdmin.objects.get(url=url)
    tasks = TaskSituationTask.objects.filter(isActive=True).filter(
        Q(task_situation__name='Teslim Edildi') | Q(task_situation__name='Teslim Edilemedi'))
    return render(request, 'Task/ending-task.html',
                  {'tasks': tasks})


# Admin Aktif Görevler
@login_required
def return_active_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    tasks = Task.objects.filter(isComplete=True)
    url_name = request.resolver_match.url_name
    app_name = resolve(request.path).app_name
    url = app_name + ':' + url_name
    obj = MenuAdmin.objects.get(url=url)
    tasks = TaskSituationTask.objects.filter(isActive=True).filter(
        Q(task_situation__name='Kurye Atandı') | Q(task_situation__name='Yolda'))
    return render(request, 'Task/active-task.html',
                  {'tasks': tasks})


# Kullanıcı Görev Tamamlama
@login_required
def taskComplete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    groups = Group.objects.filter(user=user)
    task = Task.objects.get(pk=pk)
    new_situation = TaskSituationTask(task=task, task_situation=TaskSituations.objects.get(name='Tamamlandı'),
                                      isActive=True)
    new_situation.save()

    task.isComplete = True
    task.save()
    log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                  groups[0].name + ', ' + str(task.pk) + '</strong> nolu görevi sonlandırdı.</p>'

    save_log(profile.pk, log_content)
    messages.success(request, 'Görev Tamamlandı')
    return redirect('kurye:kullanıcının biten talepleri')


@api_view()
def getTask(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    task = TaskSituationTask.objects.filter(task_id=pk).filter(isActive=True)
    data = TaskSerializer(task, many=True)

    responseData = {}
    responseData['task'] = data.data
    responseData['task'][0]
    return JsonResponse(responseData, safe=True)


def assign_courier(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    couriers = Courier.objects.all().order_by('modificationDate')
    return render(request, 'Task/assign-courier.html', {'couriers': couriers})


def other_assign_courier_task(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    task = Task.objects.get(pk=pk)
    couriers = Courier.objects.all()

    if request.method == 'POST':

        id = request.POST['courier']

        courier = Courier.objects.get(pk=id)

        active_task = TaskSituationTask.objects.filter(task_id=task.pk).filter(isActive=True)

        for active in active_task:
            active.isActive = False
            active.task.courier.isActive = False
            active.save()

        task.courier = courier
        task.save()

        new_task = TaskSituationTask()
        new_task.task = task
        new_task.task_situation = TaskSituations.objects.get(name='Kurye Atandı')
        new_task.isActive = True
        new_task.save()

        courier.isActive = False
        courier.save()

        log_content = '<p>Yeniden Görevlendirme: <strong style="color:red"> ' + groups[
            0].name + ', ' + courier.courier.user.first_name + courier.courier.user.last_name + '</strong>adlı Kuryeyi <strong style="color:red">  ' + str(
            task.pk) + ' </strong> nolu göreve atadı.</p>'

        save_log(profile.pk, log_content)

        notification = Notification()
        notification.key = 'Yeniden Görevlendirme'
        notification.message = '' + task.pk + ' nolu göreve yeni kurye atandı.Kurye : ' + courier.courier.user.first_name + ' ' + courier.courier.user.last_name + ''
        notification.save()

        subject, from_email, to = 'MotoKurye Görev Bilgileri', 'burcu.dogan@oxityazilim.com', courier.courier.user.email
        text_content = 'Görev Bilgileri'
        html_content = '<p> <strong>Adres:</strong>' + task.request.receiver.address + '</p>'
        html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + task.request.receiver.customer + '</p>'
        html_content = html_content + '<p><strong>Ödenecek Tutar: </strong>' + str(task.request.totalPrice) + '₺</p>'
        html_content = html_content + '<p>Detaylı görev bilgilerinine siteminizden ulaşabilirsiniz.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request,
                         'Görev ' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' a Atandı.')

    return render(request, 'Task/task_other_assign_courier.html', {'couriers': couriers, 'task': task})
