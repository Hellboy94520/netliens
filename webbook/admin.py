from unicodedata import category
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from webbook.models.category import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ("is_enable", )
    search_fields = ("id", "name")
    list_display = ("id", "name", "creation_date")

admin.site.register(Category, CategoryAdmin)
