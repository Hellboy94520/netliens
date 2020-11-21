from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.views import View

from ..models import Homepage, Category, Announcement

# -----------------------------
class HomeView(View):
    """
        Authentification view
    """
    template_name = "home.html"
    homepage, is_create = Homepage.objects.get_or_create()
    main_category = Category.objects.filter(parent=None, is_enable=True).order_by('order')
    # main_announcement = Announcement.objects.filter(is_enable=True, is_valid=True, on_homepage=True)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, locals())

class CategoryView(View):
    """
        Category view
    """
    template_name = "category.html"
    main_category = Category.objects.filter(parent=None, is_enable=True).order_by('order')

    def _get_env(self, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs['category_id'])
        self.children_category = Category.objects.filter(parent=main_category, is_enable=True).order_by('order')

    def get(self, request, *args, **kwargs):
        self._get_env(*args, **kwargs)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        self._get_env(*args, **kwargs)
        return render(request, self.template_name, locals())

class AnnouncementView(View):
    """
        Announcement view
    """
    template_name = "announcement.html"

    def get(self, request, *args, **kwargs):
        announcement = get_object_or_404(Announcement, pk=kwargs['announcement_id'])
