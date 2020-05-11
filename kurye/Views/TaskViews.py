from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from kurye.models.RequestSituations import RequestSituations
from kurye.models.TaskSituationActive import TaskSituationActive
from kurye.models.TaskSituations import TaskSituations

from kurye.models.Courier import Courier
from kurye.models.Task import Task
from kurye.models.Request import Request

# Talepler
from kurye.services import general_methods


def requests(request, pk):
    courier = Courier.objects.get(pk=pk)
    request1 = Request.objects.filter(request_situation__name='Onaylandı')
    return render(request, 'Request/request.html', {'requests': request1, 'courier': courier})


# görev atama kurye seçiliyor
def add_task(request, pk):
    request1 = Request.objects.get(pk=pk)
    task = Task(request=request1)
    task.save()

    if request.method == 'POST':
        c_post = request.POST['courier']
        courier = Courier.objects.get(pk=c_post)

        task.courier = courier
        task.save()
        courier.isActive = 'False'
        courier.save()
        task.task_situation.add(TaskSituations.objects.get(name='Atandı'))
        task.save()

        messages.success(request,
                         'Görev ' + task.courier.courier.user.first_name + ' ' + task.courier.courier.user.last_name + ' a Atandı.')

    return render(request, 'Task/add-task.html', {'request': request1, })


def active_tasks(request):
    activeTasks = Task.objects.filter(task_situation__name='Yolda').order_by('id')
    return render(request, 'Task/active-tasks.html', {'active_tasks': activeTasks})


@login_required
def return_completed_request(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    task = TaskSituationActive.objects.filter(isActive=True).filter(~Q(task_situation__name='Teslim Edildi'))

    task_situation = TaskSituations.objects.all()
    return render(request, 'Request/completed-requests.html',
                  {'task': task, 'task_situation': task_situation})
