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
    
    import pymysql

    def addBuyerShortList(self, buyer_username, car_id):
        try:
            # Establish DB connection
            with self.getDBConnection() as connection:
                with connection.cursor() as cursor:
                    # Try inserting the car into the Buyer_Shortlist table
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

                    # Commit both operations
                    connection.commit()

                    # Check if the update was successful
                    if cursor.rowcount > 0:
                        print("Buyer successfully added to the shortlist and car shortlisted.")
                        return True
                    return False

        except pymysql.err.IntegrityError as e:
            # Check if the error is due to a duplicate entry for the combination of buyer_username and car_id
            if "Duplicate entry" in str(e) and "for key" in str(e):
                print(f"Error: Car {car_id} is already shortlisted by buyer {buyer_username}.")
                return False
            else:
                # Raise any other types of IntegrityErrors or exceptions
                raise
        except Exception as e:
            # Catch all other exceptions
            print(f"Unexpected error: {e}")
            raise

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

    def searchBuyerShortList(self, field, value, buyer_username):
        connection = self.getDBConnection()
        try:
            with connection.cursor() as cursor:
                # Get shortlisted cars for the given buyer (ensure buyer_username is in session)
                shortlist_sql = """
                SELECT car_id
                FROM buyer_shortlist
                WHERE buyer_username = %s
                """
                cursor.execute(shortlist_sql, (buyer_username,))
                shortlisted_car_ids = [row[0] for row in cursor.fetchall()]

                if not shortlisted_car_ids:
                    return []  # No cars in the shortlist for this buyer

                # Ensure that shortlisted_car_ids are available and valid
                shortlisted_car_ids_str = ', '.join(map(str, shortlisted_car_ids))

                # Construct the base SQL query to search for cars that are in the shortlist and match the criteria
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
                    ucl.car_id IN ({shortlisted_car_ids_str})  -- Filter by shortlisted cars only
                    AND ucl.car_status = 1  -- Ensure the car is active
                """

                # Apply search filters based on the field (e.g., car_type, brand, price, etc.)
                if field == 'price':
                    sql += " AND ucl.price <= %s"
                    cursor.execute(sql, (value,))
                elif field == 'agent_username':
                    sql += " AND LOWER(ua.username) = LOWER(%s)"
                    cursor.execute(sql, (value.lower(),))
                elif field in ['car_type', 'brand', 'model']:  # Apply filters for other fields
                    sql += f" AND LOWER(ucl.{field}) LIKE LOWER(%s)"
                    cursor.execute(sql, (f"%{value.lower()}%",))

                # Fetch the results
                cars_info = cursor.fetchall()

                if not cars_info:
                    return []  # No cars match the criteria

                return cars_info

        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        finally:
            connection.close()





    
