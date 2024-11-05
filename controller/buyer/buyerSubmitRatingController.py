from entity.rating import rating

class buyerSubmitRatingController():

    def submitBuyerRating(self, agent_username, sender_username, buyer_rating):
        return rating().submitBuyerRating(agent_username, sender_username, buyer_rating)