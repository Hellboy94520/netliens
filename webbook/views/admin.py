from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import Http404
from django.utils import translation

from ..models import Category, Localisation, get_all_modelDataWithPosition_in_order

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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_main'] = Category.get_categoryWithData(
            language=translation.get_language(),
            order='order',
            parent=None,
            is_enable=True)
        return context


@method_decorator(staff_required, name='dispatch')
class CategoryView(TemplateView):
    """
        HomeView for Admin
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']  = get_all_modelDataWithColumn_in_order(
            model=Category,
            language = translation.get_language()
        )
        return context

@method_decorator(staff_required, name='dispatch')
class LocalisationView(TemplateView):
    """
        HomeView for Admin
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['localisation_continent'] = Localisation.get_localisationWithData(
            language=translation.get_language(),
            order='order')
        context['localisation_continent'] = Localisation.get_localisationWithData(
            language=translation.get_language(),
            order='order')
        return context