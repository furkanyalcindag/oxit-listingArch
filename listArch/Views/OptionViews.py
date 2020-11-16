from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from listArch.Forms.OptionForm import OptionForm
from listArch.Forms.OptionCategoryForm import OptionCategoryForm
from listArch.models import OptionValueDesc, OptionDesc
from listArch.models.Option import Option
from listArch.models.OptionValue import OptionValue
from listArch.serializers.OptionValueDescSerializer import OptionValueDescSerializer
from listArch.serializers.OptionValueSerializer import OptionValueSerializer
from listArch.services import general_methods


def add_option(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    category_form = OptionCategoryForm()
    option_form = OptionForm()
    if request.method == 'POST':
        category_form = OptionCategoryForm(request.POST)
        option_form = OptionForm(request.POST)

        try:
            if category_form.is_valid() and option_form.is_valid():

                type = request.POST['type']
                option_description_tr = request.POST['option_description[tr][name]']
                option_description_eng = request.POST['option_description[eng][name]']
                array = []
                count = request.POST['row_number']
                if count != '':
                    count = count.split(',')

                    for count in count:
                        array.append(count)

                option = Option(key=option_description_tr,
                                type=type)
                option.save()
                option_desc = OptionDesc(option=option, lang_code=2, description=option_description_eng)
                option_desc.save()

                option_desc2 = OptionDesc(option=option, lang_code=1, description=option_description_tr)
                option_desc2.save()

                is_basic = option_form.cleaned_data['isBasic']
                if is_basic:
                    option.isBasic = True
                    option.save()
                else:

                    for category in category_form.cleaned_data['category']:
                        option.category.add(category)

                if option.type == 'range':
                    min = request.POST['option_value[min]']
                    max = request.POST['option_value[max]']
                    optionValue = OptionValue(option=option, min=min, max=max)
                    optionValue.save()
                    messages.success(request, "Seçenek Başarıyla eklendi.")
                    return redirect('listArch:secenek-ekle')


                for i in array:
                    value_tr = request.POST['option_value[' + str(i) + '][option_value_description][tr][name]']
                    optionValue = OptionValue(option=option, value=value_tr)
                    optionValue.save()
                    value_eng = request.POST['option_value[' + str(i) + '][option_value_description][eng][name]']
                    option_value_desc = OptionValueDesc(option_value=optionValue, description=value_eng, lang_code=2)
                    option_value_desc.save()
                    option_value_desc2 = OptionValueDesc(option_value=optionValue, description=value_tr, lang_code=1)
                    option_value_desc2.save()

                messages.success(request, "Seçenek Başarıyla eklendi.")
                return redirect('listArch:secenek-ekle')
            else:
                messages.success(request, "Alanları kontrol ediniz.")
        except Exception as e:
            print(e)

    return render(request, 'option/add-option.html', {'category_form': category_form, 'option_form': option_form})


def feature_list(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    options = OptionDesc.objects.filter(lang_code=1)
    return render(request, 'option/option-list.html', {'options': options})


@api_view(http_method_names=['POST'])
def get_option(request):
    if request.POST:
        try:

            option_key = request.POST.get('option_id')
            option = OptionValue.objects.filter(option__key=option_key)

            data = OptionValueSerializer(option, many=True)

            responseData = dict()
            responseData['options'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_values(request):
    if request.POST:
        try:

            option_id = request.POST.get('option_id')
            option = Option.objects.get(pk=option_id)
            option_values = OptionValueDesc.objects.filter(option_value__option_id=option_id).filter(lang_code=1)

            data = OptionValueDescSerializer(option_values, many=True)

            responseData = dict()
            responseData['values'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_option_values(request):
    if request.POST:
        try:

            option_key = request.POST.get('option_id')
            option_values = OptionValue.objects.filter(option__key=option_key)

            data = OptionValueSerializer(option_values, many=True)

            responseData = dict()
            responseData['values'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def update_option(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    option = Option.objects.get(pk=pk)
    option_desc = ""
    option_values = OptionValue()
    option_array = []
    option_form = OptionForm(request.POST or None, instance=option)
    category_form = OptionCategoryForm(request.POST or None, instance=option)

    try:
        option_desc = OptionDesc.objects.filter(option=option).filter(lang_code=2)
        option_desc2 = OptionDesc.objects.filter(option=option).filter(lang_code=1)
        option_values = OptionValue.objects.filter(option=option)

        for option_value in option_values:
            option_dict = dict()
            option_value_desc = OptionValueDesc.objects.filter(option_value=option_value).filter(lang_code=1)
            option_value_desc2 = OptionValueDesc.objects.filter(option_value=option_value).filter(lang_code=2)
            option_dict['option_value'] = option_value

            if option_value.option.type != 'range':
                option_dict['option_tr'] = option_value_desc[0]
                option_dict['option_eng'] = option_value_desc2[0]
            else:
                option_dict['option_tr'] = option_value.min
                option_dict['option_eng'] = option_value.max
            option_array.append(option_dict)

        if request.method == 'POST':
            if category_form.is_valid() and option_form.is_valid():

                isBasic = option_form.cleaned_data['isBasic']
                type = request.POST['type']

                option_description_tr = request.POST['option_description[tr][name]']
                option_description_eng = request.POST['option_description[eng][name]']

                for desc in option_desc2:
                    desc.description = option_description_tr
                    desc.save()

                for desc_tr in option_desc:
                    desc_tr.description = option_description_eng
                    desc_tr.save()

                option.key = option_description_tr
                option.save()

                option.type = type
                if isBasic:
                    option.isBasic = True
                    option.category.clear()

                else:
                    option.isBasic = False
                    for category in category_form.cleaned_data['category']:
                        option.category.add(category)

                option.save()
                for option_val in option_values:
                    option_val.delete()
                count = request.POST['row_number']
                count = count.split(',')
                array = []
                for count in count:
                    array.append(count)
                if count != '':


                    for i in array:
                        value_eng = request.POST['option_value[' + str(i) + '][option_value_description][eng][name]']
                        value_tr = request.POST['option_value[' + str(i) + '][option_value_description][tr][name]']

                        if type == 'range':
                            value = OptionValue(option=option, value=option_desc2[0].description, min=value_tr,
                                            max=value_eng)
                            value.save()
                        else:
                            value = OptionValue(option=option, value=value_tr)
                            value.save()
                            desc2 = OptionValueDesc(option_value=value, lang_code=1, description=value_tr)
                            desc2.save()
                            desc = OptionValueDesc(option_value=value, lang_code=2, description=value_eng)
                            desc.save()

                messages.success(request, "Seçenek Başarıyla Güncellendi.")
                return redirect('listArch:secenekler')
            else:
                messages.success(request, "Alanları kontrol ediniz.")
    except Exception as e:
        print(e)

    return render(request, 'option/option-update.html',
                  {'option_desc': option_desc[0], 'option': option, 'option_values': option_array,
                   'loop': option_values.count(), 'category_form': category_form, 'option_form': option_form})


@login_required
def option_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.POST:
        try:

            option_id = request.POST['option_id']
            option = Option.objects.filter(pk=option_id)
            option[0].delete()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})
