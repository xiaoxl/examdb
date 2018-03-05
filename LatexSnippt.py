# -*- coding: utf-8 -*-
"""
This module implements the class that deals with the full document.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

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

class EnvParts(Environment):
    _latex_name='parts'

class ComPart(CommandBase):
    _latex_name = 'part'

class ComQuestion(CommandBase):
    _latex_name='question'

class LatexSnippt(Environment):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dumps(self):

        content = self.dumps_content()
        if not content.strip() and self.omit_if_empty:
            return ''

        return content

class QuestionModule(LatexSnippt):
    _question=''
    _solution=[]
    _part=[]
    _id=''
    _tag=[]
    _number_of_parts=0
    _points=[]


    def getQuestion(self):
        return self._question

    def getNumberOfPart(self):
        return self._number_of_parts

    def getSolution(self):
        return self._solution

    def getParts(self):
        return self._part

    def loadJSON(self,data):
        self._question='\n'.join(data["question"])
        part=data["part"]
        solution=data["solution"]
        self._number_of_parts=len(part)
        self._points=data["point"]
        temppart=[]
        tempsolution=[]
        for i in range(self._number_of_parts):
            temppart.append('\n'.join(part[i]))
            tempsolution.append('\n'.join(solution[i]))
        self._part=temppart
        self._solution=tempsolution
        varchange=data["varchange"]
        tag=data["tag"]
        self._id=data["_id"]

        for i in range(len(varchange)):
            exec(varchange[i])
            temp=0
            exec('temp=var'+str(i))
            self._question=self._question.replace('_var'+str(i)+'_',str(temp))
            for j in range(self._number_of_parts):
                self._part[j]=self._part[j].replace('_var'+str(i)+'_',str(temp))
                self._solution[j]=self._solution[j].replace('_var'+str(i)+'_',str(temp))


    def saveJSON(self,filepath):
        data={"_id":"",
              "question":"",
              "solution":"",
              "part":"",
              "tag":""}
        data["id"]=self._id
        data["question"]=self._question
        data["solution"]=self._solution
        data["part"]=self._part
        data["tag"]=self._tag
        with open(filepath,'w') as article:
            json.dump(data,article)


    def loadQuestion(self,filepath):
        data={"_id":"",
              "question":"",
              "solution":"",
              "part":"",
              "tag":""}


    def dumpQuestion(self):
        question=LatexSnippt()
        question.append('dadfasfas')
        return question


    def dumps(self):
        if self._number_of_parts>1:
            s=Command('addpoints').dumps()+Command('question').dumps()+'['+str(sum(self._points))+']'+self._question+Command('begin', 'parts').dumps()
            for i in range(self._number_of_parts):
                s=s+Command('noaddpoints').dumps()+Command('part').dumps()+'['+str(self._points[i])+']'+self._part[i]
                s=s+Command('begin','solution').dumps()+self._solution[i]+Command('end','solution').dumps()
            s=s+Command('end','parts').dumps()
        else:
            s=Command('addpoints').dumps()+Command('question').dumps()+'['+str(self._points[0])+']'+self._question+self._part[0]+Command('begin','solution').dumps()+self._solution[0]+Command('end','solution').dumps()

        return s
