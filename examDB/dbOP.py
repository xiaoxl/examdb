from tinydb import TinyDB
import re

class dbOp:


    def insertdata(self, filename,dbname):
        db=TinyDB(dbname+'.json')
        with open(filename,'r') as file:
            data=file.read()
        raw=re.split(r'\\begin{question}',data)
        num=len(raw)
        tags=[]
        course=''
        for i in range(num):
            if i>0:
                piece=re.split(r'\\end{question}',raw[i])
                question=piece[0]
                solutions=re.findall(r'begin{solution}(.*?)\\end{solution}',piece[1],re.S)
                item={"question": question,
                      "solutions": solutions,
                      "tags":tags,
                      "course":course,
                      }
                db.insert(item)