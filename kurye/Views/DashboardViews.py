from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from kurye.models import Profile, Task

# Admin İşlemleri
from kurye.models.Courier import Courier


def return_admin_dashboard(request):
    couriers = Profile.objects.filter(user__is_active=True).filter(user__groups__name='Kurye').order_by('creationDate')[
               :6]

    return render(request, 'dashboard/admin-dashboard.html', {'couriers': couriers})


# Kullanıcı İşlemleri
def return_company_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html', )


# Kurye İşlemleri
def return_courier_dashboard(request):
    return render(request, 'dashboard/courier-dashboard.html')
