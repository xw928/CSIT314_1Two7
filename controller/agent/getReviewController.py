from entity.review import review

class getReviewController():

    def getReview(self, agent_username):
        return review().getReview(agent_username)