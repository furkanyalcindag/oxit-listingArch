from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view

from listArch.Forms.FeatureValueForm import FeatureValueForm
from listArch.Forms.FeatureForm import FeatureForm
from listArch.models import OptionValueDesc, OptionDesc
from listArch.models.Option import Option
from listArch.models.OptionValue import OptionValue
from listArch.serializers.OptionSerializer import OptionSerializer
from listArch.serializers.OptionValueSerializer import OptionValueSerializer


def add_option(request):
    if request.method == 'POST':
        try:
            type = request.POST['type']
            option_discription_tr = request.POST['option_description[tr][name]']
            option_discription_eng = request.POST['option_description[eng][name]']
            row_number = int(request.POST['row_number'])

            option = Option(key=option_discription_tr,
                            type=type)
            option.save()
            option_desc = OptionDesc(option=option, lang_code=2, description=option_discription_eng)
            option_desc.save()

            option.save()
            i = 0
            while i < row_number:
                value_tr = request.POST['option_value[' + str(i) + '][option_value_description][tr][name]']
                optionValue = OptionValue(option=option, value=value_tr)
                optionValue.save()
                value_eng = request.POST['option_value[' + str(i) + '][option_value_description][eng][name]']
                option_value_desc = OptionValueDesc(option_value=optionValue, description=value_eng, lang_code=2)
                option_value_desc.save()
                i = i + 1

            messages.success(request, "Seçenek Başarıyla eklendi.")
        except Exception as e:
            print(e)

    return render(request, 'option/add-option.html')


def feature_list(request):
    options = Option.objects.all()
    return render(request, 'option/option-list.html', {'options': options})


@api_view(http_method_names=['POST'])
def get_option(request):
    if request.POST:
        try:

            option_key = request.POST.get('option_id')
            option = Option.objects.filter(key=option_key)

            data = OptionSerializer(option, many=True)

            responseData = dict()
            responseData['options'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


@api_view(http_method_names=['POST'])
def get_option_values(request):
    if request.POST:
        try:

            option_id = request.POST.get('option_id')
            option_values = OptionValue.objects.filter(option__key=option_id)

            data = OptionValueSerializer(option_values, many=True)

            responseData = dict()
            responseData['values'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


def update_option(request, pk):
    option = Option.objects.filter(pk=pk)
    option_desc = ""
    option_values = OptionValue()
    option_array = []

    try:
        option_desc = OptionDesc.objects.filter(option=option[0])
        option_values = OptionValue.objects.filter(option=option[0])
        for option_value in option_values:
            option_dict = dict()
            option_value_desc = OptionValueDesc.objects.filter(lang_code=2).filter(option_value=option_value)
            option_dict['option_tr'] = option_value.value
            option_dict['option_eng'] = option_value_desc[0].description
            option_array.append(option_dict)

        if request.method == 'POST':

            type = request.POST['type']

            option_discription_tr = request.POST['option_description[tr][name]']
            option_discription_eng = request.POST['option_description[eng][name]']

            option[0].key = option_discription_tr
            option[0].type = type
            option[0].save()
            option_desc[0].description = option_discription_eng
            option_desc[0].save()

            option_row = int(request.POST['row_number'])


            for option_val in option_values:
                option_desc = OptionValueDesc.objects.filter(lang_code=2).filter(option_value=option_val)
                option_desc.delete()
                option_val.delete()

            i = 0
            while i < option_row:
                value_eng = request.POST['option_value[' + str(i) + '][option_value_description][eng][name]']
                value_tr = request.POST['option_value[' + str(i) + '][option_value_description][tr][name]']

                value = OptionValue(option=option[0], value=value_tr)
                value.save()
                desc = OptionValueDesc(option_value=value, lang_code=2, description=value_eng)
                desc.save()
                i = i + 1

            messages.success(request, "Seçenek Başarıyla Güncellendi.")
            return redirect('listArch:secenekler')
    except Exception as e:
        print(e)

    return render(request, 'option/option-update.html',
                  {'option_desc': option_desc[0], 'option': option[0], 'option_values': option_array,
                   'loop': option_values.count()})
