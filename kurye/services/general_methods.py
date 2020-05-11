from kurye.models import MenuUser, MenuAdmin, MenuCourier, Request, RequestSituations, Task, TaskSituations


def getUserMenu(request):
    usermenus = MenuUser.objects.all().order_by('id')

    return {'usermenus': usermenus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all().order_by('id')
    return {'adminmenus': adminmenus}


def getCourierMenu(request):
    couriermenus = MenuCourier.objects.all().order_by('id')
    return {'couriermenus': couriermenus}


def activeRequest(request, pk):
    request1 = Request.objects.get(pk=pk)
    request1.request_situation.add(RequestSituations.objects.get(name="Onaylandı"))
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



