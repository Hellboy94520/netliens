from os.path import abspath, exists
from configparser import ConfigParser, ExtendedInterpolation
import pymysql

class SqlPointer:
    def __init__(self, sqlConfig):
        # Check if Sql Database Connection is working
        try:
            self.connection = pymysql.connect(host=sqlConfig.get('sql_netLiens', 'address'),
                user=sqlConfig.get('sql_netLiens', 'user'),
                password=sqlConfig.get('sql_netLiens', 'password'),
                database=sqlConfig.get('sql_netLiens', 'databasename'),
                cursorclass=pymysql.cursors.DictCursor)
        except:
            raise Exception(f"[ERROR] SQL Network Failed ({sqlConfig.get('sql_netLiens', 'address')}")

    def getSqlModel(self, sql_table_name: str):
        """
            @params:
            - sql_table_name: Python object to save on
        """
        with self.connection.cursor() as cursor:
            # dataList = []
            cursor.execute(f"select * from `{sql_table_name}`")
            return cursor.fetchall()


    def runSqlCommand(self, sql_command: str):
        with self.connection.cursor() as cursor:
            # dataList = []
            cursor.execute(sql_command)
            return cursor.fetchall()
