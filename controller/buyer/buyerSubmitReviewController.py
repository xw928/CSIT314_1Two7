from entity.review import review

class buyerSubmitReviewController():

    def submitBuyerReview(self, agent_username, sender_username, buyer_review):
        return review().submitBuyerReview(agent_username, sender_username, buyer_review)