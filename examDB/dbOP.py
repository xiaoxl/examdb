from tinydb import TinyDB,Query
from tinydb.operations import delete
import re
import difflib
import json


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

    @classmethod
    def compare(self,A,B):
        return difflib.SequenceMatcher(None, A, B).ratio()

    def compare_item(self,db,i,j):
        A=db.get(doc_id=i)["question"]
        B=db.get(doc_id=j)["question"]
        return dbOp.compare(self,A,B)

    @classmethod
    def CheckDuplicate(cls,db):
        try:
            db.update(delete("similarto"),all)
        except KeyError:
            pass
        num=len(db.all())
        for i in range(num):
            fullitem=json.dumps(db.all()[i])
            for j in range(num)[i+1:]:
                currentitem = json.dumps(db.all()[j])
                if fullitem==currentitem:
                    db.update({"duplicate":"yes"},doc_ids=[db.all()[j].doc_id])

    @classmethod
    def RemoveDuplicate(cls,db):
        User=Query()
        db.remove(User.duplicate=="yes")

    @classmethod
    def CheckSimilarity(cls,db):
        threshold=0.95
        num=len(db.all())
        flag="correct"
        for i in range(num):
            myid=db.all()[i].doc_id
            mainitem=(str)(db.all()[i]["question"])
            try:
                sim=db.all()[i]["similarto"]
            except KeyError:
                db.update({"similarto":myid},doc_ids=[myid])
                sim=myid
            simitem=(str)(db.get(doc_id=sim)["question"])
            if not (sim<myid)&(dbOp.compare(mainitem, simitem)>threshold):
                for j in range(num)[i+1:]:
                    currentid=db.all()[j].doc_id
                    currentmainitem = (str)(db.all()[j]["question"])
                    dif=dbOp.compare(mainitem,currentmainitem)
                    if dif>threshold:
                        db.update({"similarto":myid},doc_ids=[currentid])



