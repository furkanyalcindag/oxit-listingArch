from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view

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

    return render(request, 'feature/add-feature.html')


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
