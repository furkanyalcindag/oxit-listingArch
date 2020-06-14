from django.shortcuts import render_to_response

from django.template import RequestContext


def error_404_view(request):
    return render_to_response('404.html', RequestContext(request))


def error_500_view(request):
    return render_to_response('404.html', RequestContext(request))
