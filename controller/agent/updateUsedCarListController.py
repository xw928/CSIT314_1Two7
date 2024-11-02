from entity.usedCarList import usedCarList

class updateUsedCarListController():
    
    def updateUsedCarList(self, car_id, new_seller_username, new_car_type, new_brand, new_model, new_year, new_price, new_fuel_type, new_mileage, new_transmission, new_engine_size, new_description, new_status):
        return usedCarList().updateUsedCarList(car_id, new_seller_username, new_car_type, new_brand, new_model, new_year, new_price, new_fuel_type, new_mileage, new_transmission, new_engine_size, new_description, new_status)

