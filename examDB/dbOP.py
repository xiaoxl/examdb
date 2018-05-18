from tinydb import TinyDB
import re
import difflib

class dbOp:

    @classmethod
    def insertdata(self, filename,dbname):
        db=TinyDB(dbname)
        with open(filename,'r') as file:
            data=file.read()
        raw=re.split(r'\\begin{question}',data)
        num=len(raw)
        tags=[]
        course="1"
        for i in range(num):
            if i>0:
                piece=re.split(r'\\end{question}',raw[i])
                question=piece[0]
                solutions=re.findall(r'begin{solution}(.*?)\\end{solution}',piece[1],re.S)
                item={"question": question,
                      "solutions": solutions,
                      "tags":tags,
                      "course":course
                      }
                db.insert(item)


    def compare(self,A,B):
        return difflib.SequenceMatcher(None, A, B).ratio()

    def compare_item(self,db,i,j):
        A=db.get(doc_id=i)["question"]
        B=db.get(doc_id=j)["question"]
        return dbOp.compare(self,A,B)

    @classmethod
    def findduplicate(dbname):
        db=TinyDB(dbname)
