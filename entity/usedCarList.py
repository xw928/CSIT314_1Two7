import pymysql

class usedCarList():

    def getDBConnection(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Kxw92803',
            'database': 'used_car_app',
            'cursorclass': pymysql.cursors.DictCursor
        }
        return pymysql.connect(**config)
        

    #40 As a Used Car Agent, I want to create a used car listing so that buyers can view the used car's information.
    def createUsedCarList(self, agent_username, seller_username, car_type, brand, model, year, price, fuel_type, mileage, transmission, engine_size, description):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                # Get agent and seller IDs
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (agent_username, ))
                agent_id = cursor.fetchone()
                
                # Get seller ID and check if profile_id is 4 (seller role)
                cursor.execute("SELECT user_id, profile_id FROM User_Account WHERE username = %s", (seller_username, ))
                seller_data = cursor.fetchone()
                
                # Check if both IDs were found
                if agent_id and seller_data and seller_data['profile_id'] == 4:
                    sql = """
                    INSERT INTO Used_Car_List (car_type, brand, model, year, price, fuel_type, mileage, transmission, engine_size, description, agent_id, seller_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(sql, (car_type, brand, model, year, price, fuel_type, mileage, transmission, engine_size, description, agent_id['user_id'], seller_data['user_id']))
                    connection.commit()
                    return True
                else:
                    return False
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #41 As a Used Car Agent, I want to view used car listings I put up so that I can stay updated on their status.
    #81 As a Seller, I want to view all my used cars so that I can easily manage and track the used cars I own.
    #83 As a Seller, I want to track the number of views on my used car so that I can gauge the level of interest from potential buyers
    #84 As a Seller, I want to track how many times my used cars are shortlisted so that I can know which cars are generating the most interest.
    def viewUsedCarList(self, username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id, profile_id FROM User_Account WHERE username = %s", (username,))
                user_data = cursor.fetchone()

                sql = ''

                if user_data['profile_id'] == 4:

                    sql = """
                        SELECT ucl.*, ua.username AS agent_username
                        FROM Used_Car_List ucl
                        INNER JOIN User_Account ua 
                        ON ua.user_id = ucl.agent_id
                        WHERE seller_id = %s
                        ORDER BY ucl.car_id
                    """
                
                elif user_data['profile_id'] == 2:

                    sql = """
                        SELECT ucl.*, ua.username AS seller_username
                        FROM Used_Car_List ucl
                        INNER JOIN User_Account ua 
                        ON ua.user_id = ucl.seller_id
                        WHERE agent_id = %s
                        ORDER BY ucl.car_id
                    """
                else:
                    print("Error: Username not found.")
                    return None
            
                cursor.execute(sql, (user_data['user_id'],))
                cars_info = cursor.fetchall()
                return cars_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #42 As a Used Car Agent, I want to update used car listings so that the latest used car information is available.
    def updateUsedCarList(self, car_id, new_seller_username, new_car_type, new_brand, new_model, new_year, new_price, new_fuel_type, new_mileage, new_transmission, new_engine_size, new_description, new_status):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                # Check if the new seller exists and has profile_id = 4 (seller)
                cursor.execute("""
                    SELECT user_id FROM User_Account
                    WHERE username = %s AND profile_id = 4
                """, (new_seller_username,))
                
                seller = cursor.fetchone()
                if not seller:
                    return False
                
                new_seller_id = seller['user_id']

                # Check if car_id exists
                cursor.execute("SELECT car_id FROM Used_Car_List WHERE car_id = %s", (car_id,))
                if cursor.fetchone() is None:
                    return False
                
                # Update the Used_Car_List table with the new details
                sql = """
                    UPDATE Used_Car_List
                    SET 
                        car_type = %s,
                        brand = %s,
                        model = %s,
                        year = %s,
                        price = %s,
                        fuel_type = %s,
                        mileage = %s,
                        transmission = %s,
                        engine_size = %s,
                        description = %s,
                        car_status = %s,
                        seller_id = %s
                    WHERE car_id = %s
                """
                cursor.execute(sql, (new_car_type, new_brand, new_model, new_year, new_price, new_fuel_type, new_mileage, new_transmission, new_engine_size, new_description, new_status, new_seller_id, car_id))
                connection.commit()
                
                # Confirm if rows were affected
                if cursor.rowcount > 0:
                    return True
                else:
                    return False
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #43 As a Used Car Agent, I want to delete used car listings so that I can remove sold used cars or sellers change their minds from the database。
    def deleteUsedCarList(self, car_id):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM Used_Car_List
                WHERE car_id = %s;
                """
                cursor.execute(sql, (car_id,))   
                connection.commit()
                
                return True
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #44 As a Used Car Agent, I want to search for used car listings so that I can efficiently find a suitable used car that matches the buyer.
    def searchAgentUsedCarList(self, agent_username, field, value):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (agent_username,))
                agent_data = cursor.fetchone()
                
                if agent_data:
                    agent_id = agent_data['user_id']

                    sql = ""
                    if field == 'price':
                        sql = """
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS seller_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.seller_id = ua.user_id
                        WHERE 
                            ucl.agent_id = %s AND ucl.price <= %s
                        ORDER BY 
                            ucl.car_id;
                        """
                    elif field == 'seller_username':
                        sql = """
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS seller_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.seller_id = ua.user_id
                        WHERE 
                            ucl.agent_id = %s AND ua.username = %s
                        ORDER BY 
                            ucl.car_id;
                        """
                    else:
                        sql = f"""
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS seller_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.seller_id = ua.user_id
                        WHERE 
                            ucl.agent_id = %s AND {field} = %s
                        ORDER BY 
                            ucl.car_id;
                        """
                    
                    cursor.execute(sql, (agent_id, value))
                    cars_info = cursor.fetchall()
                    return cars_info
                
                else:
                    print("Error: Agent username not found.")
                    return None

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()
            

    #70 As a Buyer, I want to search for used cars available for sale so that I can explore different car options using keywords.
    def searchAvailableUsedCarList(self, field, value):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:               
                sql = ""
                if field == 'price':
                    sql = """
                    SELECT 
                        ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                        ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
                        ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                    FROM 
                        Used_Car_List ucl
                    INNER JOIN 
                        User_Account ua ON ucl.agent_id = ua.user_id
                    WHERE                   
                        ucl.price <= %s AND ucl.car_status = 1
                    ORDER BY 
                        ucl.car_id;
                    """
                elif field == 'agent_username':
                    sql = """
                    SELECT 
                        ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                        ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
                        ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                    FROM 
                        Used_Car_List ucl
                    INNER JOIN 
                        User_Account ua ON ucl.agent_id = ua.user_id
                    WHERE 
                        ua.username = %s AND ucl.car_status = 1
                    ORDER BY 
                        ucl.car_id;
                    """
                else:
                    sql = f"""
                    SELECT 
                        ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                        ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
                        ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                    FROM 
                        Used_Car_List ucl
                    INNER JOIN 
                        User_Account ua ON ucl.agent_id = ua.user_id
                    WHERE 
                        {field} = %s AND ucl.car_status = 1
                    ORDER BY 
                        ucl.car_id;
                    """

                cursor.execute(sql, (value))
                cars_info = cursor.fetchall()

                return cars_info
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


