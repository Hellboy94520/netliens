from django.http import HttpResponseRedirect
from django.utils.translation import activate


def activation(request, language):
    activate(language)
    return HttpResponseRedirect(request.GET['next'])