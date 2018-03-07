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
from QuestionModule import *


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

    __class__=r'Math 9C: Calculus'
    __term__=r'2018W'
    __examnum__=r'Final'
    __date__=r'03/23/2018'
    __timelimit__=r'180min'             

    doc.preamble.append(Command('usetikzlibrary','plotmarks'))
    doc.preamble.append(Command('singlespacing'))
    doc.preamble.append(Command('parindent 0ex'))

    # course configurations
    doc.preamble.append(Command('newcommand',Arguments(Command('class'),NoEscape(__class__))))
    doc.preamble.append(Command('newcommand',Arguments(Command('term'),NoEscape(__term__))))
    doc.preamble.append(Command('newcommand',Arguments(Command('examnum'),NoEscape(__examnum__))))
    doc.preamble.append(Command('newcommand',Arguments(Command('examdate'),NoEscape(__date__))))
    doc.preamble.append(Command('newcommand',Arguments(Command('timelimit'),NoEscape(__timelimit__))))

    # document starts
    # some formation setting
    doc.append(Command('pagestyle','head'))
    doc.append(Command('firstpageheader',Arguments('', '', '')))

    # draw header, from head.head file
    doc.append(Command('runningheader',Arguments(Command('class'),NoEscape(r'\examnum\ - Page \thepage\ of \numpages'))))
    doc.append(Command('runningheadrule'))

    with doc.create(LatexFulsh()) as fulsh:
        with fulsh.create(LatexTabular(arguments=NoEscape(r'p{2.8in} r l'))) as tabs:
            with open('edb_setting/header.cfg','r') as file:
                header=file.read().split('<__|__>')
                tabs.append(NoEscape(header[0]))
        fulsh.append(NoEscape(r'\\'))

    doc.append(Command('rule',options='1ex',arguments=Arguments(Command('textwidth'),'.1pt')))
    doc.append(Command('newcommand',Arguments(Command('boxwidth'),'0.8cm')))

    # draw statemnts, from coverpage.cfg, instructions for students
    with open('edb_setting/coverpage.cfg','r') as file:
        con=file.read()
        content=con.split('<__|__>')

    doc.append(NoEscape(content[0]))
    with doc.create(MiniPage(width='3.7in',pos='t')) as minipage:
        minipage.append(Command('vspace','0pt'))
        with minipage.create(Itemize()) as items:
            for itemcont in content[1:]:
                items.add_item(NoEscape(itemcont))

        minipage.append(NoEscape(r'Do not write in the table to the right.'))

    # draw the score table
    doc.append(Command('hfill'))
    with doc.create(MiniPage(width='2.3in',pos='t')) as minipage:
        minipage.append(Command('vspace','0pt'))
        minipage.append(Command('gradetablestretch','2'))
        minipage.append(Command('vqword','Problem'))
        minipage.append(Command('addpoints'))
        # grade table setting
        gradetablesetting='v'
        # gradetablesetting='v][page'
        minipage.append(Command('gradetable',options=NoEscape(gradetablesetting)))

    doc.append(Command('newpage'))
    doc.append(Command('addpoints'))


    with open('problemdb.json','r') as file:
        questionDB=json.loads(file.read())

        # question.loadJSON(questionDB[0])
    #

    with doc.create(EnvQuestions()):
        for i in range(3):
            question=QuestionModule()
            question2=QuestionModule()
            question.loadJSON(questionDB[i])

            question.saveJSON("problem"+str(i)+".txt")
            question.loadQuestion('problem'+str(i)+'.txt')
            with open('problem'+str(i)+'.txt') as file:
                j2=json.loads(file.read())
                question2.loadJSON(j2)
                doc.append(NoEscape(question2.dumps()))





    doc.generate_tex()
