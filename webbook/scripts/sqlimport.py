from webbook.scripts.sqlconnection import *
from webbook.scripts.category import CategoryManager
from webbook.scripts.localisation import LocalisationManager
from webbook.scripts import log as Log
import os

def readSqlTable(sqlConnection: SqlConnection, sql_table_name: str):
    # Variables
    l_table = {}

    # Get all annu_cat
    l_table_sql = sqlConnection.set_command(f"SELECT * FROM `{sql_table_name}`")
    for table in l_table_sql:
        # Check doubles annu_cat
        if l_table.get(table[0], None) is not None:
            return Log.fatal(__name__, f"{sql_table_name} with id={table[0]} already exist !")

        # Save Table
        l_table[table[0]] = table

    # Check after get data
    if len(l_table) == 0:
        Log.fatal(__name__, f"No {sql_table_name} find from SQL Database !")
    if len(l_table) != len(l_table_sql):
        Log.fatal(__name__, f"Impossible to get all {sql_table_name} from SQL Database ! \
            Get {len(l_table)} {sql_table_name} instead of {len(l_table_sql)}")

    Log.info(f"Get {len(l_table)} {sql_table_name} from SQL Database !")
    return l_table

def run():
    Log.info("Start SQL importation...")
    # -----------------------------------
    # Read config file for SQL
    # -----------------------------------
    l_sqlConfig_filename = "sql_config.ini"
    l_sqlConfig_folder = "/etc"
    l_sqlConfig_file = f"{l_sqlConfig_folder}/{l_sqlConfig_filename}"
    import configparser
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()
    if not settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), f"{l_sqlConfig_file}")):
        Log.fatal("main", f"Impossible to open {l_sqlConfig_file} !")
        exit(1)
    Log.info(f"File {l_sqlConfig_file} has been load !")


    # -----------------------------------
    # Connexion to SQL Database
    # -----------------------------------
    NetLiensSqlNetwork = SqlConnection(settings.get('sql_netLiens', 'address'),
                                    settings.get('sql_netLiens', 'user'),
                                    settings.get('sql_netLiens', 'password'),
                                    settings.get('sql_netLiens', 'databasename'))
    Log.info(f"SQL Database has been set !")


    # # -----------------------------------
    # # Start conversion
    # # -----------------------------------
    Log.info("*********************************")
    Log.info("Conversion starting...")

    Log.info("Category starting...")
    l_annuCat_list = readSqlTable(NetLiensSqlNetwork, CategoryManager.sql_table_name)
    l_categoryManager = CategoryManager()
    l_categoryManager.createCategoryFromSql(l_annuCat_list)
    Log.info("Category conversion [OK]\n")

    Log.info("Localisation Conversion starting...")
    l_annuDept_list = readSqlTable(NetLiensSqlNetwork, LocalisationManager.sql_table_name)
    l_localisationManager = LocalisationManager()
    Log.info("Localisation conversion [OK]\n")


    Log.info("Conversion [OK]")
    Log.info("*********************************")
