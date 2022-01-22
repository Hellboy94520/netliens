class AnnuCat():
    SQL_KEY = "annu_cats"

    def __init__(self, sqlObject):
        self.cat_id = None
        self.cat_name = None
        self.cat_parent = None
        self.cat_priority = None
        self.cat_show = None
        self.cat_locked = None
        self.cat_subd_geo = None
        self.cat_subd_type = None
        self.cat_color = None

    @classmethod
    def fromSql(self, sqlObject):
        self.cat_id, self.cat_name, self.cat_parent, self.cat_priority, self.cat_show, self.cat_locked, self.cat_subd_geo, self.cat_subd_type, self.cat_color = \
            sqlObject


class AnnuDept():
    SQL_KEY = "annu_dept"

    def __init__(self, sqlObject):
        self.id_dept = None
        self.nom_dept = None
        self.id_region = None
        self.id_zone = None

    @classmethod
    def fromSql(self, sqlObject):
        self.id_dept, self.nom_dept, self.id_region, self.id_zone = \
            sqlObject

class AnnuSite():
    SQL_KEY = "annu_site"

    def __init__(self):
        self.site_id = None
        self.site_name = None
        self.site_url = None
        self.site_mail = None
        self.site_pr = None
        self.site_pr_lastchecked = None
        self.site_status = None
        self.site_dispmode = None
        self.site_reg_date = None
        self.site_valid_date = None
        self.site_mail_date = None
        self.site_dept = None
        self.site_priority = None
        self.site_ip = None
        self.site_origine = None
        self.site_clics = None
        self.site_rss = None
        self.site_lien_retour = None
        self.site_vis_retour = None
        self.site_vis_retours_06 = None
        self.site_is_officetourisme = None
        self.site_is_creteria = None
        self.site_is_1stpage = None
        self.site_residence = None
        self.site_validator = None
        self.site_pagerank = None
        self.site_lien_retour_url = None
        self.site_paypal_txn = None
        self.site_type_inscr = None

    @classmethod
    def fromSql(self, sqlObject):
        self.site_id, self.site_name, self.site_url, self.site_mail,self.site_pr, self.site_pr_lastchecked, self.site_status, self.site_dispmode, self.site_reg_date, self.site_valid_date, self.site_mail_date, self.site_dept, self.site_priority, self.site_ip, self.site_origine, self.site_clics, self.site_rss, self.site_lien_retour, self.site_vis_retour, self.site_vis_retours_06, self.site_is_officetourisme, self.site_is_creteria, self.site_is_1stpage, self.site_residence, self.site_validator, self.site_pagerank, self.site_lien_retour_url, self.site_paypal_txn, self.site_type_inscr = \
            sqlObject