import logging

from webbook.models import Category, CategoryData
from webbook.models.abstract.language import Language
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

def conversion(sqlObjectList, importUser):
    # --------------------------
    # Create Models from SQL Database
    # --------------------------
    for sqlObject in sqlObjectList:
        is_visible = bool(sqlObject.get('cat_show'))

        # --------------------------
        # Verification if sql data has know issue
        # --------------------------
        # Check if parent is key is not identical as current one
        if sqlObject.get('cat_id') == sqlObject.get('cat_parent'):
            logging.error(f"Identical value on cat_id and cat_parent for id={int(sqlObject.get('cat_id'))}!")
            is_visible = False

        # --------------------------
        # Model creation
        # --------------------------
        category = Category.objects.create(
            is_enable = True,
            is_visible = is_visible,
            creation_user = importUser,
            # TODO: Get the real date
            approval_date = datetime.now(),
            approval_user = importUser
        )
        CategoryData.objects.create(
            name = str(sqlObject.get('cat_name')),
            description = str(sqlObject.get('cat_name')),
            language = Language.FR,
            category = category
        )

        # --------------------------
        # Saving old data in cache
        # --------------------------
        cache.set(f"sql:migration:category:association:{int(sqlObject.get('cat_id'))}", category.pk, None)

    # --------------------------
    # Add parent to model created in PostgreSql
    # --------------------------
    for sqlObject in sqlObjectList:
        # If there is no parent nothing to do
        if sqlObject.get('cat_parent') == 0:
            continue

        # Get children Category
        child_pk = cache.get(f"sql:migration:category:association:{int(sqlObject.get('cat_id'))}")
        if not child_pk:
            logging.error(f"Impossible to find the Category child pk={child_pk} for sql_category {int(sqlObject.get('cat_id'))} !")
            continue
        try:
            child = Category.objects.get(pk=child_pk)
        except ObjectDoesNotExist:
            logging.error(f"Impossible to get the Category child pk={child_pk} for sql_category {int(sqlObject.get('cat_id'))} from database !")
            continue

        # Get parent Category
        parent_pk = cache.get(f"sql:migration:category:association:{int(sqlObject.get('cat_parent'))}")
        if not parent_pk:
            logging.error(f"Impossible to find the Category parent pk={child_pk} for sql_category {int(sqlObject.get('cat_parent'))} !")
            continue
        try:
            parent = Category.objects.get(pk=parent_pk)
        except ObjectDoesNotExist:
            logging.error(f"Impossible to get the Category parent pk={parent_pk} for sql_category {int(sqlObject.get('cat_parent'))} !")
            continue

        # Saving parent into child
        child.parent = parent
        child.save()

    #TODO: What about the order ?
