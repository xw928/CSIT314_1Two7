from entity.usedCarList import usedCarList

class searchAgentUsedCarListController():
    
    def searchAgentUsedCarList(self, agent_username, field, value):
        return usedCarList().searchAgentUsedCarList(agent_username, field, value)