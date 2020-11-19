from django.contrib.auth.models import Group, User, Permission
from django.urls import resolve
from django.utils.crypto import get_random_string

from listArch.models.HeaderTextDesc import HeaderTextDesc
from listArch.models.ScrollingText import ScrollingText
from listArch.models.ScrollingTextDesc import ScrollingTextDesc
from listArch.models.Company import Company
from listArch.models.Log import Log
from listArch.models.Menu import Menu
from oxiterp.settings.base import home_lang_code


def activeMenu(request):
    if request.user.is_authenticated and request.user.is_anonymous == False:
        user = request.user
        groups = Group.objects.filter(user=user)
        if groups[0].name != 'Musteri':
            url_name = request.resolver_match.url_name
            app_name = resolve(request.path).app_name
            url = app_name + ':' + url_name

            obj = None
            parent = None

            if app_name != 'accounts':

                if groups[0].name == "Admin" or groups[0].name == "Firma" or groups[0].name == "Personel":
                    obj = Menu.objects.filter(url=url)
                    if obj.count() > 0 and obj[0].parent:
                        parent = Menu.objects.get(pk=obj[0].parent_id)


                else:
                    obj = Menu()

                if obj.count() == 0:
                    obj = []
                    x = Menu(url="")
                    obj.append(x)

                return {"url": url, 'self': obj[0].parent, 'parent': parent, 'obj': obj[0]}

    return {"url": "", 'self': "", 'parent': "", 'obj': ""}


def getMenu(request):
    if request.user.is_authenticated and request.user.is_anonymous == False:
        user = request.user
        group = Group.objects.get(user=user)
        menus = Menu.objects.filter(group=group).order_by('order')
        return {'menus': menus}
    return {'menus': ""}


def category_parent_show(self):
    if self.parent:
        if self.parent.parent:
            if self.parent.parent.parent:
                if self.parent.parent.parent.parent:
                    return '%s %s %s %s %s %s %s %s %s %s' % (
                        self.parent.parent.parent.parent.name, '>', self.parent.parent.parent.name, '>',
                        self.parent.parent.name, '>',
                        self.parent.name, '>', self.name, '>')
                else:
                    return '%s %s %s %s %s %s %s' % (
                        self.parent.parent.parent.name, '>', self.parent.parent.name, '>', self.parent.name, '>',
                        self.name)

            else:
                return '%s %s %s %s %s' % (self.parent.parent.name, '>', self.parent.name, '>', self.name)

        else:
            return '%s %s %s' % (self.parent.name, '>', self.name)
    else:
        return '%s %s' % (self.name, '>')


def control_access(request):
    if not request.user.is_anonymous:
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


def get_random_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def parent_categories_list(request):
    from listArch.models import CategoryDesc
    categories = CategoryDesc.objects.filter(lang_code=home_lang_code).filter(category__is_parent=True).filter(
        category__isBasic=True).filter(category__isActive=True).order_by('category__order')
    return {"parent_categories": categories}


def get_all_category(request):
    from listArch.models import Category
    categories = Category.objects.filter(isActive=True).order_by('order')
    return {"categories": categories}


def categories(request):
    from listArch.models import CategoryDesc
    categories = CategoryDesc.objects.filter(category__isActive=True).filter(category__is_parent=False).order_by(
        'category__order')
    return {"sub_categories": categories}


def get_company(request):
    companies = Company.objects.all()
    return {'companies': companies}


def get_user(request):
    if request.user.is_anonymous == False:
        group = Group.objects.get(user=request.user)
        if request.user.is_authenticated and group.name == 'Firma':
            user = request.user
            company = Company.objects.get(user=user)
            return {'company': company}
    return {}


def get_scrolling_text(request):
    scrolling = ScrollingText.objects.filter(isActive=True)
    if scrolling.count() > 0:
        scrolling_tr = ScrollingTextDesc.objects.filter(text=scrolling[0]).filter(lang_code=home_lang_code)[0]
        return {'scrolling_text': scrolling_tr}
    return {}


def headerText(request):
    headerText = HeaderTextDesc.objects.filter(headerText__isActive=True).filter(lang_code=home_lang_code)
    if headerText.count() > 0:
        return {'headerText': headerText[0]}
    return {}


def get_lang_code(request):
    lang_code = home_lang_code
    return {'lang_code': lang_code}
