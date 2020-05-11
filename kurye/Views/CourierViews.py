import datetime

from django.contrib import messages
from django.shortcuts import render

from kurye.Forms.TaskUpdateForm import TaskUpdateForm
from kurye.models import Profile, Task, TaskSituations
from kurye.models.Courier import Courier
from kurye.models.TaskSituationActive import TaskSituationActive


# atanmış görevleri güncelleme
def assigned_task(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    courier = Courier.objects.get(courier=profile)
    tasks = Task.objects.filter(courier=courier)
    date_current = datetime.datetime.today().date()
    time_current = datetime.datetime.today().time()

    task_form = TaskUpdateForm()

    if request.method == 'POST':
        task_form = TaskUpdateForm(request.POST)
        pk = request.POST['task']
        task = Task.objects.get(pk=int(pk))

        if task_form.is_valid():
            situation = TaskSituations.objects.get(pk=int(request.POST['task_situation']))
            task.task_situation.add(situation)
            task.save()
            task_situation_active = TaskSituationActive(task=task, isActive=True)
            task_situation_active.save()

            if situation.name == 'Teslim Edildi' or situation.name == 'Teslim Edilemedi':
                task.deliveryDate = date_current
                task.deliveryTime = time_current
                task.save()

            messages.success(request, 'Görev Durumu Güncellendi.')

    return render(request, 'Courier/courier-task-update.html', {'tasks': tasks, 'task_form': task_form})
