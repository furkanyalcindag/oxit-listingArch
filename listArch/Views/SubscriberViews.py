from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render

from listArch.models import Subscriber


def add_subscriber(request):
    try:
        if request.method == 'POST':
            email = request.POST['subscriber']
            subscriber = Subscriber(email=email)
            subscriber.save()
            messages.success(request, "Abonelik İsteği Başarıyla İletildi .")
            return redirect('listArch:index')

    except Exception as e:
        print(e)


def subscriber_list(request):
    return render(request, 'subscriber_list.html')


def approve_subscriber(request):
    if request.POST:
        try:
            subscriber_id = request.POST['subscriber_id']
            subscriber = Subscriber.objects.get(pk=subscriber_id)
            subscriber.isActive = True
            subscriber.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def passive_subscriber(request):
    if request.POST:
        try:
            subscriber_id = request.POST['subscriber_id']
            subscriber = Subscriber.objects.get(pk=subscriber_id)
            subscriber.isActive = False
            subscriber.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
