from numpy import random
from examdb.questionitem import QuestionItem

class ExItem:
    def __init__(self,listofquestionitems=None):
        self.stack=list(listofquestionitems)
        self.number_of=len(listofquestionitems)

    def get(self,id):
        return self.stack[id]

    def randget(self):
        id=random.choice(self.number_of)
        return self.get(id)


