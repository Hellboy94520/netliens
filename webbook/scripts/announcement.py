from webbook.models import Announcement, AnnouncementData
from webbook.models import User, UserManager
from webbook.forms import AdminUserForm, AnnouncementUserSettingForm, AnnouncementUserDataForm
from webbook.scripts.common import Manager, ManagerSqlObject
from webbook.scripts.log import create_logger
import time

class AnnouncementManager(Manager):
    sqlTableName = "annu_site"

    def __init__(self):
        super(AnnouncementManager, self).__init__(
            className = self.__class__.__name__,
            model = Announcement,
            modelData = AnnouncementData,
            modelSql = self.AnnouncementSql
        )

    class AnnouncementSql(ManagerSqlObject):
        def __init__(self, sqlObject):
            self.site_id = sqlObject[0]
            self.site_name = sqlObject[1]
            self.site_url = sqlObject[2]
            self.site_mail = sqlObject[3]
            self.site_pr = sqlObject[4]
            self.site_pr_lastchecked = sqlObject[5]
            self.site_status = sqlObject[6]
            self.site_dispmode = sqlObject[7]
            self.site_reg_date = sqlObject[8]
            self.site_valid_date = sqlObject[9]
            self.site_mail_date = sqlObject[10]
            self.site_dept = sqlObject[11]
            self.site_priority = sqlObject[12]
            self.site_ip = sqlObject[13]
            self.site_origine = sqlObject[14]
            self.site_clics = sqlObject[15]
            self.site_rss = sqlObject[16]
            self.site_lien_retour = sqlObject[17]
            self.site_vis_retour = sqlObject[18]
            self.site_vis_retours_06 = sqlObject[19]
            self.site_is_officetourisme = sqlObject[20]
            self.site_is_creteria = sqlObject[21]
            self.site_is_1stpage = sqlObject[22]
            self.site_residence = sqlObject[23]
            self.site_validator = sqlObject[24]
            self.site_pagerank = sqlObject[25]
            self.site_lien_retour_url = sqlObject[26]
            self.site_paypal_txn = sqlObject[27]
            self.site_type_inscr = sqlObject[28]

    def createModelFromSql(self, key, sqlObject, sqlObjectMap, functionnalUser: User):#, categorySqlsAssociationMap, localisationSqlAssociationMap):
        # Create user with email adress if exist
        l_user = None
        if sqlObject.site_mail:
            l_email = sqlObject.site_mail.lower()
            self.logging.debug(f"Email = {l_email}")
            userQuerySet = User.objects.filter(email=l_email)
            self.logging.debug(f"QuerySet Count = {userQuerySet.count()}")
            for user in userQuerySet:
                self.logging.debug(f"User = {user}")
            if userQuerySet.count() == 0:
                l_user = User.objects.create_user(email=l_email)
                self.logging.debug(f"User creation = {l_user}")
            else:
                l_user = userQuerySet[0]
                self.logging.debug(f"User used = {l_user}")
            self.logging.debug(f"--------")
            # if User.objects.filter(email=sqlObject.site_mail.lower()):
            #     l_user = UserManager.create_user(email=sqlObject.site_mail.lower())
            # else:
            #     User.objects.get(email=sqlObject.site_mail.lower())
        # if sqlObject.site_mail:
        #     l_userQuery = User.objects.filter(email=sqlObject.site_mail.lower())
        #     if l_userQuery.count() == 0:
        #         l_user = User.objects.create_user(email=sqlObject.site_mail.lower())
        #     else:
        #         print(l_userQuery.count())
        #         print(l_userQuery[0])
        #         l_user = l_userQuery[0]

        # l_announcementForm = AnnouncementUserSettingForm(
        #     data={
        #         'url': sqlObject.site_name,
        #         'website': sqlObject.site_url,
        #         # 'nl': sqlObject.site_pr,
        #         'owner': l_user
        #     }
        # )
            #self.logging.warning(f"No email find for: '{sqlObject.site_url}'")

# class AnnouncementManager():
#     _sql_table_name = "annu_site"
#     _announcementSql_list = {}
#     _announcementMongo_dict = {}
#     logging = create_logger('AnnouncementManager')

#     def __init__(self):
#         self.logging.debug("init starting...")
#         self.logging.debug("init done")

#     def deleteAnnouncement():
#         return deleteModel(
#             model=Announcement,
#             modelData=AnnouncementData,
#             logging=AnnouncementManager.logging
#         )

