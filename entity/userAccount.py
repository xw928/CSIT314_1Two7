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
                    WHERE ua.username=%s AND ua.password=%s AND ua.acc_status = 1 AND up.pf_status = 1;
                    """
                    cursor.execute(sql,(username, password))
                    result = cursor.fetchone()

                    if result:
                         return result
                    else:
                         return None
              
          except Exception as e:
               print(e)
               return False
          finally:
               connection.close()

        

     def createUserAccount(self, username, password, profile_id):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO User_Account (username, password, profile_id)
                    VALUES (%s, %s, %s);
                    """
                    cursor.execute(sql, (username, password, profile_id))
                    connection.commit()

                    return True
               
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()



     def viewUserAccount(self):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    SELECT ua.*, up.*
                    FROM User_Account ua
                    JOIN User_Profile up ON ua.profile_id = up.profile_id
                    ORDER BY ua.user_id;
                    """
                    cursor.execute(sql)
                    user_info = cursor.fetchall()
                    return user_info
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()

     
     def updateUserAccount(self, username, new_username, new_password, new_role, new_status):
          
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    UPDATE User_Account
                    SET username = %s, password = %s, profile_id = %s, acc_status = %s
                    WHERE username = %s
                    """
                    cursor.execute(sql, (new_username, new_password, new_role, new_status, username))
                    connection.commit()

                    return True
               
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()


     def suspendUserAccount(self, username):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    UPDATE User_Account
                    SET acc_status = %s
                    WHERE username = %s
                    """
                    cursor.execute(sql, (0, username))    # 0 = False
                    connection.commit()
                    
                    return True
               
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()


     def searchUserAccount(self, username):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    SELECT ua.*, up.*
                    FROM User_Account ua
                    JOIN User_Profile up ON ua.profile_id = up.profile_id
                    WHERE username = %s;
                    """
                    cursor.execute(sql, (username))
                    user_info = cursor.fetchone()

                    if user_info:
                         return user_info  
                    else:
                         return None 
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()  


     def resetUserPassword(self, username, new_password):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    UPDATE User_Account
                    SET password = %s
                    WHERE username = %s;
                    """
                    cursor.execute(sql, (new_password, username))
                    connection.commit()
            
                    # Check if any rows were affected
                    if cursor.rowcount == 0:
                         print("No user found with the given username.")
                         return False
                    return True 
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close() 

