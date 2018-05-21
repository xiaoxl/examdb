from tinydb import TinyDB, Query
from tinydb.operations import delete
import re
import json
import difflib
from examDB.latexSnippt import *


class MyDB(TinyDB):
    THRESHOLD=0.95

    def compare(self,A,B):
        return difflib.SequenceMatcher(None, A, B).ratio()

    def import_from_latex(self,latex_filename,input_tags=[],input_course=""):
        with open(latex_filename,'r') as file:
            data=file.read()
        raw=re.split(r'\\begin{question}',data)
        num=len(raw)
        tags=input_tags
        course=input_course
        for i in range(num)[1:]:
            piece=re.split(r'\\end{question}',raw[i])
            question=piece[0]
            solutions=re.findall(r'begin{solution}(.*?)\\end{solution}',piece[1],re.S)
            item={"question": question,
                  "solutions": solutions,
                  "tags":tags,
                  "course":course
                  }
            self.insert(item)

    def check_duplicate(self):
        try:
            self.update(delete("similarto"),all)
        except KeyError:
            pass
        num=len(self.all())
        for i in range(num):
            mainjson=self.all()[i]
            try:
                temp=mainjson["duplicate"]
            except KeyError:
                fullitem=json.dumps(mainjson)
                for j in range(num)[i+1:]:
                    currentjson=self.all()[j]
                    currentitem = json.dumps(currentjson)
                    if fullitem==currentitem:
                        self.update({"duplicate":"yes"},doc_ids=[currentjson.doc_id])

    def remove_duplicate(self):
        user=Query()
        self.remove(user.duplicate=="yes")

    def output_latex(self,json_list):
        q=LatexSnippt()
        for question in json_list:
            q.append(Command('question'))
            q.append(NoEscape(question["question"]))
            for sol in question["solutions"]:
                with q.create(EnvSolutions()):
                    q.append(NoEscape(sol))
        return q.dumps()