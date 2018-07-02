import re
import json
from numpy import random

r'''
The structure to store questions.
The problem words are stored in "master_question"(str) and "parts"(list).
Each item in "parts"(list) contains a "question"(str) section and a "solutions"(list) section.
So the problem should look like:
[master_question]: The main instruction of the question:
part1: [parts->question]: The instruction of the first part;
       [parts->solutions]: solution (method 1)
                           solution (method 2)
                           solution (method 3)
                           ...
part2: [parts->question]: The instruction of the first part;
       [parts->solutions]: solution (method 1)
                           solution (method 2)
                           solution (method 3)
                           ...
...
if there are only one part, the "part" label won't be shown.

"varchange"(list) is a list storing the randomized numbers in the problem. 
    The randomization is encouraged to use numpy.random since the package is already loaded. 

"tags"(list) and "course"(str) are labels to characterize the problem. "level"(int 1-5) is the difficulty. 

"packages"(list) and "packagesettings"(list) and "macros"(list) tell us how to run the code without any errors.

The item should look like this:
{"master_question": "main instructions",
"parts": [{"question": "instructions to part1",
          "solutions": ["solution1", "solution2", ...]},
          {"question": "instructions to part1",
          "solutions": ["solution1", "solution2", ...]},
          ...
          ],
"varchange": ["_var1_=1","_var2_=2",...],
"tags": ["tag1", "tag2", ...],
"course": "course",
"level": level,
"packages":[],
"packagesettings": [],
"macros":[]
}




The pattern part:
So far there are three default patterns:
1. \question
    instructions to questions
    \begin{parts}
    \part instructions.
    \begin{solution}
    (solution 1)..........
    (solution 2)..........
    ...........
    \end{solution}
    \part instructions.
    \begin{solution}
    (solution 1)..........
    (solution 2)..........
    ...........
    \end{solution}
    .....
2. \question
    instructions to questions
    \begin{parts}
    \part instructions.
    \begin{solution}
    ...........
    \end{solution}
    \begin{solution}
    ...........
    \end{solution}
    ...
    \part instructions.
    \begin{solution}
    ...........
    \end{solution}
    \begin{solution}
    ...........
    \end{solution}
    ...
    .....
3. \begin{exercise}
    instructions to questions
    \begin{parts}
    \part instructions.
    \begin{solution}
    ...........
    \end{solution}
    \begin{solution}
    ...........
    \end{solution}
    ...
    \part instructions.
    \begin{solution}
    ...........
    \end{solution}
    \begin{solution}
    ...........
    \end{solution}
    ...
    .....
    \end{exercise}

latetemplate: output the template

latexify: latexify will output a string with randomized numbers from "varchange" based on the template from latextemplate
latexify(1) will output a string with default value from "varchange". If there are no default value the randomized number will be used.

latexheader: output the header.
latexheader(List of QuestionItems): output the header for all, no duplicates.

comparequestion: compare latextemplate to others'
compareheader: compare latexheader to others'
'''


