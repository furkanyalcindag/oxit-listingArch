import json

from django import template
from django.conf import settings

from oxiterp.settings.base import home_lang_code

register = template.Library()

@register.filter(name='get_item_by_lang')
def get_value_by_lang(key):
    lang = home_lang_code
    json_data = None

    if lang == '1':
        json_data = open(settings.BASE_DIR + '/listArch/jsons/tr.json', 'r', encoding='utf-8')
    elif lang == '2':
        json_data = open(settings.BASE_DIR + '/listArch/jsons/eng.json', 'r', encoding='utf-8')
    else:
        json_data = None
    data1 = json.load(json_data)  # deserialises it

    data2 = json.dumps(data1)  # jsons formatted string
    json_data.close()
    return data1[0].get(key)
