import datetime
from datetime import timedelta
import calendar
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect

from inoks.models import Order, Profile, earningPayments
from inoks.models.TotalOrderObject import TotalOrderObject
from inoks.services import general_methods, earning_methods
from inoks.services.general_methods import calculate_order_of_tree


@login_required
def return_my_earnings_report(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        userprofile = Profile.objects.filter(user=request.user)
        earnDict = dict()
        earningArray = []
        total = 0
        total_paid = 0
        not_paid = 0

        total_paid = general_methods.monthlyTotalPaidByDate(request.POST['ay'], request.POST['yil'])

        part = request.POST['ay'] + "/" + request.POST['yil']

        for user in userprofile:

            profileArray = []
            levelDict = dict()
            level = 1
            total_earning = 0

            profileArray.append(user.id)

            earning_methods.returnLevelTreeNewVersionByDate(profileArray, levelDict, level, int(request.POST['ay']),
                                                            int(request.POST['yil']))

            # for i in range(7):
            #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))
            order_total_member = earning_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
                                                                               int(request.POST['yil']))

            date = request.POST['ay'] + '/' + request.POST['yil']

            total_earning = earning_methods.calculate_earning_of_tree(levelDict, order_total_member, True, date)

            # total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member)
            x = total_earning
            earnDict[user] = x - (x * 20 / 100)
            total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                            tree_price=0, kdv_tree_price=0, income_tax_tree_price=0,
                                            total_earn_with_tax=0)
            total_object.profile = user
            total_object.earning = earnDict[user]
            total_object.total_price = order_total_member
            total_object.tree_price = earning_methods.calculate_order_of_tree(levelDict)['monthly_order']

            # total_object.kdv_tree_price = total_earning - x
            total_object.income_tax_price = (x * 20 / 100)
            total_object.total_earn_with_tax = total_earning

            payment = earningPayments.objects.filter(profile=user,
                                                     payedDate=request.POST['ay'] + "/" + request.POST['yil'])
            if payment.count() > 0:
                total_object.is_paid = True
                total_object.paid_date = payment[0].creationDate

            earningArray.append(total_object)

        for key in earnDict:
            total = total + float(earnDict[key])

        return render(request, 'kazanclar/kazanclarim.html',
                      {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                       'not_paid': float(total) - float(total_paid),
                       'part': part, 'month': request.POST['ay'], 'year': request.POST['yil']})

    userprofile = Profile.objects.filter(user=request.user)
    earnDict = dict()
    earningArray = []
    total = float(0.00)
    total_paid = 0
    not_paid = 0
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    part = str(month) + "/" + str(year)
    total_paid = general_methods.monthlyTotalPaidByDate(str(month), str(year))
    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        earning_methods.returnLevelTreeNewVersion(profileArray, levelDict, level)

        # for i in range(7):
        #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        order_total_member = earning_methods.monthlyMemberOrderTotal(user, )

        total_earning = earning_methods.calculate_earning_of_tree(levelDict, order_total_member, False, None)

        # total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member)
        # earnDict[user] = total_earning
        x = total_earning
        earnDict[user] = x - (x * 20 / 100)
        total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                        tree_price=0, kdv_tree_price=0, income_tax_tree_price=0, total_earn_with_tax=0)
        total_object.profile = user
        total_object.earning = earnDict[user]
        total_object.total_price = order_total_member

        total_object.tree_price = earning_methods.calculate_order_of_tree(levelDict)['monthly_order']
        # total_object.kdv_tree_price = total_earning - x
        total_object.income_tax_price = (x * 20 / 100)
        payment = earningPayments.objects.filter(profile=user,
                                                 payedDate=part)
        if payment.count() > 0:
            total_object.is_paid = True
            total_object.paid_date = payment[0].creationDate

        earningArray.append(total_object)

    for key in earnDict:
        total = total + float(earnDict[key])

    return render(request, 'kazanclar/kazanclarim.html',
                  {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                   'not_paid': float(total) - float(total_paid),
                   'part': part, 'month': str(month), 'year': str(year)})


