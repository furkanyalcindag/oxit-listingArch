from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from kurye.models.Company import Company
from kurye.models.Request import Request
from kurye.models.RequestSituationRequest import RequestSituationRequest
from kurye.models.TaskSituationTask import TaskSituationTask


def request_report(request):
    all_request = Request.objects.all()
    canceled_request = 0
    completed_task = 0
    active = 0
    obj_array = []

    companies = Company.objects.filter(~Q(profile__user__groups__name='Admin'))

    for company in companies:
        obj = dict()

        completed_task = TaskSituationTask.objects.filter(
            task__request__company_id=company.pk).filter(
            Q(task_situation__name='Teslim Edildi') | Q(task_situation__name='Teslim Edilemedi')).filter(
            isActive=True).count()

        active = TaskSituationTask.objects.filter(
            task__request__company_id=company.pk).filter(
            Q(task_situation__name='Paket Alımı İçin Yolda') | Q(
                task_situation__name='Paket Teslimi İçin Yolda') | Q(task_situation__name='Kurye Atandı')).filter(
            isActive=True).count()

        canceled_request = RequestSituationRequest.objects.filter(
            request__company_id=company.pk).filter(
            Q(request_situation__name='İptal Edildi')).count()

        obj['company'] = company
        obj['requests'] = Request.objects.filter(company_id=company.pk).count()
        obj['cancel_count'] = canceled_request
        obj['completed_request'] = completed_task
        obj['active'] = active
        obj_array.append(obj)

    return render(request, 'request-report.html',
                  {'obj': obj_array})


def task_timeline(request):
    tasks = TaskSituationTask.objects.order_by('creationDate')
    return render(request, 'task-timeline.html', {'tasks': tasks})