class QuestionItem:

    def __init__(self):
        # first are five basic contents
        self.master_question=""
        default_list={"question":"",
                      "solutions":[]}
        self.parts=[default_list]
        self.varchange=[]
        self.tags=[]
        self.course=""
        self.level=1
        # then the required packages and macros
        self.packages=[]
        self.packagesettings=[]
        self.macros=[]
        # last are flags and patterns
        self.setdefaultpattern()


    def __init__(self,input_data):
        # first are five basic contents
        self.master_question=input_data["master_question"]
        self.parts=list(input_data["parts"])
        self.varchange=list(input_data["varchange"])
        self.tags=sorted(input_data["tags"])
        self.course=input_data["course"]
        self.level=1
        # then the required packages and macros
        self.packages=sorted(input_data["packages"])
        self.packagesettings=sorted(input_data["packagesettings"])
        self.macros=sorted(input_data["macros"])
        # last are flags and patterns
        self.setdefaultpattern()

    def setdefaultpattern(self,environmenttoken='question'):
        self.pattern_whole='\\'+environmenttoken+'\n[master_question]\n<\\begin{parts}>[parts]<\\end{parts}>'
        self.pattern_parts=r'<\part[*]> [part]'+'\n\\begin{solution}[solutions]\n\\end{solution}\n'
        self.pattern_solutions='\n'+r'<\textbf{(Solution [*])}>'+' [solution]\n'

    def setdefaultpattern2(self,environmenttoken='question'):
        self.pattern_whole='\\'+environmenttoken+'\n[master_question]\n<\\begin{parts}>[parts]<\\end{parts}>'
        self.pattern_parts=r'<\part[*]> [part]'+'\n[solutions]\n'
        self.pattern_solutions=r'\begin{solution}'+'\n[solution]\n'+r'\end{solution}'+'\n'

    def setdefaultpattern3(self,environmenttoken='exercise'):
        self.pattern_whole=r'\begin{'+environmenttoken+'}'+'\n[master_question]\n<\\begin{parts}>[parts]<\\end{parts}>'+r'\end{'+environmenttoken+'}'
        self.pattern_parts=r'<\part[*]> [part]'+'\n[solutions]\n'
        self.pattern_solutions=r'\begin{solution}'+'\n[solution]\n'+r'\end{solution}'+'\n'

    def setpatternto_onepart(self):
        pattern_parts_now = re.sub('<(.*?)>', '', self.pattern_parts)
        return pattern_parts_now

    def setpatternto_morepart(self):
        pattern_parts_now = self.pattern_parts.replace("<","")
        pattern_parts_now = pattern_parts_now.replace(">","")
        return pattern_parts_now

    def setpatternto_onesol(self):
        pattern_solutions_now = re.sub('<(.*?)>', '', self.pattern_solutions)
        return pattern_solutions_now

    def setpatternto_moresol(self):
        pattern_solutions_now = self.pattern_solutions.replace("<","")
        pattern_solutions_now = pattern_solutions_now.replace(">","")
        return pattern_solutions_now

    def setpatternto_onepart_main(self):
        pattern_whole_now = re.sub('<(.*?)>', '', self.pattern_whole)
        return pattern_whole_now

    def setpatternto_morepart_main(self):
        pattern_whole_now = self.pattern_whole.replace("<","")
        pattern_whole_now = pattern_whole_now.replace(">","")
        return pattern_whole_now

    def latextemplate(self):
        num=len(self.parts)
        if num==1:  #if there is only one part, the "part" label won't be shown.
            pattern_whole_now = self.setpatternto_onepart_main()
            pattern_parts_now = self.setpatternto_onepart()
        else: #otherwise show "parts" labels
            pattern_whole_now = self.setpatternto_morepart_main()
            pattern_parts_now = self.setpatternto_morepart()

        current_question=pattern_whole_now.replace("[master_question]",self.master_question)

        current_part=""
        nofpart=len(self.parts)
        for j in range(nofpart):
            eachpart=self.parts[j]
            part_pattern=pattern_parts_now.replace("[part]",eachpart["question"])
            part_pattern=part_pattern.replace("[*]",str(j+1))
            nofsol=len(eachpart["solutions"])
            if nofsol==1:
                pattern_solution_now=self.setpatternto_onesol()
            else:
                pattern_solution_now=self.setpatternto_moresol()
            current_sol=""
            for i in range(nofsol):
                current_pattern=pattern_solution_now.replace("[solution]",eachpart["solutions"][i])
                current_pattern=current_pattern.replace("[*]",str(i+1))
                current_sol=current_sol+current_pattern
            part_pattern=part_pattern.replace("[solutions]",current_sol)
            current_part=current_part+part_pattern
        current_question=current_question.replace("[parts]",current_part)
        return current_question

    def latexify(self,flag=0):
        '''
        :flag: a flag to show whether to use the default value for randomized numbers. If no input, the numbers are random. If input anything other than 0 the default value will be used.
        :return:  a latex code string based on the "pattern".
        '''

        #first based on patterns generate the main body of the questions and solutions
        current_question=self.latextemplate()

        #then replace all variables by numbers based on varchange
        varlist=self.runthevariables(flag)
        numofvar=len(varlist)
        for i in range(numofvar):
            varname="_var"+str(i)+"_"
            current_question=current_question.replace(varname,str(varlist[i]))
        return current_question

    def runthevariables(self,flag=0):
        '''
        :param flag: if flag==0, randomize the code. if flag is not 0, use the default value.
        :return: a list of variable vaules.
        '''
        val=[]
        num=len(self.varchange)
        for i in range(num):
            varname='_var'+str(i)+'_'
            if flag==0:
                cont=self.varchange[i].split('|')[0]
            else:
                cont=re.sub(r"=(.*?)\|","=",self.varchange[i])
            exec(cont)
            val.append(eval(varname))
        return val


    def dump(self):
        res={"master_question": self.master_question,
             "parts":self.parts,
             "varchange":self.varchange,
             "tags":self.tags,
             "course":self.course,
             "level":self.level,
             "packages":self.packages,
             "packagesettings": self.packagesettings,
             "macros":self.macros}
        return res

    def dumps(self):
        res=self.dump()
        return json.dumps(res)

    def load(self,input_data):
        self.master_question=input_data["master_question"]
        self.parts=list(input_data["parts"])
        self.varchange=list(input_data["varchange"])
        self.tags=list(input_data["tags"])
        self.course=input_data["course"]
        self.level=input_data["level"]
        self.packages=list(input_data["packages"])
        self.packagesettings=list(input_data["packagesettings"])
        self.macros=list(input_data["macros"])

    def loads(self,input_json):
        dict=json.loads(input_json)
        self.load(dict)


    def latexheader(self,listofquestions_QI=[]):
        listofpackages=list([o.packages for o in listofquestions_QI])
        listofsettings=list([o.packagesettings for o in listofquestions_QI])
        listofmacros=list([o.macros for o in listofquestions_QI])
        currentpackages=list(self.packages)
        currentsettings=list(self.packagesettings)
        currentmacros=list(self.macros)
        for package in listofpackages:
            for p in package:
                if p not in currentpackages:
                    currentpackages.append(p)
        for setting in listofsettings:
            for s in setting:
                if s not in currentsettings:
                    currentsettings.append(s)
        for macro in listofmacros:
            for m in macro:
                if m not in currentmacros:
                    currentmacros.append(m)
        listp=sorted([r'\usepackage{' + temp +r'}' for temp in currentpackages])
        lists=sorted(currentsettings)
        listm=sorted(currentmacros)
        header='\n'.join(listp)+'\n'+'\n'.join(lists)+'\n'+'\n'.join(listm)
        return header

    def comparequestion(self,QuestionB):
        self.setdefaultpattern()
        QuestionB.setdefaultpattern()
        testA=self.latextemplate()
        testB=QuestionB.latextemplate()
        if testA==testB:
            return True
        else:
            return False

    def compareheader(self,QuestionB):
        self.setdefaultpattern()
        QuestionB.setdefaultpattern()
        testA=self.latexheader()
        testB=QuestionB.latexheader()
        if testA==testB:
            return True
        else:
            return False