#71 As a Buyer, I want to view the used car listings available for sale so that I can access used car information.
    def getAvailableUsedCarList(self):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:

                sql = """
                    SELECT ucl.*, ua.username AS agent_username
                    FROM Used_Car_List ucl
                    INNER JOIN User_Account ua 
                    ON ua.user_id = ucl.agent_id
                    WHERE car_status = 1
                    ORDER BY ucl.car_id
                """
            
                cursor.execute(sql)
                cars_info = cursor.fetchall()
                return cars_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()
            

    #82 As a Seller, I want to search my used car listings so that I can easily find my used car using keywords
    def searchSellerUsedCarList(self,seller_username, field, value):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (seller_username,))
                seller_data = cursor.fetchone()
                
                if seller_data:
                    seller_id = seller_data['user_id']
                    sql = ""
                    if field == 'price':
                        sql = """
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.agent_id = ua.user_id
                        WHERE 
                            ucl.seller_id = %s AND ucl.price <= %s
                        ORDER BY 
                            ucl.car_id;
                        """
                    elif field == 'seller_username':
                        sql = """
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.agent_id = ua.user_id
                        WHERE 
                            ucl.seller_id = %s AND ua.username = %s
                        ORDER BY 
                            ucl.car_id;
                        """
                    else:
                        sql = f"""
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.agent_id = ua.user_id
                        WHERE 
                            ucl.seller_id = %s AND {field} = %s
                        ORDER BY 
                            ucl.car_id;
                        """
                    
                    cursor.execute(sql, (seller_id, value))
                    cars_info = cursor.fetchall()
                    return cars_info
                else:
                    print("Error: Seller Username not found.")
                    return None

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()



    # for update view +1
    def updateUsedCarView(self, car_id):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE Used_Car_list
                SET view = view + 1
                WHERE car_id = %s
                """
                cursor.execute(sql, (car_id,))
                connection.commit()

            if cursor.rowcount > 0:
                print("Update successful.")
                return True

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()

