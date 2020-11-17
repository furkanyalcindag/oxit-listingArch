from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from listArch.models import City, Country, CountryDesc, CityDesc
from listArch.services import general_methods


def add_country(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    cities = []
    country = []
    try:
        if request.method == 'POST':

            code = request.POST['country_code']
            country_tr = request.POST['country[tr]']
            country_eng = request.POST['country[eng]']

            country = Country(name=country_tr, code=code)
            country.save()

            country_desc = CountryDesc(lang_code=1, country_desc=country_tr, country=country)
            country_desc.save()

            country_desc2 = CountryDesc(lang_code=2, country_desc=country_eng, country=country)
            country_desc2.save()

            array = []
            count = request.POST['row_number']
            if count != '':
                count = count.split(',')

                for count in count:
                    array.append(count)

            for key in array:
                city_tr = request.POST['city[tr][' + key + ']']
                city_eng = request.POST['city[eng][' + key + ']']

                city = City(name=city_tr, country=country)
                city.save()

                city_desc = CityDesc(lang_code=1, city_desc=city_tr, city=city)
                city_desc.save()

                city_desc2 = CityDesc(lang_code=2, city_desc=city_eng, city=city)
                city_desc2.save()

            messages.success(request, "Seçenek Başarıyla eklendi.")
            return redirect('listArch:ulke-sehir-ekle')

        return render(request, 'Country/add-country.html', {'cities': cities, 'country': country})

    except Exception as e:
        print(e)
        return redirect('listArch:admin-error-sayfasi')


def countries(request):
    countries = Country.objects.all()
    return render(request, 'Country/country-list.html', {'countries': countries})


