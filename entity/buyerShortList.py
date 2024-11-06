import pymysql

class buyerShortList():

    def getDBConnection(self):
        config = {
            'host': 'localhost',
            'user': 'root',
            'password': '1234',
            'database': 'used_car_app',
            'cursorclass': pymysql.cursors.DictCursor
        }
        return pymysql.connect(**config)
    
    def addBuyerShortList(self, buyer_username, car_id):
        try:
            # Establish DB connection
            with self.getDBConnection() as connection:
                with connection.cursor() as cursor:
                    # Insert into the Buyer_Shortlist table
                    insert_sql = """
                        INSERT INTO buyer_shortlist (buyer_username, car_id)
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

                    # Commit both operations
                    connection.commit()

                    # Check if the update was successful
                    if cursor.rowcount > 0:
                        print("Buyer successfully added to the shortlist and car shortlisted.")
                        return True

            return False

        except Exception as e:
            # If there is an error, print it and return False
            print(f"Error adding to shortlist: {e}")
            return False
        
    def viewShortListedCar(self, buyer_username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                # Get all car_id values from the buyer's shortlist
                cursor.execute("SELECT car_id FROM buyer_shortlist WHERE buyer_username = %s", (buyer_username,))
                shortlisted_cars = cursor.fetchall()

                if not shortlisted_cars:
                    print("No cars found in the shortlist for this buyer.")
                    return []

                # Extract the car_id values from the result
                car_ids = [car['car_id'] for car in shortlisted_cars]

                # Create a placeholder for the SQL IN clause (for a list of car_ids)
                placeholders = ', '.join(['%s'] * len(car_ids))

                # Query to get the car details from Used_Car_List for the shortlisted cars
                sql = f"""
                    SELECT ucl.*, ua.username AS agent_username
                    FROM Used_Car_List ucl
                    INNER JOIN User_Account ua 
                    ON ua.user_id = ucl.agent_id
                    WHERE ucl.car_id IN ({placeholders})
                    ORDER BY ucl.car_id
                """

                # Execute the query with the list of car_ids
                cursor.execute(sql, tuple(car_ids))
                car_info = cursor.fetchall()

                return car_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()

# def searchBuyerShortList(self, field, value, buyer_username): 
#     connection = self.getDBConnection()
#     try:
#         with connection.cursor() as cursor:
#             # First, get the car_ids from the buyer's shortlist
#             shortlist_sql = """
#             SELECT car_id 
#             FROM buyer_shortlist 
#             WHERE buyer_username = %s
#             """
#             cursor.execute(shortlist_sql, (buyer_username,))
#             shortlisted_car_ids = [row[0] for row in cursor.fetchall()]  # Get all the car_ids

#             if not shortlisted_car_ids:
#                 return []  # If no cars are in the shortlist for this buyer

#             # Now, use the shortlisted car ids to fetch the details from Used_Car_List
#             sql = ""
#             if field == 'price':
#                 sql = """
#                 SELECT 
#                     ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
#                     ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
#                     ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
#                 FROM 
#                     Used_Car_List ucl
#                 INNER JOIN 
#                     User_Account ua ON ucl.agent_id = ua.user_id
#                 WHERE
#                     ucl.car_id IN (%s) AND ucl.price <= %s AND ucl.car_status = 1
#                 ORDER BY 
#                     ucl.car_id;
#                 """
#                 # You need to pass the list of shortlisted car IDs and the price
#                 cursor.execute(sql, (', '.join(map(str, shortlisted_car_ids)), value))
#             elif field == 'agent_username':
#                 sql = """
#                 SELECT 
#                     ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
#                     ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
#                     ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
#                 FROM 
#                     Used_Car_List ucl
#                 INNER JOIN 
#                     User_Account ua ON ucl.agent_id = ua.user_id
#                 WHERE 
#                     ucl.car_id IN (%s) AND ua.username = %s AND ucl.car_status = 1
#                 ORDER BY 
#                     ucl.car_id;
#                 """
#                 cursor.execute(sql, (', '.join(map(str, shortlisted_car_ids)), value))
#             else:
#                 sql = f"""
#                 SELECT 
#                     ucl.car_id, ucl.car_type, ucl.year, ucl.brand, ucl.model, ucl.price,
#                     ucl.fuel_type, ucl.mileage, ucl.transmission, ucl.engine_size, 
#                     ucl.description, ucl.view, ucl.shortlisted, ua.username AS agent_username
#                 FROM 
#                     Used_Car_List ucl
#                 INNER JOIN 
#                     User_Account ua ON ucl.agent_id = ua.user_id
#                 WHERE 
#                     ucl.car_id IN (%s) AND {field} = %s AND ucl.car_status = 1
#                 ORDER BY 
#                     ucl.car_id;
#                 """
#                 cursor.execute(sql, (', '.join(map(str, shortlisted_car_ids)), value))

#             # Fetch and return the results
#             cars_info = cursor.fetchall()
#             return cars_info

#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return False
#     finally:
#         connection.close()



    
