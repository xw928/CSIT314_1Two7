from entity.rating import rating

class getRatingController():

    def getRating(self, agent_username):
        return rating().getRating(agent_username)