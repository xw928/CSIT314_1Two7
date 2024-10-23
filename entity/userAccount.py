import pymysql

class userAccount():

    def getDBConnection(self):
            config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'Kxw92803',
                'database': 'used_car_app',
                'cursorclass': pymysql.cursors.DictCursor
        }
            return pymysql.connect(**config)


    def verifyAccount(self, username, password):

        connection = self.getDBConnection()

        try:
             with connection.cursor() as cursor:
                sql = """
                SELECT ua.*, up.*
                FROM User_Account ua
                JOIN User_Profile up ON ua.profile_id = up.profile_id
                WHERE ua.username=%s AND ua.password=%s 
                """
                cursor.execute(sql,(username, password))
                result = cursor.fetchone()

                if result and result['acc_status'] == 1 and result['pf_status'] == 1:
                     user_info = {
                          'username': result['username'],
                          'role': result['role']
                     }
                     return user_info
                else:
                     return None
        finally:
            connection.close()
