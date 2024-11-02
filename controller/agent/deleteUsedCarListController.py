from entity.usedCarList import usedCarList

class deleteUsedCarListController():

    def deleteUsedCarList(self, car_id):
        return usedCarList().deleteUsedCarList(car_id)