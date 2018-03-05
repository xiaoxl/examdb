from pylatex.base_classes import Environment, Command, Container, LatexObject, UnsafeCommand, CommandBase
from pylatex.base_classes.command import Arguments,CommandBase
from pylatex.package import Package
from pylatex.utils import dumps_list, rm_temp_dir, NoEscape
import pylatex.config as cf
# from json import *
import random
import json
import json
from pprint import pprint
import random
# from examcls import *

from examcls import *

from LatexSnippt import *



class EnvParts(Environment):
    _latex_name='parts'

class ComPart(CommandBase):
    _latex_name = 'part'

class EnvQuestions(Environment):
    _latex_name='questions'

class ComQuestion(CommandBase):
    _latex_name='question'



if __name__ == '__main__':
    # Basic document
    doc = Document('examdb',
                   documentclass='exam',
                   document_options='11pt',
                   fontenc=None,
                   inputenc=None,
                   # font_size=None,
                   textcomp=False,
                   lmodern=False,
                   # page_numbers=False
                   )
    # packages and some basic settings
    doc.packages.append(Package('amssymb, amsfonts, latexsym, verbatim, xspace, setspace,tikz,multicol,amsmath,multirow'))
    doc.packages.append(Package('geometry','margin=1in'))

    filehead=ExamCls()
    filehead.fillFilehead()
    doc.append(filehead)




    # temp=QuestionModule()
    # doc.append(temp.dumpQuestion())
    #
    #
    # temp=QuestionModule()
    # with open('problemdb.txt','w') as data_file:
    #     # content=json.loads(data_file.read())
    #     # data=[]
    #     # for i in range(len(content)):
    #     #     data.append(content[i])
    #     # temp.loadJSON(data[0])
    #     # temp.saveJSON('js.txt')
    #     data={
    #         "question":["\begin{ddd}$fffff$\end{ddd}",
    #                     "sadfasdf"],
    #         "solution":"asdfasfsa$_var0_$"
    #     }
    #     json.dump(data,data_file)

    with open('problemdb.json','r') as file:
        questionDB=json.loads(file.read())
        question=QuestionModule()
        question.loadJSON(questionDB[0])

    # s=question.getEverything()

    with doc.create(EnvQuestions()):
        for i in range(3):
            question.loadJSON(questionDB[i])
            s=question.dumps()
            doc.append(NoEscape(s))
    # doc.append(NoEscape(s))




    # with doc.create(EnvQuestions()) as question:
    #     question.append(ComQuestion())
    #     with question.create(EnvParts()) as inside:
    #         inside.append(ComPart(options=3))
    #         inside.append(NoEscape(question))
    #         inside.append(NoEscape(solution))
    #         inside.append(ComPart(options=3))
    #         inside.append(NoEscape(r'dfasfsafsafsadfasd'))
    #
    #         inside.append(ComPart(options=3))
    #         inside.append(NoEscape(r'dfasfsafsafsadfasd'))
    #
    #         inside.append(Command('newpage'))

    doc.generate_tex()
    # doc.generate_pdf(clean_tex=False)
