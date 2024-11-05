from entity.usedCarList import usedCarList

class searchAvailableUsedCarListController():
    
    def searchAvailableUsedCarList(self, field, value):
        return usedCarList().searchAvailableUsedCarList( field, value)