from datetime import datetime
from django.core.cache import cache

from webbook.models import Announcement, AnnouncementData
from webbook.models import Category
from webbook.models.abstract.language import Language
from webbook.management.commands.sql_object.localisation import sqlAssociation

import re, logging

RE_WEBADDR_CONTENT='(?:http|https)://www\.(\S+)(?:\.\S+)'
DEFAULT_WEB_ADDRESS = "IMPORT"

def conversion(sqlAnnuSiteList, annuSiteAppartientModelName, sqlPointer, importUser):
    print("\033[2K", end="\r") # Cleaning current line to print progression
    #TODO: Remove the limit fixed to first 1000
    for progression, sqlObject in enumerate(sqlAnnuSiteList[:1000]):
        return_url = sqlObject.get('site_lien_retour_url') if sqlObject.get('site_lien_retour_url') else None
        return_url_quantity = sqlObject.get('site_lien_retour') if sqlObject.get('site_lien_retour') else 0
        is_visible_by_officetourisme = True if sqlObject.get('site_is_officetourisme') else False
        is_enable = True if sqlObject.get('site_status') == 9 else False
        is_visible = True if sqlObject.get('site_status') == 9 else False
        nl = sqlObject.get('site_pr') if sqlObject.get('site_pr') else 0
        click_quantity = sqlObject.get('site_click') if sqlObject.get('site_click') else 0
        creation_date = datetime.fromtimestamp(sqlObject.get('site_reg_date')) if sqlObject.get('site_reg_date') != 0 else datetime.today()
        approval_date = datetime.fromtimestamp(sqlObject.get('site_valid_date')) if sqlObject.get('site_valid_date') != 0 else None
        last_update_date = datetime.fromtimestamp(sqlObject.get('site_pr_lastchecked')) if sqlObject.get('site_pr_lastchecked') else datetime.today()

        # Saving old Sql key in cache
        l_old_sqlId = int(sqlObject.get('site_id'))

        # --------------------------
        # Verification if sql data has know issue
        # --------------------------
        # - Visible and Enable
        is_enable = False
        is_visible = False
        if sqlObject.get('site_status') == 0:
            # Waiting Approval
            is_enable = False
            is_visible = False
        elif sqlObject.get('site_status') == 2:
            # Postpone
            #TODO
            pass
        elif sqlObject.get('site_status') == 3:
            # Approved
            is_enable = True
            is_visible = True
        elif sqlObject.get('site_status') == 4:
            # Deleted
            is_enable = False
            is_visible = False
        elif sqlObject.get('site_status') == 6:
            # Specials
            #TODO
            pass

        # - Url
        try:
            url = re.match(RE_WEBADDR_CONTENT, sqlObject.get('site_url')).groups(1)[0]
        except:
            is_enable = False
            is_visible = False
            logging.error(f"Impossible to find a valid web url {sqlObject.get('site_url')} !")
            url = f"{DEFAULT_WEB_ADDRESS}_{l_old_sqlId}"
        else:
            url_identical = Announcement.objects.filter(url=url)
            if url_identical.count() > 0:
                is_enable = False
                is_visible = False
                logging.error(f"Web Url already exists {list(url_identical.values_list('pk', flat=True))} !")
                i = 0
                while Announcement.objects.filter(url=url).count() > 0:
                    url = url.replace(f"_ IMPORT_{i}", "")
                    i = i+1
                    url = f"{url}_IMPORT_{i}"

        # - Website
        website = sqlObject.get('site_url')
        website_identical = Announcement.objects.filter(website=website)
        if website_identical.count() > 0:
            is_enable = False
            is_visible = False
            logging.error(f"Website is identical to other(s) {list(website_identical.values_list('pk', flat=True))} !")
            i = 0
            while Announcement.objects.filter(website=website):
                website = website.replace(f".IMPORT_{i}", "")
                i = i+1
                website = f"{website}.IMPORT_{i}"

        # - Category
        try:
            annu_site_appartient = sqlPointer.runSqlCommand(f"select * from `{annuSiteAppartientModelName}` WHERE `app_site_id` = {l_old_sqlId}")
            if len(annu_site_appartient) != 1:
                raise Exception(f"[ERROR] Can not find an association with a Category for Site sqlId='{l_old_sqlId}': {annu_site_appartient}")
            category_id = annu_site_appartient[0].get("app_cat_id")
            category_pk = cache.get(f"sql:migration:category:association:{category_id}")
            category = Category.objects.get(pk=category_pk)
        except Exception as e:
            category = None
            is_enable = False
            is_visible = False
            logging.error("Impossible to find a Category associated !")

        # - Localisation
        localisation = None
        if sqlObject.get('site_dept'):
            try:
                localisation = sqlAssociation(sqlObject.get('site_dept'))
            except Exception as e:
                localisation = None
                is_enable = False
                is_visible = False
                logging.error(f"Impossible to find a Localisation with an id='{sqlObject.get('site_dept')}' associated !")

        # --------------------------
        # User account creation
        # --------------------------
        # - Owner
        owner = importUser
        #TODO: Find Compte pro and set is_vip as True if it is
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
            click_quantity = click_quantity,
            return_url = return_url,
            return_url_quantity = return_url_quantity,
            is_visible_by_officetourisme = is_visible_by_officetourisme,
            is_enable = is_enable,
            is_visible = is_visible,
            owner = owner,
            creation_date = creation_date,
            creation_user = importUser,
            last_update_date = last_update_date,
            approval_date = approval_date,
            approval_user = approval_user
        )
        AnnouncementData.objects.create(
            name = sqlObject.get('site_name'),
            language = Language.FR,
            announcement = announcement
        )
        cache.set(f"sql:migration:announcement:association:{l_old_sqlId}", announcement.pk, None)
        print(f"[RUNNING] {progression}/{len(sqlAnnuSiteList)} Announcement created...", end="\r")