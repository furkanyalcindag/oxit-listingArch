from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from kurye.models.Profile import Profile
from kurye.models.Notification import Notification
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.models.TaskSituations import TaskSituations
from kurye.models.Courier import Courier
from kurye.models.Task import Task
from kurye.models.Request import Request
from kurye.serializers.TaskSerializer import TaskSerializer
from kurye.services import general_methods
from kurye.services.general_methods import save_log


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
        courier.isActive = False
        courier.save()

        notification = Notification.objects.filter(message__icontains='Talep No: ' + str(request1.pk)).filter(
            key__icontains='Talep')
        for notification in notification:
            notification.delete()

        log_content = '<p><strong style="color:red"> ' + groups[
            0].name + ', ' + courier.courier.user.first_name + ' ' + courier.courier.user.last_name + '</strong>adlı Kuryeyi <strong style="color:red">  ' + str(
            task.pk) + ' </strong> nolu göreve atadı.</p>'

        save_log(profile.pk, log_content)

        notification2 = Notification()
        notification2.profile = courier.courier
        notification2.key = 'Kurye Görevlendirme'
        notification2.message = 'Yeni Görev ID: ' + str(task.pk) + ''
        notification2.save()

        notification3 = Notification()
        notification3.profile = task.request.company.profile
        notification3.key = 'Kurye Görevlendirme'
        notification3.message = '' + str(
            task.request.pk) + ' nolu talebiniz için ' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' adlı kurye görevlendirildi.'
        notification3.save()

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


# admin Bütün Görevler
@login_required
def return_completed_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    return render(request, 'Task/completed-tasks.html')


# ADMİN İptal Edilen Görevler
@login_required
def return_canceled_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    # tasks = TaskSituationTask.objects.filter(isActive=True).filter(task_situation__name='İptal Edildi')
    return render(request, 'Task/cancel-tasks.html', )


# Admin Biten Görevler
@login_required
def return_ending_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

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

    tasks = TaskSituationTask.objects.filter(isActive=True).filter(
        Q(task_situation__name='Kurye Atandı') | Q(task_situation__name='Paket Alımı İçin Yolda') | Q(
            task_situation__name='Paket Teslimi İçin Yolda'))
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

    current_taskSituation = TaskSituationTask.objects.filter(task=task).filter(isActive=True)
    for taskk in current_taskSituation:
        taskk.isActive = False
        taskk.task.isComplete = True
        taskk.task.save()
        taskk.save()

    new_situation = TaskSituationTask()
    new_situation.task = task
    new_situation.task_situation = TaskSituations.objects.get(name='Tamamlandı')
    new_situation.isActive = True
    new_situation.save()

    notification = Notification()
    notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
    notification.key = 'Görev Tamamlama'
    notification.message = '' + str(
        task.request.pk) + 'nolu talebi ' + user.first_name + ' ' + user.last_name + ' tamamladı.'
    notification.save()

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


# Yeniden Kurye
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

        active_courier = task.courier

        active_courier.isActive = True
        active_courier.save()

        active_task = TaskSituationTask.objects.filter(task_id=task.pk).filter(isActive=True)

        for active in active_task:
            active.isActive = False
            active.save()

        cancel_task = TaskSituationTask()
        cancel_task.task = task
        cancel_task.task.courier = active_courier
        cancel_task.task_situation = TaskSituations.objects.get(name='İptal Edildi')
        cancel_task.isActive = False
        cancel_task.save()

        courier.isActive = False
        courier.save()

        task.courier = courier
        task.save()

        new_task = TaskSituationTask()
        new_task.task = task
        new_task.task_situation = TaskSituations.objects.get(name='Kurye Atandı')
        new_task.isActive = True
        new_task.save()

        log_content = '<p>Yeniden Görevlendirme : <strong style="color:red"> ' + groups[
            0].name + ', ' + courier.courier.user.first_name + courier.courier.user.last_name + '</strong> adlı Kuryeyi <strong style="color:red">  ' + str(
            task.pk) + ' </strong> nolu göreve atadı.</p>'

        save_log(profile.pk, log_content)

        notification = Notification()
        notification.profile = profile
        notification.key = 'Yeniden Görevlendirme'
        notification.message = '' + str(
            task.pk) + ' nolu göreve yeni kurye atandı.Kurye : ' + courier.courier.user.first_name + ' ' + courier.courier.user.last_name + ''
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
