import datetime

from django.contrib.auth.models import User
from django.shortcuts import render

from listArch.models import Company, Product, Category


def admin_dashboard(request):
    companies = Company.objects.filter(user__is_active=True)
    products = Product.objects.all()
    d = datetime.datetime.today() - datetime.timedelta(hours=0, minutes=10)

    online = User.objects.filter(is_superuser=False).filter(last_login__gt=d).count()

    return render(request, 'dashboard/admin.html',
                  {'companies': companies.count(), 'products': products.count(), 'online': online})


def user_dashboard(request):
    return render(request, 'dashboard/user.html')

def staff_dashboard(request):
    return render(request, 'dashboard/staff.html')

def company_dashboard(request):
    user = request.user
    company = Company.objects.get(user=user)
    products = Product.objects.filter(company=company)
    return render(request, 'dashboard/company.html', {'products': products.count()})
