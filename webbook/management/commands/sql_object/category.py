from webbook.models import Category, CategoryData
from webbook.models.language import LanguageAvailable
from django.db.models import F, Value
from django.db.models.functions import Concat

import datetime

def conversion(sqlObjectList, importUser):
    for sqlObject in sqlObjectList:
        is_enable = bool(sqlObject.get('cat_show'))
        old_migrateStatus = ""

        # --------------------------
        # Verification if sql data has know issue
        # --------------------------
        # Check if parent is key is not identical as current one
        if sqlObject.get('cat_id') == sqlObject.get('cat_parent'):
            old_migrateStatus = f"[IMPORT] - [ERROR]: Identical value on cat_id and cat_parent;"
            is_enable = False

        # --------------------------
        # Model creation
        # --------------------------
        category = Category.objects.create(
            is_enable = is_enable,
            old_sqlId = int(sqlObject.get('cat_id')),
            old_migrateStatus = str(old_migrateStatus),
            creation_user = importUser,
            approval_date = datetime.datetime.now(),
            approval_user = importUser
        )
        CategoryData.objects.create(
            name = str(sqlObject.get('cat_name')),
            resume = str(sqlObject.get('cat_name')),
            language = LanguageAvailable.FR.value,
            category = category
        )

    # --------------------------
    # Add parent
    # --------------------------
    for sqlObject in sqlObjectList:
        # If there is no parent nothing to do
        if sqlObject.get('cat_parent') == 0:
            continue

        resultat = Category.objects.filter(old_sqlId=sqlObject.get('cat_parent'))
        # if no parent is find
        if len(resultat) == 0:
            Category.objects.filter(old_sqlId=sqlObject.get('cat_id')).update(
                old_migrateStatus = Concat(F('old_migrateStatus'), Value(f"[IMPORT] - [ERROR]: Parent {sqlObject.get('cat_parent')} is not find;")),
                is_enable = False
            )
            continue
        # if several parent are find
        # Impossible case

        # Save informations find
        Category.objects.filter(old_sqlId=sqlObject.get('cat_id')).update(
            parent = resultat[0]
        )

    #TODO: What about the order ?