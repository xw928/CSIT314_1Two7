from entity.review import review

class buyerSubmitReviewController():

    def submitReview(self, agent_username, sender_username, buyer_review):
        return review().submitReview(agent_username, sender_username, buyer_review)