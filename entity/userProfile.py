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
        

     #9 As a User Admin, I want to create a user profile so that I can store and manage essential information, such as user type about each user.
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

     #11 As a User Admin, I want to view the user profile so that I can know the user’s personal details.
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

     #13 As a User Admin, I want to update the user profile so that the latest user profile information is available.
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
                    
                    if cursor.rowcount > 0:
                         print("Update successful.")
                         return True
                    
          except Exception as e:
               print(f"Error occurred: {e}")
               return False
          finally:
               connection.close()


     #15 As a User Admin, I want to suspend user profiles so that I can remove all associated personal information and user types from the system, even if the user’s account remains active.
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


     #17 As a User Admin, I want to search for the user profile so that I can find the particular user profile.
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
