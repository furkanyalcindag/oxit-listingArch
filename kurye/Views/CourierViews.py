import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from kurye.models.Notification import Notification
from kurye.models.Profile import Profile
from kurye.models.Task import Task
from kurye.models.Courier import Courier
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.models.TaskSituations import TaskSituations
from kurye.serializers.CourierSerializer import CourierSerializer
from kurye.services import general_methods
from kurye.services.general_methods import save_log


# atanmış görevleri güncelleme
def assigned_task(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)
    tasks = Task.objects.filter(courier=courier)


    for task in tasks:
        task.activeTask = TaskSituationTask.objects.filter(task_id=task.pk).filter(isActive=True)[
                0].task_situation.name

    if request.method == 'POST':

        pk = request.POST['task']

        task = Task.objects.get(pk=int(pk))

        task.description = request.POST['description']
        task.save()

        active = TaskSituationTask.objects.filter(task_id=task.pk).filter(isActive=True)

        for active in active:
            active.isActive = False
            active.save()

        situation = TaskSituations.objects.get(name=request.POST['situation'])
        new_active = TaskSituationTask(task=task,
                                       task_situation=TaskSituations.objects.get(
                                           pk=situation.pk),
                                       isActive=True)
        new_active.save()

        if new_active.task_situation.name == 'Teslim Edildi' or new_active.task_situation.name == 'Teslim Edilemedi':
            task.deliveryDate = datetime.datetime.today().date()
            task.deliveryTime = datetime.datetime.today().time()
            task.save()
            courier.isActive = True
            courier.save()

        log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                      groups[0].name + ', ' + str(
            pk) + '</strong> nolu görevin durumunu <strong style="color:red"> ' + new_active.task_situation.name + '</strong> olarak  güncelledi</p>'

        save_log(profile.pk, log_content)

        subject, from_email, to = '' + task.request.company.companyName + ' Talep Durum Bilgisi', 'burcu.dogan@oxityazilim.com', user.email
        text_content = 'Talep Durumu'
        html_content = '<p><strong>Talep No: </strong>' + str(task.request.pk) + '</p>'
        html_content = html_content + '<p> <strong>Adres:</strong>' + task.request.receiver.address + '</p>'
        html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + task.request.receiver.customer + '</p>'
        html_content = html_content + '<p><strong>Talep Durumu: </strong>' + new_active.task_situation.name + '₺</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        subject, from_email, to = '' + task.request.company.companyName + ' Talep Durum Bilgisi', 'burcu.dogan@oxityazilim.com', task.request.company.profile.user.email
        text_content = 'Talep Durumu'
        html_content = '<p><strong>Talep No: </strong>' + str(task.request.pk) + '</p>'
        html_content = html_content + '<p> <strong>Adres:</strong>' + task.request.receiver.address + '</p>'
        html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + task.request.receiver.customer + '</p>'
        html_content = html_content + '<p><strong>Talep Durumu: </strong>' + new_active.task_situation.name + '₺</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        notification = Notification()
        notification.key = 'Kurye Gorev Durumu'
        notification.message = '' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' adlı kurye görev durumunu ' + new_active.task_situation.name + ' olarak güncellemiştir.'
        notification.save()
        messages.success(request, 'Görev Durumu Güncellendi.')
        return redirect("kurye:kurye atanan gorevler")

    task_situations = TaskSituations.objects.all()

    return render(request, 'Courier/courier-task-update.html',
                  {'tasks': tasks, 'task_situations': task_situations})


def courier_ending_tasks(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)

    ending_tasks = TaskSituationTask.objects.filter(task__courier=courier).filter(isActive=True).filter(
        Q(task_situation__name='Teslim Edildi') | Q(task_situation__name='Teslim Edilemedi'))

    return render(request, 'Courier/courier-ending-tasks.html', {'ending_tasks': ending_tasks})


def courier_tasks(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)

    tasks = TaskSituationTask.objects.filter(task__courier=courier).filter(isActive=True).exclude(
        task_situation__name='Teslim Edildi').exclude(task_situation__name='Teslim Edilemedi')

    return render(request, 'Courier/courier-tasks.html', {'tasks': tasks})


def courier_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    couriers = Courier.objects.all()
    return render(request, 'Courier/courier-list.html', {'couriers': couriers})


@api_view()
def getCourier(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    courier = Courier.objects.get(pk=pk)
    data = CourierSerializer(courier, many=True)

    responseData = {}
    responseData['courier'] = data.data
    responseData['courier'][0]
    return JsonResponse(responseData, safe=True)
