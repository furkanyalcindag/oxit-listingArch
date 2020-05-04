

from kurye.models import MenuUser, MenuAdmin, MenuCourier

def getUserMenu(request):
    usermenus = MenuUser.objects.all().order_by('name')

    return {'usermenus': usermenus}


def getAdminMenu(request):
    adminmenus = MenuAdmin.objects.all().order_by('name')
    return {'adminmenus': adminmenus}

def getCourierMenu(request):
    couriermenus = MenuCourier.objects.all().order_by('name')
    return {'couriermenus': couriermenus}