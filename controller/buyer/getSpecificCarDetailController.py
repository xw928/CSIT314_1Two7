from entity.usedCarList import usedCarList

class getSpecificCarDetailController():
    
    def getSpecificCarDetail(self, car_id):
        return usedCarList().getSpecificCarDetail(car_id)