@login_required
def return_all_earnings_report(request):
    total_my_orders = Order.objects.filter(isApprove=True).count()
    orders = Order.objects.filter(isApprove=True)

    return render(request, 'kazanclar/kazanclar.html', {'orders': orders, 'total_my_orders': total_my_orders})


@login_required
def return_odenenler(request):
    return render(request, 'kazanclar/odenenler.html')


"""
@login_required
def return_odenecekler(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        userprofile = Profile.objects.filter(user__is_active=True).exclude(user__groups__name="Admin")
        earnDict = dict()
        earningArray = []
        total = 0
        total_paid = 0
        not_paid = 0

        total_paid = general_methods.monthlyTotalPaidByDate(request.POST['ay'], request.POST['yil'])

        part = request.POST['ay'] + "/" + request.POST['yil']

        for user in userprofile:

            profileArray = []
            levelDict = dict()
            level = 1
            total_earning = 0

            profileArray.append(user.id)

            general_methods.returnLevelTreeByDate(profileArray, levelDict, level, int(request.POST['ay']),
                                                  int(request.POST['yil']))

            # for i in range(7):
            #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

            order_total_member = general_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
                                                                               int(request.POST['yil']))

            date = request.POST['ay'] + '/' + request.POST['yil']

            total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member, True, date)

            # earnDict[user] = total_earning
            # x = (total_earning * 100) / 118
            x = total_earning
            earnDict[user] = x - (x * 20 / 100)
            total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                            tree_price=0, kdv_tree_price=0, income_tax_tree_price=0,
                                            total_earn_with_tax=0)
            total_object.profile = user
            total_object.earning = earnDict[user]
            total_object.total_price = order_total_member
            total_object.tree_price = calculate_order_of_tree(levelDict)
            # total_object.kdv_tree_price = total_earning - x
            total_object.income_tax_price = (x * 20 / 100)
            total_object.total_earn_with_tax = total_earning

            payment = earningPayments.objects.filter(profile=user,
                                                     payedDate=request.POST['ay'] + "/" + request.POST['yil'])
            if payment.count() > 0:
                total_object.is_paid = True
                total_object.paid_date = payment[0].creationDate

            earningArray.append(total_object)

        for key in earnDict:
            total = total + float(earnDict[key])

        return render(request, 'kazanclar/odenecekler.html',
                      {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                       'not_paid': float(total) - float(total_paid),
                       'part': part, 'month': request.POST['ay'], 'year': request.POST['yil']})

    userprofile = Profile.objects.filter(user__is_active=True).exclude(user__groups__name="Admin")
    earnDict = dict()
    earningArray = []
    total = float(0.00)
    total_paid = 0
    not_paid = 0
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    part = str(month) + "/" + str(year)
    total_paid = general_methods.monthlyTotalPaidByDate(str(month), str(year))
    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        general_methods.returnLevelTree(profileArray, levelDict, level)

        # for i in range(7):
        #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        order_total_member = general_methods.monthlyMemberOrderTotal(user, )
        #order_total_member = general_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
        #                                                                   int(request.POST['yil']))

        total_earning = general_methods.calculate_earning_of_tree(levelDict, order_total_member, False, None)

        # earnDict[user] = total_earning
        # x = (total_earning * 100) / 118
        x = total_earning
        earnDict[user] = x - (x * 20 / 100)
        total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                        tree_price=0, kdv_tree_price=0, income_tax_tree_price=0, total_earn_with_tax=0)
        total_object.profile = user
        total_object.earning = earnDict[user]
        total_object.total_price = order_total_member

        total_object.tree_price = total_earning
        # total_object.kdv_tree_price = total_earning - x
        total_object.income_tax_price = (x * 20 / 100)

        payment = earningPayments.objects.filter(profile=user,
                                                 payedDate=part)
        if payment.count() > 0:
            total_object.is_paid = True
            total_object.paid_date = payment[0].creationDate

        earningArray.append(total_object)

    for key in earnDict:
        total = total + float(earnDict[key])

    ##

    return render(request, 'kazanclar/odenecekler.html',
                  {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                   'not_paid': float(total) - float(total_paid),
                   'part': part, 'month': str(month), 'year': str(year)})













"""


