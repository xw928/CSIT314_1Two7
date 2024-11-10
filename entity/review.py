import pymysql

class review():

    def getDBConnection(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Kxw92803',
            'database': 'used_car_app',
            'cursorclass': pymysql.cursors.DictCursor
        }
        return pymysql.connect(**config)


    #46 As a Used Car Agent, I want to view my reviews so that I can understand my clients' feedback and improve my service accordingly.
    def getReview(self, agent_username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (agent_username,))
                agent_data = cursor.fetchone()
                
                if agent_data:
                    agent_id = agent_data['user_id']
                    sql = """
                    SELECT Rv.sender_id AS sender_id, Rv.review
                    FROM Review Rv
                    WHERE Rv.receiver_id = %s
                    """
                    cursor.execute(sql, (agent_id,))
                    reviews_info = cursor.fetchall()
                    return reviews_info
                else:
                    print("Error: Agent username not found.")
                    return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #77 As a Buyer, I want to view all Used Car Agent reviews so that I can evaluate their service.
    #85 As a Seller, I want to view all Used Car Agent reviews so that I can evaluate their service.
    def getAllAgentReview(self):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT Ua.username AS agent_username, Rv.review
                FROM Review Rv
                JOIN User_Account Ua ON Rv.receiver_id = Ua.user_id
                WHERE Ua.profile_id = 2
                """
                cursor.execute(sql)
                reviews_info = cursor.fetchall()
                return reviews_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #75 As a Buyer, I want to submit a review of my experience working with a Used Car Agent so that I can share my feedback about their service with others.
    #86 As a Seller, I want to submit a review of my experience working with a Used Car Agent so that I can share my feedback about their service with others.
    def submitReview(self, agent_username, sender_username, review):
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
                    sql = "INSERT INTO Review (sender_id, receiver_id, review) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (sender_id, agent_id, review))
                    connection.commit()
                    return True
                else:
                    return False
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


