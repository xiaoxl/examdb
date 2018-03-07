import os
# import subprocess
# import errno
from pylatex.base_classes import Environment, Command, Container, LatexObject, UnsafeCommand, CommandBase
# from pylatex.base_classes.command import Arguments,CommandBase
from pylatex.package import Package
from pylatex.utils import dumps_list, rm_temp_dir, NoEscape
import pylatex.config as cf
# from json import *
import random
import json
import LatexSnippt

from parser import *

class EnvParts(Environment):
    _latex_name='parts'

class ComPart(CommandBase):
    _latex_name = 'part'

class ComQuestion(CommandBase):
    _latex_name='question'


class QuestionModule(Environment):
    _question=[]
    _solution=[]
    _part=[]
    _id=''
    _tag=[]
    _number_of_parts=0
    _points=[]
    _varchange=[]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def loadJSON(self,data):
        self._question=data["question"][:]
        self._part=data["part"][:]
        self._solution=data["solution"][:]
        self._number_of_parts=len(self._part)
        self._points=data["point"][:]
        self._varchange=data["varchange"][:]
        self._tag=data["tag"][:]
        self._id=data["_id"]



    def saveJSON(self,filepath):
        data={"_id":"",
              "question":[],
              "solution":[],
              "part":[],
              "point":[],
              "varchange":[],
              "tag":""}
        data["id"]=self._id
        data["question"]=self._question[:]
        data["solution"]=self._solution[:]
        data["part"]=self._part[:]
        data["tag"]=self._tag[:]
        data["varchange"]=self._varchange[:]
        data["point"]=self._points[:]
        with open(filepath,'w') as article:
            json.dump(data,article)


    def loadQuestion(self,filepath):
        # with open(filepath,'r') as datafile:
        #     data=datafile.read()
        # format_string=r'\question{}\begin\{parts\}{}\end\{parts\}'
        #
        # self._question=data["question"][:]
        # self._part=data["part"][:]
        # self._solution=data["solution"][:]
        # self._number_of_parts=len(self._part)
        # self._points=data["point"][:]
        # self._varchange=data["varchange"][:]
        # self._tag=data["tag"][:]
        # self._id=data["_id"]
        pass
        #
        # json_serial = "123"
        # my_json = {
        #     'settings': {
        #         "serial": json_serial,
        #         "status": '2',
        #         "ersion": '3',
        #     },
        #     'config': {
        #         'active': '4',
        #         'version': '5'
        #     }
        # }
        # print(json.dumps(my_json))


    def dumpQuestion(self):
        question=LatexSnippt()
        question.append('dadfasfas')
        return question


    def dumps(self):
        tempquestion='\n'.join(self._question)
        temppart=[]
        tempsolution=[]
        if self._number_of_parts!=0:
            for i in range(self._number_of_parts):
                temppart.append('\n'.join(self._part[i]))
                tempsolution.append('\n'.join(self._solution[i]))
        else:
            tempsolution.append('\n'.join(self._solution[0]))


        for i in range(len(self._varchange)):
            exec(self._varchange[i])
            temp=0
            exec('temp=var'+str(i))
            tempquestion=tempquestion.replace('_var'+str(i)+'_',str(temp))
            if self._number_of_parts>1:
                for j in range(self._number_of_parts):
                    temppart[j]=temppart[j].replace('_var'+str(i)+'_',str(temp))
                    tempsolution[j]=tempsolution[j].replace('_var'+str(i)+'_',str(temp))
            else:
                tempsolution[0]=tempsolution[0].replace('_var'+str(i)+'_',str(temp))

        if self._number_of_parts>1:
            s=Command('question').dumps()+ '%\n'+tempquestion+Command('begin', 'parts').dumps()+ '%\n'
            for i in range(self._number_of_parts):
                s=s+Command('part').dumps()+'['+str(self._points[i])+']' + '%\n'+temppart[i]
                s=s + '%\n'+Command('begin','solution').dumps() + '%\n'+tempsolution[i] + '%\n'+Command('end','solution').dumps() + '%\n'
            s=s+Command('end','parts').dumps() + '%\n'
        else:
            s=Command('question').dumps()+'['+str(self._points[0])+']' + '%\n'+tempquestion + '%\n'
            if self._number_of_parts!=0:
                s=s+temppart[0] + '%\n'
            s=s+Command('begin','solution').dumps() + '%\n'+tempsolution[0] + '%\n'+Command('end','solution').dumps() + '%\n'

        return s