@login_required
def return_odenecekler(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        userprofile = Profile.objects.filter(user__is_active=True).exclude(user__groups__name="Admin")
        earnDict = dict()
        earningArray = []
        total = 0
        total_paid = 0
        not_paid = 0

        total_paid = general_methods.monthlyTotalPaidByDate(request.POST['ay'], request.POST['yil'])

        part = request.POST['ay'] + "/" + request.POST['yil']

        for user in userprofile:

            profileArray = []
            levelDict = dict()
            level = 1
            total_earning = 0

            profileArray.append(user.id)

            earning_methods.returnLevelTreeNewVersionByDate(profileArray, levelDict, level, int(request.POST['ay']),
                                                            int(request.POST['yil']))

            # for i in range(7):
            #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

            order_total_member = earning_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
                                                                               int(request.POST['yil']))

            date = request.POST['ay'] + '/' + request.POST['yil']

            total_earning = earning_methods.calculate_earning_of_tree(levelDict, order_total_member, True, date)

            # earnDict[user] = total_earning
            # x = (total_earning * 100) / 118
            x = total_earning
            earnDict[user] = x - (x * 20 / 100)
            total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                            tree_price=0, kdv_tree_price=0, income_tax_tree_price=0,
                                            total_earn_with_tax=0)
            total_object.profile = user
            total_object.earning = earnDict[user]
            total_object.total_price = order_total_member
            total_object.tree_price = earning_methods.calculate_order_of_tree(levelDict)['monthly_order']
            # total_object.kdv_tree_price = total_earning - x
            total_object.income_tax_price = (x * 20 / 100)
            total_object.total_earn_with_tax = total_earning

            payment = earningPayments.objects.filter(profile=user,
                                                     payedDate=request.POST['ay'] + "/" + request.POST['yil'])
            if payment.count() > 0:
                total_object.is_paid = True
                total_object.paid_date = payment[0].creationDate

            earningArray.append(total_object)

        for key in earnDict:
            total = total + float(earnDict[key])

        return render(request, 'kazanclar/odenecekler.html',
                      {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                       'not_paid': float(total) - float(total_paid),
                       'part': part, 'month': request.POST['ay'], 'year': request.POST['yil']})

    userprofile = Profile.objects.filter(user__is_active=True).exclude(user__groups__name="Admin")
    earnDict = dict()
    earningArray = []
    total = float(0.00)
    total_paid = 0
    not_paid = 0
    datetime_current = datetime.datetime.today()
    year = datetime_current.year
    month = datetime_current.month
    part = str(month) + "/" + str(year)
    total_paid = general_methods.monthlyTotalPaidByDate(str(month), str(year))
    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        earning_methods.returnLevelTreeNewVersion(profileArray, levelDict, level)

        # for i in range(7):
        #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        order_total_member = earning_methods.monthlyMemberOrderTotal(user, )
        # order_total_member = general_methods.monthlyMemberOrderTotalByDate(user, int(request.POST['ay']),
        #                                                                   int(request.POST['yil']))

        total_earning = earning_methods.calculate_earning_of_tree(levelDict, order_total_member, False, None)

        # earnDict[user] = total_earning
        # x = (total_earning * 100) / 118
        x = total_earning
        earnDict[user] = x - (x * 20 / 100)
        total_object = TotalOrderObject(profile=None, total_price=0, earning=0, is_paid=False, paid_date=None,
                                        tree_price=0, kdv_tree_price=0, income_tax_tree_price=0, total_earn_with_tax=0)
        total_object.profile = user
        total_object.earning = earnDict[user]
        total_object.total_price = order_total_member

        total_object.tree_price = earning_methods.calculate_order_of_tree(levelDict)['monthly_order']
        # total_object.kdv_tree_price = total_earning - x
        total_object.income_tax_price = (x * 20 / 100)

        payment = earningPayments.objects.filter(profile=user,
                                                 payedDate=part)
        if payment.count() > 0:
            total_object.is_paid = True
            total_object.paid_date = payment[0].creationDate

        earningArray.append(total_object)

    for key in earnDict:
        total = total + float(earnDict[key])

    ##

    return render(request, 'kazanclar/odenecekler.html',
                  {"earnDict": earningArray, 'total': total, 'total_paid': total_paid,
                   'not_paid': float(total) - float(total_paid),
                   'part': part, 'month': str(month), 'year': str(year)})


