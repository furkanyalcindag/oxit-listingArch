from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group, User, Permission
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.urls import resolve

from kurye.models.Log import Log
from kurye.models.Profile import Profile
from kurye.models.Notification import Notification
from kurye.models.RequestSituationRequest import RequestSituationRequest
from kurye.models.Task import Task
from kurye.models.MenuCompany import MenuUser
from kurye.models.MenuAdmin import MenuAdmin
from kurye.models.MenuCourier import MenuCourier
from kurye.models.Request import Request
from kurye.models.RequestSituations import RequestSituations
from kurye.models.TaskSituationTask import TaskSituationTask
from kurye.models.TaskSituations import TaskSituations


def activeMenu(request):
    url_name = request.resolver_match.url_name
    app_name = resolve(request.path).app_name
    url = app_name + ':' + url_name
    obj = None
    parent = None

    obj = None
    parent = None
    if app_name != 'accounts':
        user = request.user
        groups = Group.objects.filter(user=user)
        if groups[0].name == "Admin":
            obj = MenuAdmin.objects.filter(url=url)
            if obj.count() > 0 and obj[0].parent:
                parent = MenuAdmin.objects.get(pk=obj[0].parent_id)
        elif groups[0].name == "Kullanıcı":
            obj = MenuUser.objects.filter(url=url)
            if obj.count() > 0 and obj[0].parent:
                parent = MenuUser.objects.get(pk=obj[0].parent_id)
        elif groups[0].name == "Kurye":
            obj = MenuCourier.objects.filter(url=url)
            if obj.count() > 0 and obj[0].parent:
                parent = MenuCourier.objects.get(pk=obj[0].parent_id)
        else:
            obj = None

        if obj.count() == 0:
            obj = []
            x = MenuCourier(url="")
            obj.append(x)

        return {"url": url, 'self': obj[0].parent, 'parent': parent, 'obj': obj[0]}

    return {"url": url, 'self': obj, 'parent': parent, 'obj': obj}


def getUserMenu(request):
    usermenus = MenuUser.objects.all().order_by('order')

    return {'usermenus': usermenus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all().order_by('order')
    return {'adminmenus': adminmenus}


def getCourierMenu(request):
    couriermenus = MenuCourier.objects.all().order_by('order')
    return {'couriermenus': couriermenus}


# Talep Onayla
def activeRequest(request, pk):
    request1 = Request.objects.get(pk=pk)
    situation = RequestSituationRequest(request_situation=RequestSituations.objects.get(name="Onaylandı"),
                                        isActive=True)
    situation.save()
    request1.request_situation = situation
    request1.isApprove = True
    request1.save()
    return request1


def control_access(request):
    group = request.user.groups.all()[0]

    permissions = group.permissions.all()

    is_exist = False

    for perm in permissions:

        if request.resolver_match.url_name == perm.name:
            is_exist = True

    if group.name == "Admin":
        is_exist = True

    return is_exist


def show_urls(urllist, depth=0):
    urls = []

    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)
        perm = Permission(name=entry.name, codename=entry.pattern.regex.pattern, content_type_id=11)

        if Permission.objects.filter(name=entry.name).count() == 0:
            perm.save()
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls


def existMail(mail):
    users = User.objects.filter(email=mail)
    if len(users) == 0:
        return False
    else:
        return True


def notifications(request):
    notification = ""
    count = 0

    if not request.user.is_anonymous:
        user = request.user
        profile = Profile.objects.get(user=user)
        notification = Notification.objects.filter(profile=profile).filter(isRead=False).order_by('-creationDate')[:10]
        count = Notification.objects.filter(profile=profile).filter(isRead=False).count()
    else:
        logout(request)
    return {'notification': notification, 'count_not': count}


# Görevi İptal Et
def make_cancel_task(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    groups = Group.objects.filter(user=user)
    active_task = Task.objects.get(pk=pk)

    task_situation = TaskSituationTask.objects.filter(task_id=active_task.pk).filter(isActive=True)

    for task in task_situation:
        task.isActive = False
        task.save()

    cancel_task = TaskSituationTask(task=active_task, task_situation=TaskSituations.objects.get(name="İptal Edildi"),
                                    isActive=True)

    cancel_task.save()

    log_content = '<p><strong style="color:red">' + groups[
        0].name + '</strong><strong style="color:red">' + active_task.pk + ' </strong> nolu görevi iptal etti.</p>'

    save_log(profile.pk, log_content)

    subject, from_email, to = 'MotoKurye Görev Bilgileri', 'burcu.dogan@oxityazilim.com', cancel_task.task.courier.courier.user.email
    text_content = 'Görev Bilgileri'
    html_content = '<p> <strong>Görev No: </strong>' + str(cancel_task.task.pk) + ' nolu göreviniz iptal edilmiştir</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return cancel_task


def save_log(profile_id, content):
    profile = Profile.objects.get(pk=profile_id)
    log = Log()
    log.profile = profile
    log.content = content
    log.save()
    return log


def return_month(month_number):
    month = ["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN", "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM",
             "ARALIK"]

    return month[int(month_number) - 1]
