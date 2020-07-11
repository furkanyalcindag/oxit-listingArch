from django.shortcuts import render


def admin_dashboard(request):

    return render(request, 'dashboard/admin.html')


def user_dashboard(request):
    return render(request, 'dashboard/user.html')


def company_dashboard(request):
    return render(request, 'dashboard/company.html')
