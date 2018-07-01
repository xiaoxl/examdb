from tinydb import TinyDB, Query
from tinydb.operations import delete
import tinydb
import re
import json
# import difflib
from examdb.LatexSnippt import *
import random
from pylatex.utils import NoEscape


'''
Based on TinyDB.

To change to other databases only this file need to be updated.
'''


class QuestionItem():
    '''
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

    "tags"(list) and "course"(str) are labels to characterize the problem.

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
    "packages":[],
    "packagesettings": [],
    "macros":[]
    }
    '''

    def __init__(self):
        # first are five basic contents
        self.master_question=""
        default_list={"question":"",
              "solutions":[]}
        self.parts=[default_list]
        self.varchange=[]
        self.tags=[]
        self.course=""
        # then the required packages and macros
        self.packages=[]
        self.packagesettings=[]
        self.macros=[]
        # last are flags and patterns
        self.flag=0             #flag=0 means the variable will be randomized. flag~=0 means the variable will use the default value.
        self.setdefaultpattern()

    def __init__(self,input_data):
        # first are five basic contents
        self.master_question=input_data["master_question"]
        self.parts=list(input_data["parts"])
        self.varchange=list(input_data["varchange"])
        self.tags=list(input_data["tags"])
        self.course=input_data["course"]
        # then the required packages and macros
        self.packages=[]
        self.packagesettings=[]
        self.macros=[]
        # last are flags and patterns
        self.flag=0             #flag=0 means the variable will be randomized. flag~=0 means the variable will use the default value.
        self.setdefaultpattern()

    def setdefaultpattern(self):
        self.pattern_whole=r'\question'+'\n[master_question]\n\\begin{parts}[parts]\\end{parts}'
        self.pattern_parts=r'\part[*] [part]'+'\n\\begin{solution}[solutions]\n\\end{solution}\n'
        self.pattern_solutions='\n'+r'\textbf{(Solution [*])}'+' [solution]\n'
        self.pattern_whole_nopart=r'\question'+'\n\\begin{solution}[solutions]\n\\end{solution}'
        self.pattern_solutions_nopart='\n'+r'\textbf{(Solution [*])}'+' [solution]\n'


    def latexify(self):
        '''
        :return:  a latex code string based on the "pattern".
        '''

        #first based on patterns generate the main body of the questions and solutions

        num=len(self.parts)
        if num==1:  #if there is only one part, the "part" label won't be shown.
            current_question=self.pattern_whole_nopart
            current_question=current_question.replace("[master_question]",self.master_question+'\n'+self.parts[0]["question"])

            # current_part=""
            # nofpart=len(self.parts)
            # for j in range(nofpart):
            #     eachpart=self.parts[j]
            #     part_pattern=self.pattern_parts
            #     part_pattern=part_pattern.replace("[part]",eachpart["question"])
            #     part_pattern=part_pattern.replace("[*]",str(j+1))
            eachpart=self.parts[0]
            nofsol=len(eachpart["solutions"])
            current_sol=""
            for i in range(nofsol):
                current_pattern=self.pattern_solutions
                current_pattern=current_pattern.replace("[solution]",eachpart["solutions"][i])
                current_pattern=current_pattern.replace("[*]",str(i+1))
                current_sol=current_sol+current_pattern
            # part_pattern=part_pattern.replace("[solutions]",current_sol)
            # current_part=current_part+part_pattern
            current_question=current_question.replace("[solutions]",current_sol)
        else: #otherwise show "parts" labels
            current_question=self.pattern_whole
            current_question=current_question.replace("[master_question]",self.master_question)

            current_part=""
            nofpart=len(self.parts)
            for j in range(nofpart):
                eachpart=self.parts[j]
                part_pattern=self.pattern_parts
                part_pattern=part_pattern.replace("[part]",eachpart["question"])
                part_pattern=part_pattern.replace("[*]",str(j+1))
                nofsol=len(eachpart["solutions"])
                current_sol=""
                for i in range(nofsol):
                    current_pattern=self.pattern_solutions
                    current_pattern=current_pattern.replace("[solution]",eachpart["solutions"][i])
                    current_pattern=current_pattern.replace("[*]",str(i+1))
                    current_sol=current_sol+current_pattern
                part_pattern=part_pattern.replace("[solutions]",current_sol)
                current_part=current_part+part_pattern
            current_question=current_question.replace("[parts]",current_part)

        #
        # res=self.preamble_que+'\n'+self.master_question+' '
        # num=len(self.parts)
        # if num==1:  #if there is only one part, the "part" label won't be shown.
        #     current_part=self.parts[0]
        #     res=res+current_part["question"]+'\n'
        #     for sol in current_part["solutions"]:
        #         res=res+'\n'+self.preamble_sol+'\n'+sol+'\n'+self.postamble_sol+'\n'
        # else: #otherwise show "parts" labels
        #     res=res+'\n'+self.preamble_part+'\n'
        #     for current_part in self.parts:
        #         res=res+self.separator_part+' '+current_part["question"]+'\n'
        #         for sol in current_part["solutions"]:
        #             res=res+'\n'+self.preamble_sol+'\n'+sol+'\n'+self.postamble_sol+'\n'
        #     res=res+self.postamble_part
        # res=res+'\n'+self.postamble_que+'\n'
        #
        #then replace all variables by numbers based on varchange
        varlist=self.runthevariables()
        numofvar=len(varlist)
        for i in range(numofvar):
            varname="_var"+str(i)+"_"
            current_question=current_question.replace(varname,str(varlist[i]))
        return current_question

    def runthevariables(self):
        '''
        :param flag: if flag==0, randomize the code. if flag is not 0, use the default value.
        :return: a list of variable vaules.
        '''
        val=[]
        num=len(self.varchange)
        for i in range(num):
            varname='_var'+str(i)+'_'
            cont=self.varchange[i].split('|')[0]
            if self.flag==0:
                exec(cont)
                val.append(eval(varname))
            else:
                pass
                # varname=raw.split('=')[0]
                # val.append(exec(varname+'='+cont[1]))
        return val


    def dump(self):
        res={"master_question": self.master_question,
             "parts":self.parts,
             "varchange":self.varchange,
             "tags":self.tags,
             "course":self.course,
             "packages":self.packages,
             "packagesettings": self.packagesettings,
             "macros":self.macros}
        return res

    def dumps(self):
        res=self.dump()
        return json.dumps(res)

    def load(self,input_data):
        self.question=input_data["question"]
        self.parts=list(input_data["parts"])
        self.varchange=list(input_data["varchange"])
        self.tags=list(input_data["tags"])
        self.course=input_data["course"]








