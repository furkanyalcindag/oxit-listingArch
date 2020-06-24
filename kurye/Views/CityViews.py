from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from kurye.Forms.NeighborhoodUpdateForm import NeighborhoodUpdateForm
from kurye.Forms.NeighborhoodForm import NeighborhoodForm
from kurye.models import Neighborhood
from kurye.models.City import City
from kurye.models.District import District
from kurye.models.Profile import Profile
from kurye.serializers.DistrictSerializer import DistrictSerializer
from kurye.serializers.NeighborhoodSerializer import NeighborhoodSerializer
from kurye.services import general_methods
from kurye.services.general_methods import save_log


@api_view(http_method_names=['POST'])
def get_districts(request):
    if request.POST:
        try:

            il_id = request.POST.get('il_id')
            districts = District.objects.filter(city_id=il_id)

            data = DistrictSerializer(districts, many=True)

            responseData = dict()
            responseData['ilceler'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_neighborhood(request):
    if request.POST:
        try:

            ilce_name = request.POST.get('ilce_id')
            neighborhoods = Neighborhood.objects.filter(district=ilce_name)

            data = NeighborhoodSerializer(neighborhoods, many=True)

            responseData = dict()
            responseData['neighborhoods'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


# Mahalle kaydet
def add_neighborhood(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    cities = City.objects.all()
    form = NeighborhoodForm()
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = NeighborhoodForm(request.POST)

        city_id = request.POST['city']
        city = City.objects.get(pk=city_id)
        if form.is_valid():

            neighborhood = Neighborhood(city=city, district=form.cleaned_data['district'],
                                        neighborhood_name=form.cleaned_data['neighborhood_name'],
                                        price=form.cleaned_data['price'])
            neighborhood.save()
            log_content = '<p><strong style="color:red">' + neighborhood.neighborhood_name + ' </strong>  Mahallesi eklendi.</p>'

            save_log(profile.pk, log_content)
            messages.success(request, 'Mahalle bilgileri başarılıyla kayıt edildi.')
        else:
            messages.warning(request, 'Alanları kontrol ediniz.')

    return render(request, 'add-neighborhood.html', {'cities': cities, 'form': form})


# Mahalle güncelle
def update_neighborhood(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    user = request.user
    profile = Profile.objects.get(user=user)
    cities = City.objects.all()
    neighborhood = Neighborhood.objects.get(uuid=uuid)
    form = NeighborhoodUpdateForm(request.POST or None, instance=neighborhood)

    if request.method == 'POST':

        city_id = request.POST['city']
        city = City.objects.get(pk=city_id)
        if form.is_valid():

            neighborhood.city = city
            neighborhood.neighborhood_name = form.cleaned_data['neighborhood_name']
            neighborhood.price = form.cleaned_data['price']
            neighborhood.district = form.cleaned_data['district']
            neighborhood.save()
            log_content = '<p><strong style="color:red">' + neighborhood.neighborhood_name + ' </strong>  mahallesi güncellendi.</p>'

            save_log(profile.pk, log_content)

            messages.success(request, 'Mahalle bilgileri başarılıyla güncellendi.')
            return redirect('kurye:mahalle-ekle')
        else:
            messages.warning(request, 'Alanları kontrol ediniz.')

    return render(request, 'add-neighborhood.html', {'cities': cities, 'form': form, 'ilce': neighborhood.district,
                                                     'mahalle': neighborhood.neighborhood_name})


def neighborhoods(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'neighborhood-list.html', )
