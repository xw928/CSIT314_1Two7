import pymysql

class buyerShortList():

    def getDBConnection(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'Kxw92803',
            'database': 'used_car_app',
            'cursorclass': pymysql.cursors.DictCursor
        }
        return pymysql.connect(**config)
    
    import pymysql


    #72 As a Buyer, I want to save the cars that I’m interested in on my shortlist so that I can easily access them again later.
    def addBuyerShortList(self, buyer_username, car_id):
        try:
            with self.getDBConnection() as connection:
                with connection.cursor() as cursor:
                    # Inserting the car into the Buyer_Shortlist table
                    insert_sql = """
                        INSERT INTO Buyer_Shortlist (buyer_username, car_id)
                        VALUES (%s, %s)
                    """
                    cursor.execute(insert_sql, (buyer_username, car_id))

                    # If insertion is successful, increment the shortlisted count in Used_Car_list
                    update_sql = """
                        UPDATE Used_Car_List
                        SET shortlisted = shortlisted + 1
                        WHERE car_id = %s
                    """
                    cursor.execute(update_sql, (car_id,))
                    connection.commit()

                    if cursor.rowcount > 0:
                        print("Buyer successfully added to the shortlist and car shortlisted.")
                        return True
                    return False

        except pymysql.err.IntegrityError as e:
            if "Duplicate entry" in str(e) and "for key" in str(e):
                print(f"Error: Car {car_id} is already shortlisted by buyer {buyer_username}.")
                return False
            else:
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise


    #73 As a Buyer, I want to view the car in my shortlist so that I can view information of the shortlisted cars that I’m interested in.   
    def viewShortListedCar(self, buyer_username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT car_id FROM buyer_shortlist WHERE buyer_username = %s", (buyer_username,))
                shortlisted_cars = cursor.fetchall()

                if not shortlisted_cars:
                    return []

                car_ids = [car['car_id'] for car in shortlisted_cars]
                placeholders = ', '.join(['%s'] * len(car_ids))

                sql = f"""
                    SELECT ucl.*, ua.username AS agent_username
                    FROM Used_Car_List ucl
                    INNER JOIN User_Account ua 
                    ON ua.user_id = ucl.agent_id
                    WHERE ucl.car_id IN ({placeholders}) AND ucl.car_status = 1
                    ORDER BY ucl.car_id
                """

                cursor.execute(sql, tuple(car_ids))
                cars_info = cursor.fetchall()
                return cars_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()


    #74 As a Buyer, I want to search for the cars I have shortlisted so that I can quickly find and review the details of my preferred options using keywords.
    def searchBuyerShortList(self, buyer_username, field, value):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM User_Account WHERE username = %s", (buyer_username,))
                buyer_data = cursor.fetchone()

                if buyer_data:

                    sql = ""
                    # Filter based on the specified field and value, within the buyer's shortlist
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
                        INNER JOIN 
                            buyer_shortlist bs ON bs.car_id = ucl.car_id
                        WHERE 
                            bs.buyer_username = %s AND ucl.price <= %s AND ucl.car_status = 1
                        ORDER BY 
                            ucl.car_id;
                        """
                    elif field == 'agent_username':
                        sql = """
                        SELECT 
                            ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
                            ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, ucl.car_status,
                            ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
                        FROM 
                            Used_Car_List ucl
                        INNER JOIN 
                            User_Account ua ON ucl.agent_id = ua.user_id
                        INNER JOIN 
                            buyer_shortlist bs ON bs.car_id = ucl.car_id
                        WHERE 
                            bs.buyer_username = %s AND ua.username = %s AND ucl.car_status = 1
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
                        INNER JOIN 
                            buyer_shortlist bs ON bs.car_id = ucl.car_id
                        WHERE 
                            bs.buyer_username = %s AND {field} = %s AND ucl.car_status = 1
                        ORDER BY 
                            ucl.car_id;
                        """
                    
                    cursor.execute(sql, (buyer_username, value))
                    cars_info = cursor.fetchall()

                    return cars_info
                else:
                    print("Error: Buyer username not found.")
                    return None

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()





    
