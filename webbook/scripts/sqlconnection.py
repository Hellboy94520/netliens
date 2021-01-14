import pymysql

class SqlConnection:
    def __init__(self, pHost, pUser, pPassword, pDatabase):
        self.Database = pDatabase
        try:
            self.conn = pymysql.connect(host=pHost, user=pUser, password=pPassword, database=pDatabase)
            self.cursor = self.conn.cursor()

        except pymysql.Error as e:
            print(e)
    
    def __del__(self):
        print("Delete SqlConnection instance from database \'"+self.Database+"\'")
        self.conn.close()

    def set_command(self, pText):
        self.cursor.execute(str(pText))
        return self.cursor.fetchall()

