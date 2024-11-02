from entity.usedCarList import usedCarList

class createUsedCarListController():

    def createUsedCarList(self, agent_username, seller_username, car_type, brand, model, year, price, fuel_type, mileage, transmission, engine_size, description):
        return usedCarList().createUsedCarList(agent_username, seller_username, car_type, brand, model, year, price, fuel_type, mileage, transmission, engine_size, description)

