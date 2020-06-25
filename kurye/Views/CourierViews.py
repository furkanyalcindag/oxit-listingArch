import calendar
import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from kurye.Forms.SettingCourierPrimForm import SettingCourierPrimForm
from kurye.models import Settings
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
    task_situations = TaskSituations.objects.all()
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)
    tasks = TaskSituationTask.objects.filter(
        Q(task_situation__name='Paket Alımı İçin Yolda') | Q(task_situation__name='Paket Teslimi İçin Yolda') | Q(
            task_situation__name='Kurye Atandı')).filter(task__courier=courier).filter(isActive=True)

    return render(request, 'Courier/courier-task-update.html',
                  {'tasks': tasks, 'task_situations': task_situations, 'courier': courier.pk})


def updateTask(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    groups = Group.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)
    if request.POST:
        try:

            situation = TaskSituations.objects.get(name=request.POST['situation'])
            uuid = request.POST['task']
            task = Task.objects.get(uuid=uuid)
            active = TaskSituationTask.objects.filter(task_id=task.pk).filter(task__courier=courier).filter(
                isActive=True)
            if situation.name != active[0].task_situation.name:

                if request.POST['description']:

                    task.description = request.POST['description']
                else:
                    task.description = "Açıklama Yapılmadı"

                task.save()

                for active in active:
                    active.isActive = False
                    active.save()

                new_active = TaskSituationTask(task=task,
                                               task_situation=TaskSituations.objects.get(
                                                   pk=situation.pk),
                                               isActive=True)
                new_active.save()

                if new_active.task_situation.name == 'Teslim Edildi' or new_active.task_situation.name == 'Teslim Edilemedi':
                    task.deliveryDate = datetime.datetime.today().date()
                    task.deliveryTime = datetime.datetime.today().time()
                    if TaskSituationTask.objects.filter(Q(task_situation__name='Kurye Atandı') | Q(
                                task_situation__name='Paket Alımı İçin Yolda') | Q(
                                task_situation__name='Paket Teslimi İçin Yolda')).filter(isActive=True).filter(task__courier=courier).count() <= 0:
                        task.courier.isActive = True
                    task.courier.save()
                    task.isComplete = True
                    task.save()

                if TaskSituationTask.objects.filter(task__courier=courier).filter(
                        isActive=True).filter(
                    Q(task_situation__name='Kurye Atandı') | Q(task_situation__name='Paket Teslimi İçin Yolda') | Q(
                        task_situation__name='Paket Alımı İçin Yolda')).count() < 0:
                    courier.isActive = True
                    courier.save()

                log_content = '<p><strong style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</strong> adlı <strong style="color:red">' + \
                              groups[0].name + ', ' + str(
                    task.pk) + '</strong> nolu görevin durumunu <strong style="color:red"> ' + new_active.task_situation.name + '</strong> olarak  güncelledi</p>'

                save_log(profile.pk, log_content)

                subject, from_email, to = '' + task.request.company.companyName + ' Talep Durum Bilgisi', 'burcu.dogan@oxityazilim.com', user.email
                text_content = 'Talep Durumu'
                html_content = '<p><strong>Talep No: </strong>' + str(task.request.pk) + '</p>'
                html_content = html_content + '<p> <strong>Adres:</strong>' + task.request.receiver.address + '</p>'
                html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + task.request.receiver.customer + '</p>'
                html_content = html_content + '<p><strong>Talep Durumu: </strong>' + new_active.task_situation.name + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                subject, from_email, to = '' + task.request.company.companyName + ' Talep Durum Bilgisi', 'burcu.dogan@oxityazilim.com', task.request.company.profile.user.email
                text_content = 'Talep Durumu'
                html_content = '<p><strong>Talep No: </strong>' + str(task.request.pk) + '</p>'
                html_content = html_content + '<p> <strong>Adres:</strong>' + task.request.receiver.address + '</p>'
                html_content = html_content + '<p><strong>Müşteri Adı Soyadı: </strong>' + task.request.receiver.customer + '</p>'
                html_content = html_content + '<p><strong>Talep Durumu: </strong>' + new_active.task_situation.name + '</p>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                notification = Notification()
                notification.key = 'Kurye Gorev Durumu Güncelleme'
                notification.profile = Profile.objects.get(user=User.objects.filter(groups__name='Admin')[0])
                notification.message = '' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' adlı kurye görev durumunu ' + new_active.task_situation.name + ' olarak güncellemiştir.'
                notification.save()

                notification = Notification()
                notification.key = 'Kurye Gorev Durumu Güncelleme'
                notification.profile = task.request.company.profile
                notification.message = '' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' adlı kurye görev durumunu ' + new_active.task_situation.name + ' olarak güncellemiştir.'
                notification.save()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def courier_ending_tasks(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)

    ending_tasks = TaskSituationTask.objects.filter(task__courier=courier).filter(isActive=True).filter(
        Q(task_situation__name='Teslim Edildi') | Q(task_situation__name='Teslim Edilemedi') | Q(
            task_situation__name='Tamamlandı') | Q(task_situation__name='İptal Edildi'))

    return render(request, 'Courier/courier-ending-tasks.html', {'ending_tasks': ending_tasks})


def courier_tasks(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)

    tasks = TaskSituationTask.objects.filter(task__courier=courier).filter(isActive=True).filter(
        Q(task_situation__name='Kurye Atandı') | Q(task_situation__name='Paket Alımı İçin Yolda') | Q(
            task_situation__name='Paket Teslimi İçin Yolda'))

    return render(request, 'Courier/courier-tasks.html', {'tasks': tasks})


def courier_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    couriers = Courier.objects.filter(courier__isActive=True)
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


def update_courier_prim_limit(request, pk):
    setting = Settings.objects.get(pk=pk)
    form = SettingCourierPrimForm(request.POST or None, instance=setting)
    today = datetime.date.today()

    x = datetime.datetime(int(today.year), int(today.month), 1)
    days_in_month = calendar.monthrange(x.year, x.month)[1]
    start_date = x + datetime.timedelta(days=days_in_month)

    if request.method == 'POST':
        if start_date - x == days_in_month:
            if form.is_valid():
                form.save()
                messages.success(request, 'Değerler Güncellendi.')

                return redirect('kurye:prim-limit-listesi')
        else:
            messages.warning(request, 'Güncellemelerinizi Her ayın Başında Yapabilirsiniz.')
    return render(request, 'Courier/courier-limit-prim.html', {'form': form})


def prim_limit_list(request):
    settings = Settings.objects.filter(
        Q(name='motorlu_kurye_prim') | Q(name='motorsuz_kurye_prim') | Q(name='motorlu_kurye_limit') | Q(
            name='motorsuz_kurye_limit'))
    return render(request, 'Courier/prim-limit-list.html', {'settings': settings})


def delete_notification(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    profile = Profile.objects.get(user=request.user)
    if request.POST:
        try:

            check_list = request.POST['checks'].split(',')

            for check in check_list:
                notification = Notification.objects.get(pk=int(check))
                notification.delete()

            log_content = '<p><b style="color:red">' + profile.user.first_name + ' ' + profile.user.last_name + '</b>  ID : <strong style="color:red">' + str(
                check_list) + ' </strong> bildirimleri sildi.</p>'

            save_log(profile.pk, log_content)

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view()
def getCourier(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    couriers = Courier.objects.filter(courier__isActive=True)
    data = CourierSerializer(couriers, many=True)

    responseData = {}
    responseData['request'] = data.data
    responseData['request'][0]
    return JsonResponse(responseData, safe=True)
