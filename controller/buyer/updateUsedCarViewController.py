from entity.usedCarList import usedCarList

class updateUsedCarViewController():
    
    def updateUsedCarView(self, car_id):
        return usedCarList().updateUsedCarView(car_id)