from django.contrib.auth.models import Group, User, Permission
from django.urls import resolve

from listArch.models.Log import Log
from listArch.models.Menu import Menu


def activeMenu(request):
    url_name = request.resolver_match.url_name
    app_name = resolve(request.path).app_name
    url = app_name + ':' + url_name
    obj = None
    parent = None

    obj = None
    parent = None
    if app_name != 'accounts':
        user = request.user
        groups = Group.objects.filter(user=user)
        if groups[0].name == "Admin":
            obj = Menu.objects.filter(url=url)
            if obj.count() > 0 and obj[0].parent:
                parent = Menu.objects.get(pk=obj[0].parent_id)
        elif groups[0].name == "Firma":
            obj = Menu.objects.filter(url=url)
            if obj.count() > 0 and obj[0].parent:
                parent = Menu.objects.get(pk=obj[0].parent_id)

        else:
            obj = None

        if obj.count() == 0:
            obj = []
            x = Menu(url="")
            obj.append(x)

        return {"url": url, 'self': obj[0].parent, 'parent': parent, 'obj': obj[0]}

    return {"url": url, 'self': obj, 'parent': parent, 'obj': obj}


def getMenu(request):
    menus = Menu.objects.all().order_by('order')
    return {'menus': menus}


def category_parent_show(self):
    if self.parent:
        if self.parent.parent:
            if self.parent.parent.parent:
                if self.parent.parent.parent.parent:
                    return '%s %s %s %s %s %s %s %s %s' % (
                        self.name, '>', self.parent.name, '>', self.parent.parent.name, '>',
                        self.parent.parent.parent.name, '>', self.parent.parent.parent.parent.name)
                else:
                    return '%s %s %s %s %s %s %s' % (
                        self.name, '>', self.parent.name, '>', self.parent.parent.name, '>',
                        self.parent.parent.parent.name)

            else:
                return '%s %s %s %s %s' % (self.name, '>', self.parent.name, '>', self.parent.parent.name)

        else:
            return '%s %s %s' % (self.name, '>', self.parent.name)
    else:
        return '%s %s' % (self.name, '>')


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


def save_log(user_id, content):
    user = User.objects.get(pk=user_id)
    log = Log()
    log.user = user
    log.content = content
    log.save()
    return log


def show_urls(urllist, depth=0):
    urls = []

    # show_urls(urls.urlpatterns)
    for entry in urllist:

        urls.append(entry)
        perm = Permission(name=entry.name, codename=entry.pattern.regex.pattern, content_type_id=11)

        if Permission.objects.filter(name=entry.name).count() == 0:
            perm.save()
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

    return urls