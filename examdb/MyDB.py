from tinydb import TinyDB, Query
from tinydb.operations import delete
import re
import json
import difflib
from examdb.LatexSnippt import *

'''
Based on TinyDB.

To change to other databases only this file need to be updated.
'''

class MyDB(TinyDB):
    THRESHOLD=0.95

    def compare(self,A,B):
        return difflib.SequenceMatcher(None, A, B).ratio()

    def import_from_latex_btype(self,latex_filename,input_tags=[],input_course=""):
        ##### import from a latex file who contains \begin{question}\end{question} and \begin{solution}\end{solution}
        ##### can add tags and courses when using the function

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

    # def import_from_latex_qtype(self,latex_filename,input_tags=[],input_course=""):
    #     ##### import from a latex file who contains \question and \begin{solution}\end{solution}
    #     ##### can add tags and courses when using the function
    #
    #     with open(latex_filename,'r') as file:
    #         data=file.read()
    #     raw=re.split(r'\\question',data)
    #     num=len(raw)
    #     tags=input_tags
    #     course=input_course
    #     for i in range(num)[1:]:
    #         piece=re.split(r'\\begin{question}',raw[i])
    #         question=piece[0]
    #         solutions=re.findall(r'begin{solution}(.*?)\\end{solution}',piece[1],re.S)
    #         item={"question": question,
    #               "solutions": solutions,
    #               "tags":tags,
    #               "course":course
    #               }
    #         self.insert(item)

    def check_duplicate(self):
        ############ used to mark all duplicated entries
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
        ########### remove all entries which are marked as duplicated
        user=Query()
        self.remove(user.duplicate=="yes")

    def output_latex(self,json_list):
        ########### output a LatexSnippt which contains all questions and solutions from the json_list
        ########### the json_list don't have to be from the database, but it should have question entry (srtings) and solution entry (lists of strings)
        q=LatexSnippt()
        for question in json_list:
            q.append(Command('question'))
            q.append(NoEscape(question["question"]))
            for sol in question["solutions"]:
                with q.create(EnvSolutions()):
                    q.append(NoEscape(sol))
        return q.dumps()

    # def update_tags(self,):