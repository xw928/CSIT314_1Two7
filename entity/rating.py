import pymysql

class rating():

    def getDBConnection(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Kxw92803',
            'database': 'used_car_app',
            'cursorclass': pymysql.cursors.DictCursor
        }
        return pymysql.connect(**config)


    def getRating(self, agent_username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (agent_username,))
                agent_data = cursor.fetchone()
                
                if agent_data:
                    agent_id = agent_data['user_id']
                    sql = """
                    SELECT Rt.sender_id AS sender_id, Rt.rating
                    FROM Rating Rt
                    WHERE Rt.receiver_id = %s
                    """
                    cursor.execute(sql, (agent_id,))
                    ratings_info = cursor.fetchall()
                    return ratings_info
                else:
                    print("Error: Agent username not found.")
                    return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()





