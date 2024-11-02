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



    def viewUsedCarList(self, agent_username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (agent_username,))
                agent_data = cursor.fetchone()
                
                if agent_data:
                    agent_id = agent_data['user_id']
                    sql = """
                    SELECT 
                        ucl.*, 
                        agent.username AS agent_username, 
                        seller.username AS seller_username
                    FROM 
                        Used_Car_List ucl
                    JOIN 
                        User_Account agent ON ucl.agent_id = agent.user_id
                    JOIN 
                        User_Account seller ON ucl.seller_id = seller.user_id
                    WHERE 
                        ucl.agent_id = %s
                    ORDER BY 
                        ucl.car_id;
                    """
                    cursor.execute(sql, (agent_id,))
                    car_info = cursor.fetchall()
                    return car_info
                else:
                    print("Error: Agent username not found.")
                    return None

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()

     
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
                    print("Error: New seller username does not exist or is not a seller (profile_id = 4).")
                    return False
                
                new_seller_id = seller['user_id']

                # Check if car_id exists
                cursor.execute("SELECT car_id FROM Used_Car_List WHERE car_id = %s", (car_id,))
                if cursor.fetchone() is None:
                    print("Error: car_id does not exist.")
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
                    print("Update successful.")
                    return True
                else:
                    print("No rows were updated. Check if values are the same as current ones.")
                    return False
            
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


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


    def searchUsedCarList(self, agent_username, field, value):
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
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
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
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
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
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
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
