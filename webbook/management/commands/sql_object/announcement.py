from datetime import datetime
from webbook.models import Announcement, AnnouncementData
from webbook.models import Category, getUnknownCategory
from webbook.models import Localisation, getUnknownLocalisation
from webbook.models.abstract.language import LanguageAvailable
from webbook.management.commands.sql_object.localisation import sqlAssociation

import re

RE_WEBADDR_CONTENT='(?:http|https)://www\.(\S+)(?:\.\S+)'
DEFAULT_WEB_ADDRESS = "IMPORT"

def conversion(sqlAnnuSiteList, annuSiteAppartientModelName, sqlPointer, importUser):
    for sqlObject in sqlAnnuSiteList[:100]:
        is_enable = True if sqlObject.get('site_status') == 9 else False
        is_visible = True if sqlObject.get('site_status') == 9 else False
        old_sqlId = sqlObject.get('site_id')
        old_migrateStatus = f"[IMPORT] - [INFO]: site_status={sqlObject.get('site_status')}, site_dispmode={sqlObject.get('site_dispmode')}; "
        nl = sqlObject.get('site_pr') if sqlObject.get('site_pr') else 0
        creation_date = datetime.fromtimestamp(sqlObject.get('site_reg_date')) if sqlObject.get('site_reg_date') != 0 else datetime.today()
        approval_date = datetime.fromtimestamp(sqlObject.get('site_valid_date')) if sqlObject.get('site_valid_date') != 0 else None

        # --------------------------
        # Verification if sql data has know issue
        # --------------------------
        # - Url
        try:
            url = re.match(RE_WEBADDR_CONTENT, sqlObject.get('site_url')).groups(1)[0]
        except:
            is_visible = False
            old_migrateStatus = old_migrateStatus + "[IMPORT] - [ERROR]: Impossible to find a web url from regexp; "
            url = f"{DEFAULT_WEB_ADDRESS}_{old_sqlId}"
        else:
            url_identical = Announcement.objects.filter(url=url)
            if url_identical.count() > 0:
                is_visible = False
                old_migrateStatus = old_migrateStatus + f"[IMPORT] - [ERROR]: Url is identical to other(s) {list(url_identical.values_list('pk', flat=True))}; "
                i = 0
                while Announcement.objects.filter(url=url).count() > 0:
                    url = url.replace(f"_ IMPORT_{i}", "")
                    i = i+1
                    url = f"{url}_IMPORT_{i}"

        # - Website
        website = sqlObject.get('site_url')
        website_identical = Announcement.objects.filter(website=website)
        if website_identical.count() > 0:
            is_visible = False
            old_migrateStatus = old_migrateStatus + f"[IMPORT] - [ERROR]: Website is identical to other(s) {list(website_identical.values_list('pk', flat=True))}; "
            i = 0
            while Announcement.objects.filter(website=website):
                website = website.replace(f".IMPORT_{i}", "")
                i = i+1
                website = f"{website}.IMPORT_{i}"

        # - Category
        try:
            annu_site_appartient = sqlPointer.runSqlCommand(f"select * from `{annuSiteAppartientModelName}` WHERE `app_site_id` = {old_sqlId}")
            if len(annu_site_appartient) != 1:
                raise Exception(f"[ERROR] Can not find an association with a Category for Site sqlId='{old_sqlId}': {annu_site_appartient}")
            category_id = annu_site_appartient[0].get("app_cat_id")
            category = Category.objects.get(old_sqlId=category_id)
        except Exception as e:
            category = getUnknownCategory()
            is_visible = False
            old_migrateStatus = old_migrateStatus + "[IMPORT] - [ERROR]: Impossible to find a Category associated; "

        # - Localisation
        try:
            localisation = sqlAssociation(sqlObject.get('site_dept'))
        except Exception as e:
            localisation = getUnknownLocalisation()
            is_visible = False
            old_migrateStatus = old_migrateStatus + f"[IMPORT] - [ERROR]: Impossible to find a Localisation with an id='{sqlObject.get('site_dept')}' associated; "

        # --------------------------
        # User account creation
        # --------------------------
        # - Owner
        owner = importUser
        if sqlObject.get('site_mail'):
            # TODO: Verify if gestion or not. If not, verify if an account already exist. If not, create it
            pass

        # - Validator
        approval_user = None
        if sqlObject.get('site_validator'):
            # TODO: Create account if does not exist.
            pass

        # --------------------------
        # Model creation
        # --------------------------
        announcement = Announcement.objects.create(
            url = url,
            website = website,
            localisation = localisation,
            category = category,
            nl = nl,
            is_enable = is_enable,
            is_visible = is_visible,
            owner = owner,
            old_sqlId = old_sqlId,
            old_migrateStatus = old_migrateStatus,
            creation_date = creation_date,
            creation_user = importUser,
            approval_date = approval_date,
            approval_user = approval_user
        )
        AnnouncementData.objects.create(
            name = sqlObject.get('site_name'),
            language = LanguageAvailable.FR,
            announcement = announcement
        )
