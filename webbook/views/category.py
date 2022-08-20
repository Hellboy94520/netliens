from faulthandler import is_enabled
from django.http import HttpResponse
from rest_framework import viewsets

from webbook.models.category import Category
from webbook.serializers.category import CategorySerializer

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get(self, *args, **kwargs):
    #   main_categories = CategoryData.objects.filter(language=Language.FR, category__in=Category.objects.filter(parent=None, is_enabled=True, is_visible=True))
    #   return HttpResponse(dict(), "application/javascript")