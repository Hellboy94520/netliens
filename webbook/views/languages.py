from django.shortcuts import redirect
from django.utils.translation import activate


def activation(request, language):
    activate(language)
    # Not working with apache2
    return redirect(request.GET['next'])