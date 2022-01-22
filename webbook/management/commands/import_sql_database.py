from configparser import ConfigParser
from django.core.management.base import BaseCommand, CommandError

from webbook.models import Category, Localisation

from time import time
from os.path import abspath
from configparser import ConfigParser, ExtendedInterpolation
import pymysql

from .sql_object.sqlObject import *

SQL_TABLE_CATEGORY = "annu_cats"
SQL_TABLE_LOCALISATION = "annu_dept"
SQL_TABLE_SITE = "annu_site"

class Command(BaseCommand):
    help = 'Import Old Sql Database'

    def print_running(self, msg):
        self.stdout.write(f"[RUNNING] {msg}...", ending="\x1b[1K\r")

    def print_ok(self, msg):
        self.stdout.write(f"{self.style.SUCCESS('[OK]')} {msg}.")

    def check_models_empty(self, models):
        assert models.objects.count()==0, \
            CommandError(f"[ERROR] {models.__name__} is not empty !")

    def save_sqlModel(self, object):
        """
            @params:
            - object: Python object to save on
        """
        with self.connection.cursor() as cursor:
            self.print_running(f"Download '{object.SQL_KEY}' from Sql Database")
            dataList = []
            cursor.execute(f"select * from {object.SQL_KEY}")
            for data in cursor.fetchall():
                dataList.append(object.fromSql(data))
            self.print_ok(f"{len(dataList)} '{object.SQL_KEY}' from Sql Database downloaded")
            return dataList

    def handle(self, *args, **options):
        tic = time()
        # ------------------------------------
        # Verification
        # ------------------------------------
        # Check if PostGreSql models are empty
        self.print_running("Vérifying local Database is empty")
        for model in [
            Category, Localisation
        ]:
            self.check_models_empty(model)

        self.print_ok("Local Database is empty")

        # Read Sql Database Configuration file
        SQL_CONFIG_PATH = abspath("../config/sql_config.ini")
        self.print_running(f"SQL Configuration file '{SQL_CONFIG_PATH}' opening")
        try:
            sql_config = ConfigParser()
            sql_config._interpolation = ExtendedInterpolation()
            sql_config.read(SQL_CONFIG_PATH)
        except:
            CommandError(f"[ERROR] Impossible to open SQL Configuration file '{SQL_CONFIG_PATH}'")
        self.print_ok(f"SQL Configuration file '{SQL_CONFIG_PATH}' opened")

        # Check if Sql Database Connection is working
        self.print_running("SQL Network connection")
        try:
            self.connection = pymysql.connect(host=sql_config.get('sql_netLiens', 'address'),
                user=sql_config.get('sql_netLiens', 'user'),
                password=sql_config.get('sql_netLiens', 'password'),
                database=sql_config.get('sql_netLiens', 'databasename'),
                cursorclass=pymysql.cursors.DictCursor)
        except:
            raise CommandError(f"[ERROR] SQL Network Failed ({sql_config.get('sql_netLiens', 'address')}")
        self.print_ok("SQL Network established")

        # ------------------------------------
        # Preparation to import DB
        # ------------------------------------
        annu_cats = self.save_sqlModel(AnnuCat)
        annu_dept = self.save_sqlModel(AnnuDept)
        annu_site = self.save_sqlModel(AnnuSite)

        # ------------------------------------
        # End
        # ------------------------------------
        toc = time()
        self.stdout.write(f"Command finished in {int(round((toc - tic)))} s")
