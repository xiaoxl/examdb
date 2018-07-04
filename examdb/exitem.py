from numpy import random
from examdb.questionitem import QuestionItem


class ExItem:
    def __init__(self,listofquestionitems=None):
        if listofquestionitems == None:
            listofquestionitems=[]
        self.stack=list(listofquestionitems)
        self.number_of=len(listofquestionitems)

    def get(self,id):
        return self.stack[id]

    def randget(self):
        id=random.choice(self.number_of)
        return self.get(id)


    def append(self,QI):
        self.stack.append(QI)
        self.number_of=self.number_of+1

    def remove(self,id):
        self.stack.remove(self.get(id))
        self.number_of=self.number_of-1

    def setdefaultpattern(self):
        for i in self.stack:
            i.setdefaultpattern()

    def setpattern(self,id=1):
        for i in self.stack:
            i.setpattern(id)
