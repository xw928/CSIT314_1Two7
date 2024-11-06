import pymysql

class rating():

    def getDBConnection(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
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


    def getAllAgentRating(self):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT Ua.username AS agent_username, Rt.rating
                FROM Rating Rt
                JOIN User_Account Ua ON Rt.receiver_id = Ua.user_id
                WHERE Ua.profile_id = 2
                """
                cursor.execute(sql)
                ratings_info = cursor.fetchall()
                print(ratings_info)
                return ratings_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    def submitRating(self, agent_username, sender_username, rating):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (agent_username, ))
                agent_data = cursor.fetchone()

                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (sender_username, ))
                sender_data = cursor.fetchone()

                # Check if both IDs were found
                if agent_data and sender_data:
                    agent_id = agent_data['user_id']
                    sender_id = sender_data['user_id']
                    sql = "INSERT INTO Rating (sender_id, receiver_id, rating) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (sender_id, agent_id, rating))
                    connection.commit()
                    return True
                else:
                    return False
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


