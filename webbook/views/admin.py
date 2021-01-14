from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import Http404

# -----------------------------
# Decorator
# -----------------------------
def staff_required(function):
    """
        Decorator used to allow staff only.
        If not, return 404 page
    """
    def wrap(request, *args, **kwargs):
        if not request.user:
            return Http404()
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise Http404()
    wrap.__doc__ = function.__doc__
    return wrap

def superuser_required(function):
    """
        Decorator used to allow superuser only.
        If not, return 404 page
    """
    def wrap(request, *args, **kwargs):
        if not request.user:
            raise Http404()
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise Http404()
    wrap.__doc__ = function.__doc__
    return wrap


@method_decorator(staff_required, name='dispatch')
class HomeView(TemplateView):
    """
        HomeView for Admin
    """