class MyDB(TinyDB):
    THRESHOLD=0.95

    def compare(self,A,B):
        return difflib.SequenceMatcher(None, A, B).ratio()

    def import_from_latex_btype(self,latex_filename,input_tags=[],input_course="",separete_symbol='question'):
        '''
        import from a latex file who contains \begin{question}\end{question} and \begin{solution}\end{solution}
        can add tags and courses when using the function
        separate symbol can be changed to other than 'question' for the purpose of 'exercise' or 'example'
        :param latex_filename:
        :param input_tags:
        :param input_course:
        :param separete_symbol:
        :return:
        '''

        with open(latex_filename,'r') as file:
            data=file.read()
        raw=re.split(r'\\begin{'+separete_symbol+r'}',data)
        num=len(raw)
        tags=input_tags
        course=input_course
        for i in range(num)[1:]:
            piece=re.split(r'\\end{'+separete_symbol+r'}',raw[i])
            master_question=piece[0]
            solutions=re.findall(r'begin{solution}(.*?)\\end{solution}',piece[1],re.S)
            item={"master_question": master_question,
                  "parts":[{"question":"","solutions": solutions}],
                  "varchange": [],
                  "tags":tags,
                  "course":course
                  }
            self.insert(item)


    def check_duplicate(self):
        '''
        used to mark all duplicated entries
        :return:
        '''
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
        '''
        remove all entries which are marked as duplicated
        :return:
        '''
        user=Query()
        self.remove(user.duplicate=="yes")

    def output_latex(self,json_list,separate_symbol="\n"):
        '''
        output a LatexSnippt which contains all questions and solutions from the json_list
        the json_list don't have to be from the database, but it should have question entry (srtings) and solution entry (lists of strings)
        :param json_list:
        :param separate_symbol:
        :return:
        '''
        res=""
        if isinstance(json_list,list):
            for question in reversed(json_list):
                q=LatexSnippt()
                q.append(Command('question'))
                q.append(NoEscape(question["question"]))
                for sol in question["solutions"]:
                    with q.create(EnvSolutions()):
                        q.append(NoEscape(sol))
                res=q.dumps()+'\n'+separate_symbol+'\n'+res


        elif isinstance(json_list,tinydb.database.Document):
            q=LatexSnippt()
            q.append(Command('question'))
            q.append(NoEscape(json_list["question"]))
            for sol in json_list["solutions"]:
                with q.create(EnvSolutions()):
                    q.append(NoEscape(sol))
            res=q.dumps()+separate_symbol+'\n'
        return res


    def random_pickone(self,tags):
        '''
        random pick one problem from tags.
        if tags is a str, pick one problem from the tag.
        if tags is a list, pick one problem which has all these tags.
        after the problem is picked, it is sent to the currentview table.
        :param tags:
        :return:
        '''
        if isinstance(tags,str):
            picked=random.choice(self.search(Query().tags.any([tags])))
            currentview=self.table('currentview')

            currentview.insert(picked)

            return picked
        if isinstance(tags,list):
            return random.choice(self.search(Query().tags.any(tags)))

    def random_pick(self,tags):
        '''
        random pick problems from a list of tags. tags has to be a list, each entry represents a combination of tags
        :param tags:
        :return:
        '''
        q=[]
        for tag in tags:
            q.append(self.random_pickone(tag))
        return q

    def dump_randompick(self,filename,tags,separate_symbol="\n"):
        '''
        random pick problems from a list of tags and write them into a file. The separation is separate_symbol which is default to '\n'
        tags has to be a list, each entry represents a combination of tags
        :param filename:
        :param tags:
        :param separate_symbol:
        :return:
        '''
        text=self.random_pick(tags)
        with open(filename,'w') as file:
            file.write(self.output_latex(text,separate_symbol))

    def update_by_id_s(self,json_data,idnum):
        '''
        update the corresponding field for id
        json_data only contains one item
        :param json_data:
        :param id:
        :return:
        '''
        if "question" in json_data:
            self.update({"question":json_data["question"]},doc_ids=[idnum])
        if "solutions" in json_data:
            self.update({"solutions":json_data["solutions"]},doc_ids=[idnum])
        if "tags" in json_data:
            self.update({"tags":json_data["tags"]},doc_ids=[idnum])
        if "course" in json_data:
            self.update({"course":json_data["course"]},doc_ids=[idnum])

    def update_by_id(self,filename,idnum):
        '''
        update the corresponding field for id from a file
        json_data only contains one item
        :param filename:
        :param id:
        :return:
        '''
        with open(filename,'r') as file:
            data=file.read()
        json_data=json.loads(data)
        self.update_by_id_s(json_data,idnum)


    def display_by_id(self,filename,idnum):
        data=self.get(doc_id=idnum)

        with open(filename,'w') as file:
            file.write(data["question"])
            file.write('-'*30+'\n')
            for i in data["solutions"][:-2]:
                file.write(i)
                file.write('='*30+'\n')
            file.write(data["solutions"][-1]+'\n')
            file.write('-'*30+'\n')
            for i in data["tags"][:-2]:
                file.write(i)
                file.write('\n')
            file.write(data["tags"][-1]+'\n')
            file.write('-'*30+'\n')
            file.write(data["course"])

    def read_from_file(self,filename):
        with open(filename,'r') as file:
            data=file.read()
        raw=data.split('-'*30+'\n')
        question=raw[0]
        s=raw[1]
        t=raw[2]
        course=raw[3]
        solutions=s.split('='*30+'\n')
        tags=t.split('\n')
        json_data={"question":question,"solutions":solutions,"tags":tags,"course":course}
        return json_data

    def update_by_id2(self,filename,idnum):
        '''
        update the corresponding field for id from a file(new pattern)
        json_data only contains one item
        :param filename:
        :param id:
        :return:
        '''
        json_data=self.read_from_file(filename)
        self.update_by_id_s(json_data,idnum)