#     def createAnnouncementFromSql(self, sqlObjectList: list, categorySqlAssociationMap: dict, localisationSqlAssociationMap: dict, functionnalUser: User):
#         # Convert Sql to Python object
#         for key, value in sqlObjectList.items():
#             self._announcementSql_list[key] = self.AnnouncementSql(value)

#         if len(self._announcementSql_list) == 0:
#             self.logging.critical(f"No {self.AnnouncementSql.__class__.__name__} has been created !")
#         if len(self._announcementSql_list) != len(sqlObjectList):
#             self.logging.critical(f"Impossible to create all {AnnouncementSql.__class__.__name__} ! \
#                 Get {len(self._announcementSql_list)} {self.AnnouncementSql.__class__.__name__} instead of {len(sqlObjectList)}")


#     class AnnouncementSql():
#         def __init__(self, sqlObject):
#             self.site_id = sqlObject[0]
#             self.site_name = sqlObject[1]
#             self.site_url = sqlObject[2]
#             self.site_mail = sqlObject[3]
#             self.site_pr = sqlObject[4]
#             self.site_pr_lastchecked = sqlObject[5]
#             self.site_status = sqlObject[6]
#             self.site_dispmode = sqlObject[7]
#             self.site_reg_date = sqlObject[8]
#             self.site_valid_date = sqlObject[9]
#             self.site_mail_date = sqlObject[10]
#             self.site_dept = sqlObject[11]
#             self.site_priority = sqlObject[12]
#             self.site_ip = sqlObject[13]
#             self.site_origine = sqlObject[14]
#             self.site_clics = sqlObject[15]
#             self.site_rss = sqlObject[16]
#             self.site_lien_retour = sqlObject[17]
#             self.site_vis_retour = sqlObject[18]
#             self.site_vis_retours_06 = sqlObject[19]
#             self.site_is_officetourisme = sqlObject[20]
#             self.site_is_creteria = sqlObject[21]
#             self.site_is_1stpage = sqlObject[22]
#             self.site_residence = sqlObject[23]
#             self.site_validator = sqlObject[24]
#             self.site_pagerank = sqlObject[25]
#             self.site_lien_retour_url = sqlObject[26]
#             self.site_paypal_txn = sqlObject[27]
#             self.site_type_inscr = sqlObject[28]

#         def __repr__(self):
#             return f"{self.__class__.__name__}: {self.site_id} - {self.site_name}"

#         def __str__(self):
#             return f"{self.__class__.__name__}: " + \
#                 f"site_id = {self.site_id}, " + \
#                 f"site_name = {self.site_name}, " + \
#                 f"site_url = {self.site_url}, " + \
#                 f"site_mail = {self.site_mail}, " + \
#                 f"site_pr = {self.site_pr}, " + \
#                 f"site_pr_lastchecked = {self.site_pr_lastchecked}, " + \
#                 f"site_status = {self.site_status}, " + \
#                 f"site_dispmode = {self.site_dispmode}, " + \
#                 f"site_reg_date = {self.site_reg_date}, " + \
#                 f"site_valid_date = {self.site_valid_date}, " + \
#                 f"site_mail_date = {self.site_mail_date}, " + \
#                 f"site_dept = {self.site_dept}, " + \
#                 f"site_priority = {self.site_priority}, " + \
#                 f"site_ip = {self.site_ip}, " + \
#                 f"site_origine = {self.site_origine}, " + \
#                 f"site_clics = {self.site_clics}, " + \
#                 f"site_rss = {self.site_rss}, " + \
#                 f"site_lien_retour = {self.site_lien_retour}, " + \
#                 f"site_vis_retour = {self.site_vis_retour}, " + \
#                 f"site_vis_retours_06 = {self.site_vis_retours_06}, " + \
#                 f"site_is_officetourisme = {self.site_is_officetourisme}, " + \
#                 f"site_is_creteria = {self.site_is_creteria}, " + \
#                 f"site_is_1stpage = {self.site_is_1stpage}, " + \
#                 f"site_residence = {self.site_residence}, " + \
#                 f"site_validator = {self.site_validator}, " + \
#                 f"site_pagerank = {self.site_pagerank}, " + \
#                 f"site_lien_retour_url = {self.site_lien_retour_url}, " + \
#                 f"site_paypal_txn = {self.site_paypal_txn}, " + \
#                 f"site_type_inscr = {self.site_type_inscr}"