def calculate_earning(request):
    userprofile = Profile.objects.filter(user__is_active=True)

    earnDict = dict()

    for user in userprofile:

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(user.id)

        general_methods.returnLevelTree(profileArray, levelDict, level)

        for i in range(7):
            total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        earnDict[user] = total_earning


@login_required
def make_pay(request):
    if request.POST:
        try:

            profile_id = request.POST.get('profile_id')
            user = request.user
            part = request.POST.get('part')
            payment = request.POST.get('payment')
            profile = Profile.objects.get(id=profile_id)

            payment = earningPayments(profile=profile,
                                      payer_profile=Profile.objects.get(user=user),
                                      payedDate=part,
                                      paymentTotal=payment)

            payment.save()

            profileArray = []
            levelDict = dict()
            level = 1
            total_earning = 0

            month = part.split('/')[0]
            year = part.split('/')[1]

            profileArray.append(profile.id)

            earning_methods.returnLevelTreeNewVersionByDate(profileArray, levelDict, level, int(month),
                                                            int(year))
            total_order =earning_methods.calculate_order_of_tree(levelDict)['all_order']

            kademe = earning_methods.return_level_of_profile(total_order, levelDict)

            profile.level = kademe
            profile.save()

            # total siparişe göre kademe bilgisi atanacak

            subject, from_email, to = 'BAVEN Prim Ödeme Yapıldı', 'info@baven.net', payment.profile.user.email
            text_content = 'Sayın ' + payment.profile.user.first_name + ' ' + payment.profile.user.last_name + '<br>'
            html_content = payment.payedDate + ' dönemine ait' + payment.paymentTotal + ' ₺ ödemeiniz yapılmıştır.'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def earning_control(request):
    profile = Profile.objects.get(pk=110)
    earning1 = None
    earning = 0
    earnings = earningPayments.objects.filter(profile=profile).order_by('-id')
    if earnings.count() > 0:
        earning1 = earnings[0]
        split = earning1.payedDate.split('/')
        x = datetime.datetime(int(split[1]), int(split[0]), 1)
        days_in_month = calendar.monthrange(x.year, x.month)[1]
        start_date = x + timedelta(days=days_in_month)
        datetime_current = datetime.datetime.today()
        year = datetime_current.year
        month = datetime_current.month

        profileArray = []
        levelDict = dict()
        level = 1
        total_earning = 0

        profileArray.append(profile.id)

        general_methods.returnLevelTreeByDate(profileArray, levelDict, level, start_date.month,
                                              start_date.year)

        # for i in range(7):
        #   total_earning = float(total_earning) + float(general_methods.calculate_earning(levelDict, i + 1))

        order_total_member = general_methods.monthlyMemberOrderTotalByDate(profile, start_date.month,
                                                                           start_date.year)

        for i in range(7):

            if i + 1 == 1:
                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

            if i + 1 == 2:

                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

            if i + 1 == 3:

                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

            if i + 1 == 4:

                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

            if i + 1 == 5:

                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

            if i + 1 == 6:

                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

            if i + 1 == 7:

                for orderPrice in levelDict[str(i + 1)]:
                    earning = earning + float(orderPrice.total_order)

        print("sjdghkjsdhkjs")




    else:
        earning = 0

    return render(request, 'kazanclar/deneme.html')
