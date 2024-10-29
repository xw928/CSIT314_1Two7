import pymysql

class userProfile():

     def getDBConnection(self):
               config = {
                    'host': 'localhost',
                    'user': 'root',
                    'password': 'Kxw92803',
                    'database': 'used_car_app',
                    'cursorclass': pymysql.cursors.DictCursor
          }
               return pymysql.connect(**config)
        

     def createUserProfile(self, role, description):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    INSERT INTO User_Profile (role, description)
                    VALUES (%s, %s);
                    """
                    cursor.execute(sql, (role, description))
                    connection.commit()

                    return True
               
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()


     def viewUserProfile(self):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    SELECT * FROM User_Profile;
                    """
                    cursor.execute(sql)
                    profile_info = cursor.fetchall()
                    return profile_info
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()

     
     def updateUserProfile(self, rolename, new_rolename, new_description, new_status):        
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    UPDATE User_Profile
                    SET role = %s, description = %s, pf_status = %s
                    WHERE role = %s
                    """
                    cursor.execute(sql, (new_rolename, new_description, new_status, rolename))
                    connection.commit()
                    
                    return True
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()


     def suspendUserProfile(self, role):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    UPDATE User_Profile
                    SET pf_status = %s
                    WHERE role = %s
                    """
                    cursor.execute(sql, (0, role))    # 0 = False
                    connection.commit()
                    
                    return True
               
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()


     def searchUserProfile(self, role):
          connection = self.getDBConnection()
          try:
               with connection.cursor() as cursor:
                    sql = """
                    SELECT * FROM User_Profile
                    WHERE role = %s;
                    """
                    cursor.execute(sql, (role))
                    profile_info = cursor.fetchone()

                    if profile_info:
                         return profile_info  
                    else:
                         return None 
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()   
